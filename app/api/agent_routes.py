from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.agent_entity import (
    AgentCreate, AgentUpdate, AgentRead, AgentPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.agent_usecase import AgentUseCase
from ..infrastructure.repositories.agent_repository import AgentRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_agent_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = AgentRepository(db)
    return AgentUseCase(repo)


@router.get(
    "/{agent_id}",
    response_model=AgentRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    agent_id: str, use_case: AgentUseCase = Depends(get_agent_usecase),
):
    return await use_case.get_by_id(agent_id)


@router.get(
    "/", 
    response_model=AgentPaginationList, 
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
    use_case: AgentUseCase = Depends(get_agent_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{agent_id}",
    response_model=AgentRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_agent(
    agent_id: str, payload: AgentUpdate, use_case: AgentUseCase = Depends(get_agent_usecase)
):
    updated = await use_case.update(agent_id, payload)
    await FastAPICache.clear(namespace="users:list")
    
    return updated


@router.delete(
    "/{agent_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    agent_id: str, use_case: AgentUseCase = Depends(get_agent_usecase),
):
    return await use_case.delete(agent_id)
