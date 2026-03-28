import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .auth import get_current_user
from ..models.models import PermissionModel, UserPermissionModel
from ..infrastructure.db.database import db
from ..redis.redis_client import redis_client


def require_roles(roles):
    async def checker(data = Depends(get_current_user)):
        user, _ = data
        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return user
    return checker


def require_permission(permission_name: str):
    async def checker(
        current_user=Depends(get_current_user),
    ):
        cache_key = f"permissions:user:{current_user.id}"
        cached = await redis_client.get(cache_key)

        if not cached:
            raise HTTPException(403, "Permissions not loaded")

        permissions = set(cached.split(","))

        if permission_name not in permissions:
            raise HTTPException(403, "Permission denied")

        return current_user

    return checker


async def cache_user_permissions(user, db):
    permissions = set()

    # Role permissions
    for role in user.roles:
        for perm in role.permissions:
            permissions.add(perm.name)

    # User-specific permissions
    result = await db.execute(
        select(PermissionModel.name)
        .join(UserPermissionModel)
        .where(UserPermissionModel.user_id == user.id)
    )

    permissions.update([row[0] for row in result.all()])

    # 🔥 Store in Redis (TTL optional)
    await redis_client.set(
        name=f"permissions:user:{user.id}",
        value=",".join(permissions),
        ex=3600  # 1 hour cache
    )
    
    
def enforce_tenant_access(resource_tenant_id: str):
    def checker(current_user=Depends(get_current_user)):
        if current_user.tenant_id != resource_tenant_id:
            raise HTTPException(403, "Cross-tenant access denied")
        return current_user
    return checker