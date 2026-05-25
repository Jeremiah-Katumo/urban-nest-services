from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ...domain.interfaces.campaign_interface import ICampaign
from ...models.models import CampaignModel


class CampaignRepository(BaseRepository[CampaignModel], ICampaign):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, CampaignModel)
        
    async def assign_entity(self, campaign_id: str, entity_id: str):
        ''' Assigns an entity to a campaign by updating the campaign's entity_id field with the provided entity_id. '''
        campaign = await self.get_by_id(campaign_id)
        
        campaign.entity_id = entity_id
        
        await self.db_session.commit()
        await self.db_session.refresh(campaign)
        return campaign