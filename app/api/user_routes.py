from fastapi import APIRouter, Depends, Query, status
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_cache.decorator import cache
from ..domain.entities.user_entity import UserRead, UserUpdate, UserPaginationList
from ..infrastructure.db.database import db
from ..domain.usecases.user_usecase import UserUseCase
from ..domain.enums.user_enum import UserRoles
from ..infrastructure.repositories.user_repository import UserRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_user_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    return UserUseCase(repo)


@router.get(
    "/", 
    response_model=UserPaginationList, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="get_all_products_list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: UserUseCase = Depends(get_user_usecase),
):
    return await use_case.get_all(page, limit, columns, filter, sort) 


@router.get(
    "/{user_id}", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin", "tenant", "landlord", "agent"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    user_id: str, use_case: UserUseCase = Depends(get_user_usecase),
):
    return await use_case.get_by_id(user_id)


@router.get(
    "/{email}/email", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_email(
    email: str, use_case: UserUseCase = Depends(get_user_usecase),
):
    return await use_case.get_by_email(email)


@router.get(
    "/{username}/user", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_username(
    username: str,  use_case: UserUseCase = Depends(get_user_usecase),
):
    return await use_case.get_by_username(username)


@router.patch(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_user(
    user_id: int, payload: UserUpdate, use_case: UserUseCase = Depends(get_user_usecase)
):
    return await use_case.update(user_id, payload)


@router.patch(
    "/{user_id}/role", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_201_CREATED
)
async def assign_role(
    user_id: str, role: UserRoles, use_case: UserUseCase = Depends(get_user_usecase),
):
    return await use_case.assign_role(user_id, role)


@router.delete(
    "/{user_id}", 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    user_id: str, use_case: UserUseCase = Depends(get_user_usecase),
):
    return await use_case.delete(user_id)
