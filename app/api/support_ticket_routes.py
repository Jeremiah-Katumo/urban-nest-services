from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.support_ticket_entity import (
    SupportTicketRead, SupportTicketUpdate, SupportTicketPaginationList, AISupportTicketRead
)
from ..infrastructure.db.database import db
from ..domain.usecases.support_ticket_usecase import SupportTicketUseCase
from ..infrastructure.repositories.support_ticket_repository import SupportTicketRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_tenant_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = SupportTicketRepository(db)
    return SupportTicketUseCase(repo)


@router.get(
    "/{ticket_id}",
    response_model=SupportTicketRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    ticket_id: str, use_case: SupportTicketUseCase = Depends(get_tenant_usecase),
):
    return await use_case.get_by_id(ticket_id)


@router.get(
    "/", 
    response_model=SupportTicketPaginationList, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="tickets:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: SupportTicketUseCase = Depends(get_tenant_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{ticket_id}",
    response_model=SupportTicketRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_support_ticket(
    ticket_id: str, payload: SupportTicketUpdate, use_case: SupportTicketUseCase = Depends(get_tenant_usecase)
):
    updated = await use_case.update(ticket_id, payload)
    await FastAPICache.clear(namespace="tenants:list")
    
    return updated


@router.delete(
    "/{ticket_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    ticket_id: str, use_case: SupportTicketUseCase = Depends(get_tenant_usecase),
):
    return await use_case.delete(ticket_id)


@router.post("/ai/advanced")
def ai_support(
    session_id: str,
    role: str,
    user_id: int,
    query: str,
    use_case: SupportTicketUseCase = Depends(get_tenant_usecase),
):
    return use_case.ai_support(db, session_id, role, user_id, query)