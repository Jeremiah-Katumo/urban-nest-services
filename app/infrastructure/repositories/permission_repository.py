from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import StrictBool
from .base_repository import BaseRepository
from ...models.models import PermissionModel, RoleModel, UserPermissionModel, UserModel
from ...domain.interfaces.permission_interface import IPermission


class PermissionRepository(BaseRepository[PermissionModel], IPermission):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, PermissionModel)
        
    async def assign_permission_to_role(self, role_id: str, permission_id: str ):
        db_role = await self.db.execute(
            select(RoleModel).where(
                RoleModel.id == role_id,
                RoleModel.deleted_at.is_(None)
            )
        )
        role = db_role.scalar_one_or_none()
        
        db_permission =  await self.db.execute(
            select(PermissionModel).where(
                PermissionModel.id == permission_id,
                PermissionModel.deleted_at.is_(None)
            )
        )
        permission = db_permission.scalar_one_or_none()
        
        if not role or not permission:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Role or Permission not found"
            )
            
        role.permissions.append(permission)
        
        await self.db.commit()
        await self.db.refresh(role)
        
        return role
            
    async def assign_permission_to_user(self, user_id: str, permission_id: str):
        user_perm = UserPermissionModel(
            user_id=user_id,
            permission_id=permission_id
        )

        self.db.add(user_perm)
        await self.db.commit()

        return user_perm
    
    async def user_has_permission(self, user_id: str, permission_name: str) -> StrictBool:
        user = await self.db.execute(
            select(UserModel).where(
                UserModel.id == user_id,
                UserModel.deleted_at.is_(None)
            )
        )
        user = user.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )

        user_permissions = {
            perm.name
            for role in user.roles
            for perm in role.permissions
        }

        return True if permission_name in user_permissions else False