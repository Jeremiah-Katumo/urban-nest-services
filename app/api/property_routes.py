from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.property_entity import (
    PropertyCreate, PropertyUpdate, PropertyRead, PropertyPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.property_usecase import PropertyUseCase
from ..infrastructure.repositories.property_repository import PropertyRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_property_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = PropertyRepository(db)
    return PropertyUseCase(repo)


@router.post(
    "/",
    response_model=PropertyRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def create_property(
    data: PropertyCreate,
    use_case: PropertyUseCase = Depends(get_property_usecase)
):
    return await use_case.create(data)


@router.get(
    "/{property_id}",
    response_model=PropertyRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    property_id: str, use_case: PropertyUseCase = Depends(get_property_usecase),
):
    return await use_case.get_by_id(property_id)


@router.get(
    "/", 
    response_model=PropertyPaginationList, 
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
    use_case: PropertyUseCase = Depends(get_property_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{property_id}",
    response_model=PropertyRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_property(
    property_id: str, payload: PropertyUpdate, use_case: PropertyUseCase = Depends(get_property_usecase)
):
    updated = await use_case.update(property_id, payload)
    await FastAPICache.clear(namespace="users:list")
    
    return updated


@router.patch(
    "/{property_id}/landlord", 
    response_model=PropertyRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_201_CREATED
)
async def assign_landlord(
    property_id: str, landlord_id: str, use_case: PropertyUseCase = Depends(get_property_usecase),
):
    return await use_case.assign_landlord(property_id, landlord_id)


@router.patch(
    "/{property_id}/agent", 
    response_model=PropertyRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager"]))],
    status_code=status.HTTP_201_CREATED
)
async def assign_agent(
    property_id: str, agent_id: str, use_case: PropertyUseCase = Depends(get_property_usecase),
):
    return await use_case.assign_agent(property_id, agent_id)


@router.delete(
    "/{property_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    property_id: str, use_case: PropertyUseCase = Depends(get_property_usecase),
):
    return await use_case.delete(property_id)
