from fastapi import APIRouter, Depends, Query, status
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi_cache.decorator import cache
from ..domain.entities.user_entity import UserRead, UserCreate, UserPaginationList
from ..infrastructure.db.database import db
from ..domain.usecases.user_usecase import UserUseCase
from ..domain.enums.user_enum import UserRoles
from ..infrastructure.repositories.user_repository import UserRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles
from ..dependencies.auth import get_current_user


router = APIRouter()

@router.post(
    "/", 
    response_model=UserPaginationList, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_200_OK
)
# @cache(expire=3600, namespace="get_all_products_list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=20),
    columns: Optional[str] = None,
    search: Optional[str] = None,
    sort: Optional[str] = "created_at",
    db: AsyncSession = Depends(db.get_db)
):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    
    skip = max((page - 1) * limit, 0)
    
    result = await use_case.get_all(skip, limit, columns, search, sort)
    
    return result  


@router.get(
    "/{id}", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin", "tenant", "landlord", "agent"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(id: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.get_by_id(id)
    return user


@router.get(
    "/{email}/email", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_email(email: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.get_by_email(email)
    return user


@router.get(
    "/{username}/user", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_username(username: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.get_by_username(username)
    return user


@router.post(
    "/role/assign", 
    response_model=UserRead, 
    dependencies=[Depends(require_roles(["admin"]))],
    status_code=status.HTTP_201_CREATED
)
async def assign_role(
    role: UserRoles, 
    db: AsyncSession = Depends(db.get_db), 
    user=Depends(get_current_user)
):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.assign_role(user.id, role)
    return user


@router.delete("/{id}", response_model=UserRead, status_code=status.HTTP_404_NOT_FOUND)
async def soft_delete(id: str, db: AsyncSession = Depends(db.get_db)):
    repo = UserRepository(db)
    use_case = UserUseCase(repo)
    user = await use_case.soft_delete(id)
    return user
