from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.value_entity import (
    ValueCreate, ValueRead, ValueUpdate, ValuePaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.value_usecase import ValueUseCase
from ..infrastructure.repositories.value_repository import ValueRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_field_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = ValueRepository(db)
    return ValueUseCase(repo)


@router.post(
    "/",
    response_model=ValueRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def create_custom_value(
    payload: ValueCreate,
    use_case: ValueUseCase = Depends(get_field_usecase)
):
    created = await use_case.create(payload)
    await FastAPICache.clear(namespace="values:list")
    
    return created


@router.get(
    "/{field_id}",
    response_model=ValueRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    field_id: str, use_case: ValueUseCase = Depends(get_field_usecase),
):
    return await use_case.get_by_id(field_id)


@router.get(
    "/{module}/module{entity_id}/entity",
    response_model=ValueRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_all_by_module_and_entity(
    entity_id: str, module: str, use_case: ValueUseCase = Depends(get_field_usecase),
):
    return await use_case.get_by_entity(module, entity_id)


@router.get(
    "/", 
    response_model=ValuePaginationList, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="values:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: ValueUseCase = Depends(get_field_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{field_id}",
    response_model=ValueRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_custom_value(
    field_id: str, payload: ValueUpdate, use_case: ValueUseCase = Depends(get_field_usecase)
):
    updated = await use_case.update(field_id, payload)
    await FastAPICache.clear(namespace="values:list")
    
    return updated


@router.delete(
    "/{field_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    field_id: str, use_case: ValueUseCase = Depends(get_field_usecase),
):
    return await use_case.delete(field_id)
