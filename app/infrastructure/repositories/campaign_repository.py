from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ...domain.interfaces.campaign_interface import ICampaign
from ...models.models import CampaignModel


class CampaignRepository(BaseRepository[CampaignModel], ICampaign):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, CampaignModel)