from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.field_entity import (
    FieldCreate, FieldRead, FieldUpdate, FieldPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.field_usecase import FieldUseCase
from ..infrastructure.repositories.field_repository import FieldRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_field_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = FieldRepository(db)
    return FieldUseCase(repo)


@router.post(
    "/",
    response_model=FieldRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def create_custom_field(
    payload: FieldCreate,
    use_case: FieldUseCase = Depends(get_field_usecase)
):
    created = await use_case.create(payload)
    await FastAPICache.clear(namespace="fields:list")
    
    return created


@router.get(
    "/{field_id}",
    response_model=FieldRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    field_id: str, use_case: FieldUseCase = Depends(get_field_usecase),
):
    return await use_case.get_by_id(field_id)


@router.get(
    "/{module}/module",
    response_model=FieldRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_all_by_module(
    module: str, use_case: FieldUseCase = Depends(get_field_usecase),
):
    return await use_case.get_all_by_module(module)


@router.get(
    "/", 
    response_model=FieldPaginationList, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="fields:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: FieldUseCase = Depends(get_field_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{field_id}",
    response_model=FieldRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_custom_field(
    field_id: str, payload: FieldUpdate, use_case: FieldUseCase = Depends(get_field_usecase)
):
    updated = await use_case.update(field_id, payload)
    await FastAPICache.clear(namespace="fields:list")
    
    return updated


@router.delete(
    "/{field_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    field_id: str, use_case: FieldUseCase = Depends(get_field_usecase),
):
    return await use_case.delete(field_id)
