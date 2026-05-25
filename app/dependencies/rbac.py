from fastapi import Depends, HTTPException, status
from sqlalchemy import select
from .auth import get_current_user_http_bearer #, get_current_user_oauth_bearer
from ..models.models import PermissionModel, UserPermissionModel
from ..redis.redis_client import redis_client


def require_roles(roles):
    ''' Dependency factory to require specific user roles for access control.
        - roles: A list of role names that are allowed to access the endpoint.
        - Returns a dependency function that checks if the current user's role is in the allowed roles.
        - If the user's role is not in the allowed roles, raises a 403 Forbidden HTTP exception.
    '''
    async def checker(user = Depends(get_current_user_http_bearer)):
        
        print("User:", user.id)

        if user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Forbidden"
            )
        return user

    return checker


def require_permission(permission_name: str):
    ''' Dependency factory to require specific permissions for access control.
        - permission_name: The name of the permission required to access the endpoint.
        - Returns a dependency function that checks if the current user has the required permission.
    '''
    async def checker(
        current_user=Depends(get_current_user_http_bearer),
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
    ''' Caches the permissions of a user in Redis for quick access during permission checks.
        - user: The user object for whom to cache permissions.
        - db: The database session to query for permissions.
        - Retrieves permissions from the user's roles and any user-specific permissions, 
            then stores them in Redis with a TTL for efficient access during permission checks.
    '''   
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
    ''' Dependency factory to enforce tenant-based access control.
        - resource_tenant_id: The tenant ID associated with the resource being accessed.
        - Returns a dependency function that checks if the current user's tenant ID matches the resource's tenant ID.
        - If the tenant IDs do not match, raises a 403 Forbidden HTTP exception to prevent cross-tenant access.
    '''
    def checker(current_user=Depends(get_current_user_http_bearer)):
        if current_user.tenant_id != resource_tenant_id:
            raise HTTPException(403, "Cross-tenant access denied")
        
        return current_user
    
    return checker
