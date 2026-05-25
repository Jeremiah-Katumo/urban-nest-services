from .base_usecase import BaseUseCase
from ..interfaces.campaign_interface import ICampaign

class CampaignUseCase(BaseUseCase):
    
    def __init__(self, repo: ICampaign, response_schema=None):
        super().__init__(repo, response_schema)
        
    async def assign_entity(self, campaign_id: str, entity_id: str):
        ''' Assigns an entity to a campaign.
            - campaign_id: The ID of the campaign to which the entity will be assigned.
            - entity_id: The ID of the entity that will be assigned to the campaign.
            - Calls the repository's assign_entity method to perform the assignment in the database.
            - Returns the updated campaign with the assigned entity.
        '''
        return await self.repo.assign_entity(campaign_id, entity_id)