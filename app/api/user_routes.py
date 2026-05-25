from fastapi import APIRouter, Depends, Query, status
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from ..domain.entities.user_entity import UserRead, UserUpdate, UserPaginationList
from ..infrastructure.db.database import db
from ..domain.usecases.user_usecase import UserUseCase
from ..domain.enums.user_enum import UserRoles
from ..infrastructure.repositories.user_repository import UserRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_user_usecase(session: AsyncSession = Depends(db.get_db)):
    ''' Dependency function to get an instance of UserUseCase with the database session '''
    repo = UserRepository(session)
    return UserUseCase(repo)


@router.get(
    "/", 
    response_model=UserPaginationList, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="users:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: UserUseCase = Depends(get_user_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.get(
    "/{user_id}", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    user_id: str, use_case: UserUseCase = Depends(get_user_usecase),
):
    user = await use_case.get_by_id(user_id)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="users:list")
    return user


@router.get(
    "/{email}/email", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_email(
    email: str, use_case: UserUseCase = Depends(get_user_usecase),
):
    user = await use_case.get_by_email(email)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="users:list")
    return user


@router.get(
    "/{username}/user", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_username(
    username: str,  use_case: UserUseCase = Depends(get_user_usecase),
):
    user = await use_case.get_by_username(username)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="users:list")
    return user


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_user(
    user_id: str, payload: UserUpdate, use_case: UserUseCase = Depends(get_user_usecase)
):
    updated = await use_case.update(user_id, payload)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="users:list")
    
    return updated


@router.patch(
    "/{user_id}/role", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_201_CREATED
)
async def assign_role(
    user_id: str, role: UserRoles, use_case: UserUseCase = Depends(get_user_usecase),
):
    assigned = await use_case.assign_role(user_id, role)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="users:list")
    return assigned


@router.delete(
    "/{user_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    user_id: str, use_case: UserUseCase = Depends(get_user_usecase),
):
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="users:list")
        
    return await use_case.soft_delete(user_id)