from fastapi import APIRouter, Depends, Query, status
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from ..domain.entities.campaign_entity import (
    CampaignRead, CampaignCreate, CampaignUpdate, CampaignPaginationList
)
from ..infrastructure.db.database import db
from ..domain.usecases.campaign_usecase import CampaignUseCase
from ..infrastructure.repositories.campaign_repository import CampaignRepository
from ..core.filter_cache_manager import list_cache_key_builder
from ..dependencies.rbac import require_roles


router = APIRouter()

def get_campaign_usecase(session: AsyncSession = Depends(db.get_db)):
    ''' Dependency function to get an instance of CampaignUseCase with the database session '''
    repo = CampaignRepository(session)
    return CampaignUseCase(repo, response_schema=CampaignRead)


@router.post(
    "/",
    response_model=CampaignRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def create_campaign(
    payload: CampaignCreate, 
    use_case: CampaignUseCase = Depends(get_campaign_usecase)
):
    campaign = await use_case.create(payload)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="campaigns:list")
    
    return campaign


@router.get(
    "/{campaign_id}",
    response_model=CampaignRead, 
    dependencies=[Depends(require_roles(["super_admin", "admin", "tenant", "landlord", "agent", "manager"]))],
    status_code=status.HTTP_200_OK
)
async def get_by_id(
    campaign_id: str, use_case: CampaignUseCase = Depends(get_campaign_usecase),
):
    campaign = await use_case.get_by_id(campaign_id)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="campaigns:list")
    return campaign


@router.get(
    "/", 
    response_model=CampaignPaginationList, 
    dependencies=[Depends(require_roles(["admin", "landlord", "agent", "manager", "super_admin"]))],
    status_code=status.HTTP_200_OK
)
@cache(expire=3600, namespace="campaigns:list", key_builder=list_cache_key_builder)
async def get_all(
    page: int = Query(1, ge=1),
    limit: int = Query(20, le=100),
    columns: Optional[str] = None,
    search_filter: Optional[str] = None,
    sort: Optional[str] = "created_at",
    use_case: CampaignUseCase = Depends(get_campaign_usecase),
):
    relations: Optional[List[str]] = ["entity"]
    
    return await use_case.get_all(page, limit, columns, search_filter, sort, relations) 


@router.patch(
    "/{campaign_id}",
    response_model=CampaignRead,
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_201_CREATED
)
async def update_campaign(
    campaign_id: str, 
    payload: CampaignUpdate, 
    use_case: CampaignUseCase = Depends(get_campaign_usecase)
):
    updated = await use_case.update(campaign_id, payload)
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="campaigns:list")
    
    return updated


@router.delete(
    "/{campaign_id}", 
    dependencies=[Depends(require_roles(["super_admin", "admin", "manager", "landlord"]))],
    status_code=status.HTTP_204_NO_CONTENT
)
async def soft_delete(
    campaign_id: str, use_case: CampaignUseCase = Depends(get_campaign_usecase),
):
    if FastAPICache.get_backend():
        await FastAPICache.clear(namespace="campaigns:list")
    return await use_case.soft_delete(campaign_id)