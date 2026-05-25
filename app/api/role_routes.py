from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.role_entity import (
    RoleCreate, RoleRead, RoleUpdate, RolePaginationList
)
from ..domain.entities.user_entity import UserRead
from ..infrastructure.db.database import db
from ..domain.usecases.role_usecase import RoleUseCase
from ..infrastructure.repositories.role_repository import RoleRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles, require_permission


router = APIRouter()

def get_role_usecase(session: AsyncSession = Depends(db.get_db)):
    ''' Dependency function to get an instance of RoleUseCase with the database session '''
    repo = RoleRepository(session)
    return RoleUseCase(repo)


@router.post(
    "/",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED
)
async def create_role(
    payload: RoleCreate,
    use_case: RoleUseCase = Depends(get_role_usecase),
):
    created = await use_case.create(payload)

    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="roles:list")

    return created


@router.post(
    "/with_permissions",
    response_model=RoleRead,
    status_code=status.HTTP_201_CREATED,
    # dependencies=[Depends(require_permission("create_roles"))]
    dependencies=[Depends(require_roles(["super_admin", "admin"]))]
)
async def create_role_with_permissions(
    payload: RoleCreate,
    permission_list: List[str] = Query(..., description="List of permissions to assign to the role"),
    use_case: RoleUseCase = Depends(get_role_usecase)
):
    created = await use_case.create_role_with_permissions(payload, permission_list)

    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="roles:list")

    return created


@router.get(
    "/{role_id}",
    response_model=RoleRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    role_id: str, use_case: RoleUseCase = Depends(get_role_usecase),
):
    role = await use_case.get_by_id(role_id)

    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="roles:list")

    return role


@router.get(
    "/", 
    response_model=RolePaginationList, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="roles:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: RoleUseCase = Depends(get_role_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{role_id}",
    response_model=RoleRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_role(
    role_id: str, payload: RoleUpdate, use_case: RoleUseCase = Depends(get_role_usecase)
):
    updated = await use_case.update(role_id, payload)
    
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="roles:list")
    
    return updated


@router.post(
    "/users/{user_id}/roles/{role_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles(["super_admin", "admin"]))]
)
async def assign_role_to_user(
    user_id: str,
    role_id: str,
    use_case: RoleUseCase = Depends(get_role_usecase),
):
    assigned = await use_case.assign_role_to_user(user_id, role_id)
    
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="users:list")
    
    return assigned


@router.delete(
    "/{role_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    role_id: str, use_case: RoleUseCase = Depends(get_role_usecase),
):
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="roles:list")
        
    return await use_case.soft_delete(role_id)
