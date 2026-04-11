from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.subscription_entity import (
    SubscriptionUpdate, SubscriptionRead, SubscriptionCreate, SubscriptionPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.subscription_usecase import SubscriptionUseCase
from ..infrastructure.repositories.subscription_repository import SubscriptionRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_subscription_usecase(db: AsyncSession = Depends(db.get_db)):
    repo = SubscriptionRepository(db)
    return SubscriptionUseCase(repo)


@router.post(
    "/",
    response_model=SubscriptionRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def create_subscription(
    payload: SubscriptionCreate,
    use_case: SubscriptionUseCase = Depends(get_subscription_usecase)
):
    created = await use_case.create(payload)
    await FastAPICache.clear(namespace="subscriptions:list")
    
    return created


@router.get(
    "/{subscription_id}",
    response_model=SubscriptionRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    subscription_id: str, use_case: SubscriptionUseCase = Depends(get_subscription_usecase),
):
    return await use_case.get_by_id(subscription_id)


@router.get(
    "/", 
    response_model=SubscriptionPaginationList, 
    dependencies=[Depends(require_roles(["admin", "tenant", "customer", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="subscriptions:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: SubscriptionUseCase = Depends(get_subscription_usecase),
):
    return await use_case.get_all(page, limit, columns, search_filter, sort) 


@router.patch(
    "/{subscription_id}",
    response_model=SubscriptionRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_subscription(
    subscription_id: str, payload: SubscriptionUpdate, use_case: SubscriptionUseCase = Depends(get_subscription_usecase)
):
    updated = await use_case.update(subscription_id, payload)
    await FastAPICache.clear(namespace="subscriptions:list")
    
    return updated


@router.delete(
    "/{subscription_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    subscription_id: str, use_case: SubscriptionUseCase = Depends(get_subscription_usecase),
):
    return await use_case.delete(subscription_id)
