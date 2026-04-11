from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.transporter_entity import (
    TransporterRead, TransporterUpdate, TransporterPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.transporter_usecase import TransporterUseCase
from ..infrastructure.repositories.transporter_repository import TransporterRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_transporter_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = TransporterRepository(db)
    return TransporterUseCase(repo)


@router.get(
    "/{transporter_id}",
    response_model=TransporterRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    transporter_id: str, use_case: TransporterUseCase = Depends(get_transporter_usecase),
):
    return await use_case.get_by_id(transporter_id)


@router.get(
    "/", 
    response_model=TransporterPaginationList, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="transporters:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: TransporterUseCase = Depends(get_transporter_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{transporter_id}",
    response_model=TransporterRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_tranporter(
    transporter_id: str, payload: TransporterUpdate, use_case: TransporterUseCase = Depends(get_transporter_usecase)
):
    updated = await use_case.update(transporter_id, payload)
    await FastAPICache.clear(namespace="transporters:list")
    
    return updated


@router.delete(
    "/{transporter_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    transporter_id: str, use_case: TransporterUseCase = Depends(get_transporter_usecase),
):
    return await use_case.delete(transporter_id)
