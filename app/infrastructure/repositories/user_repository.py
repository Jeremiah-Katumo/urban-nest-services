from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, asc, desc, func
from datetime import datetime, timezone
from ...models.models import UserModel
from ...domain.enums.user_enum import UserRoles
from ...core.security import hash_password
from ...domain.interfaces.user_interface import IUser
from ...domain.entities.user_entity import UserUpdate


class UserRepository(IUser):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, user_id: str):
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.id == user_id,
                UserModel.deleted_at.is_(None)
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="User not found")

        return user

    async def get_all(
        self,
        skip: int = 0,
        limit: int = 10,
        search: str = None,
        sort_by: str = "created_at",
        order: str = "desc"
    ):
        stmt = select(UserModel).where(UserModel.deleted_at.is_(None))

        # Search
        if search:
            stmt = stmt.where(
                or_(
                    UserModel.first_name.ilike(f"%{search}%"),
                    UserModel.last_name.ilike(f"%{search}%"),
                    UserModel.email.ilike(f"%{search}%")
                )
            )

        # Sorting
        column = getattr(UserModel, sort_by, UserModel.created_at)
        stmt = stmt.order_by(desc(column) if order == "desc" else asc(column))
        
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total = await self.db_session(count_stmt)

        stmt = stmt.offset(skip).limit(limit)

        result = await self.db_session.execute(stmt)

        return result.scalars().all()

    async def get_by_email(self, email: str):
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.email == email,
                UserModel.deleted_at.is_(None)
            )
        )

        return result.scalar_one_or_none()

    async def get_by_username(self, username: str):
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.username == username,
                UserModel.deleted_at.is_(None)
            )
        )

        return result.scalar_one_or_none()

    async def update(self, user_id: str, data: UserUpdate):
        user = await self.get_by_id(user_id)

        for field, value in data.dict(exclude_unset=True).items():
            if field == "password":
                value = hash_password(value)

            setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def assign_role(self, user_id: str, role: UserRoles):
        user = await self.get_by_id(user_id)

        user.role = role
        user.updated_at = datetime.now(timezone.utc)

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def soft_delete(self, user_id: str):
        user = await self.get_by_id(user_id)

        user.deleted_at = datetime.now(timezone.utc)

        await self.db_session.commit()

        return {"message": "User deleted successfully"}