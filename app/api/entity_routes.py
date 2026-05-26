from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.entity_entity import (
    EntityCreate, EntityRead, EntityUpdate, EntityPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.entity_usecase import EntityUseCase
from ..infrastructure.repositories.entity_repository import EntityRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles

router = APIRouter()

def get_entity_usecase(session: AsyncSession = Depends(db.get_db)):
    ''' Dependency to get EntityUseCase instance '''
    repo = EntityRepository(session)
    return EntityUseCase(repo)


@router.post(
    "/",
    response_model=EntityRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def create_entity(
    payload: EntityCreate,
    use_case: EntityUseCase = Depends(get_entity_usecase)
):
    created = await use_case.create(payload)
    
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="entities:list")
    
    return created


@router.get(
    "/{entity_id}",
    response_model=EntityRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_entity_by_id(
    entity_id: str, use_case: EntityUseCase = Depends(get_entity_usecase),
):
    entity = await use_case.get_by_id(entity_id)
    
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="entities:list")
        
    return entity


@router.get(
    "/",
    response_model=EntityPaginationList,
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=60, key_builder=list_cache_key_builder, namespace="entities:list")
async def get_all_entities(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    size: int = Query(10, ge=1, le=100),
    use_case: EntityUseCase = Depends(get_entity_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort, size)


@router.patch(
    "/{entity_id}",
    response_model=EntityRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_200_OK
)
async def update_entity(
    entity_id: str,
    payload: EntityUpdate,
    use_case: EntityUseCase = Depends(get_entity_usecase)
):
    updated = await use_case.update(entity_id, payload)
    
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="entities:list")
    
    return updated


@router.delete(
    "/{entity_id}",
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_entity(
    entity_id: str,
    use_case: EntityUseCase = Depends(get_entity_usecase)
):
    await use_case.delete(entity_id)
    
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="entities:list")