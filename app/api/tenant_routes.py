from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.tenant_entity import (
    TenantCreate, TenantRead, TenantUpdate, TenantPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.tenant_usecase import TenantUseCase
from ..infrastructure.repositories.tenant_repository import TenantRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_tenant_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = TenantRepository(db)
    return TenantUseCase(repo)


@router.get(
    "/{tenant_id}",
    response_model=TenantRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    tenant_id: str, use_case: TenantUseCase = Depends(get_tenant_usecase),
):
    return await use_case.get_by_id(tenant_id)


@router.get(
    "/", 
    response_model=TenantPaginationList, 
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
    use_case: TenantUseCase = Depends(get_tenant_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{tenant_id}",
    response_model=TenantRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_tenant(
    tenant_id: str, payload: TenantUpdate, use_case: TenantUseCase = Depends(get_tenant_usecase)
):
    updated = await use_case.update(tenant_id, payload)
    await FastAPICache.clear(namespace="users:list")
    
    return updated


@router.delete(
    "/{tenant_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    tenant_id: str, use_case: TenantUseCase = Depends(get_tenant_usecase),
):
    return await use_case.delete(tenant_id)
