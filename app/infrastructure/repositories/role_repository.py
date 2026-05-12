from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from .base_repository import BaseRepository
from ...models.models import (
    RoleModel, UserModel, PermissionModel, 
    TenantModel, LandlordModel, AgentModel, TransporterModel
)
from ...domain.interfaces.role_interface import IRole
from ...redis.redis_client import redis_client
from ...domain.enums.user_enum import UserRoles
from ...domain.entities.role_entity import RoleCreate


class RoleRepository(BaseRepository[RoleModel], IRole):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, RoleModel)
        
    async def create_role_with_permissions(self, role_data: RoleCreate, permission_list: list):
        result = await self.db.execute(
            select(PermissionModel).where(
                PermissionModel.name.in_(permission_list)
            )
        )
        permissions = result.scalars().all()

        role = RoleModel(
            name=role_data.name,
            description=role_data.description,
            permissions=permissions
        )

        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)

        return role
        
    async def assign_role_to_user(self, user_id: str, role_id: str):
        user = await self.db.get(UserModel, user_id)
        role = await self.db.get(RoleModel, role_id)

        if not user or not role:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User or Role not found"
            )

        user.roles.append(role)
        user.updated_at = datetime.now(timezone.utc)

        profile_map = {
            UserRoles.TENANT: (TenantModel, "tenant_id"),
            UserRoles.LANDLORD: (LandlordModel, "landlord_id"),
            UserRoles.AGENT: (AgentModel, "agent_id"),
            UserRoles.MOVER: (TransporterModel, "transporter_id"),
        }

        role_enum = role.name  # ensure this matches UserRoles enum
        profile_entry = profile_map.get(role_enum)

        if profile_entry:
            profile_class, user_fk_field = profile_entry

            profile = profile_class(
                # user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email,
                phone=user.phone,
                created_at=datetime.now(timezone.utc)
            )

            self.db.add(profile)
            await self.db.flush()  # 🔥 important: gets ID without commit

            # ✅ assign generated profile ID (FK) to user
            setattr(user, user_fk_field, profile.id)

        await self.db.commit()
        await self.db.refresh(user)

        # 🔥 Invalidate cache
        await redis_client.delete(f"permissions:user:{user.id}")

        return user
    