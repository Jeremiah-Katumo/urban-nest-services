from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from ...models.models import UserModel, TenantModel, LandlordModel, AgentModel
from ...domain.enums.user_enum import UserRoles
from ...domain.interfaces.user_interface import IUser
from ...domain.entities.user_entity import UserUpdate, UserRead
from ...core import security
from ...infrastructure.repositories.base_repository import BaseRepository


class UserRepository(BaseRepository[UserModel], IUser):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, UserModel)

    # Only keep custom queries
    async def get_by_email(self, email: str) -> UserRead:
        result = await self.db.execute(
            select(self.model).where(
                self.model.email == email,
                self.model.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    async def get_by_username(self, username: str) -> UserRead:
        result = await self.db.execute(
            select(self.model).where(
                self.model.username == username,
                self.model.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    # Override update ONLY for password handling
    async def update(self, user_id: str, data: UserUpdate) -> UserRead:
        if "password" in data:
            data["password"] = security.hash_password(data["password"])

        return await super().update(user_id, data)

    # Custom business logic stays here (role assignment)
    async def assign_role(self, user_id: str, role: UserRoles) -> UserRead:
        user = await self.get_by_id(user_id)

        if user.role == role:
            return user

        user.role = role
        user.updated_at = datetime.now(timezone.utc)

        profile_map = {
            UserRoles.TENANT: TenantModel,
            UserRoles.LANDLORD: LandlordModel,
            UserRoles.AGENT: AgentModel,
        }

        profile_class = profile_map.get(role)

        if profile_class:
            profile = profile_class(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                created_at=datetime.now(timezone.utc)
            )
            self.db.add(profile)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    # Optional: override soft delete response only
    async def soft_delete(self, user_id: str, soft: bool = True):
        await super().soft_delete(user_id, soft)
        return {"message": "User deleted successfully"}
    