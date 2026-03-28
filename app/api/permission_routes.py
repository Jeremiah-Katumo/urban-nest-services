from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.permission_entity import (
    PermissionCreate, PermissionRead, PermissionUpdate, PermissionPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.permission_usecase import PermissionUseCase
from ..infrastructure.repositories.permission_repository import PermissionRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles, require_permission


router = APIRouter()

def get_permission_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = PermissionRepository(db)
    return PermissionUseCase(repo)


@router.post(
    "/",
    response_model=PermissionRead,
    status_code=status.HTTP_201_CREATED
)
async def create_permission(
    payload: PermissionCreate,
    use_case: PermissionUseCase = Depends(get_permission_usecase),
):
    return await use_case.create(payload)    


@router.get(
    "/{permission_id}",
    response_model=PermissionRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    permission_id: str, use_case: PermissionUseCase = Depends(get_permission_usecase),
):
    return await use_case.get_by_id(permission_id)


@router.get(
    "/", 
    response_model=PermissionRead, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="permissions:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: PermissionUseCase = Depends(get_permission_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{permission_id}",
    response_model=PermissionRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_permission(
    permission_id: str, payload: PermissionUpdate, use_case: PermissionUseCase = Depends(get_permission_usecase)
):
    updated = await use_case.update(permission_id, payload)
    await FastAPICache.clear(namespace="permissions:list")
    
    return updated


@router.post("/roles/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(
    role_id: str,
    permission_id: str,
    use_case: PermissionUseCase = Depends(get_permission_usecase),
    current_user=Depends(require_permission("assign_permissions"))
):
    return await use_case.assign_permission_to_role(role_id, permission_id)    


@router.post("/users/{user_id}/permissions/{permission_id}")
async def assign_permission_to_user(
    user_id: str,
    permission_id: str,
    use_case: PermissionUseCase = Depends(get_permission_usecase),
    current_user=Depends(require_permission("assign_permissions"))
):
    return await use_case.assign_permission_to_user(user_id, permission_id)    


@router.delete(
    "/{permission_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    permission_id: str, use_case: PermissionUseCase = Depends(get_permission_usecase),
):
    return await use_case.delete(permission_id)
