from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.landlord_entity import (
    LandlordCreate, LandlordUpdate, LandlordRead, LandlordPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.landlord_usecase import LandlordUseCase
from ..infrastructure.repositories.landlord_repository import LandlordRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_landlord_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = LandlordRepository(db)
    return LandlordUseCase(repo)


@router.post(
    "/",
    response_model=LandlordRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def create_landlord(
    data: LandlordCreate,
    use_case: LandlordUseCase = Depends(get_landlord_usecase)
):
    return await use_case.create(data)


@router.get(
    "/{landlord_id}",
    response_model=LandlordRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    landlord_id: str, use_case: LandlordUseCase = Depends(get_landlord_usecase),
):
    return await use_case.get_by_id(landlord_id)


@router.get(
    "/", 
    response_model=LandlordPaginationList, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="properties:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: LandlordUseCase = Depends(get_landlord_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{landlord_id}",
    response_model=LandlordRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_landlord(
    landlord_id: str, payload: LandlordUpdate, use_case: LandlordUseCase = Depends(get_landlord_usecase)
):
    updated = await use_case.update(landlord_id, payload)
    await FastAPICache.clear(namespace="users:list")
    
    return updated


@router.delete(
    "/{landlord_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    landlord_id: str, use_case: LandlordUseCase = Depends(get_landlord_usecase),
):
    return await use_case.delete(landlord_id)
