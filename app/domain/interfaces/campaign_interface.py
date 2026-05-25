from abc import ABC, abstractmethod
from ..entities.campaign_entity import CampaignUpdate, CampaignRead, CampaignCreate


class ICampaign(ABC):
    @abstractmethod
    async def create(self, data: CampaignCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, campaign_id: str) -> CampaignRead:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(
        self,
        page: int,
        limit: int,
        columns: str | None,
        search_filter: str | None,
        sort: str | None,
    ):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, campaign_id: str, data: CampaignUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, campaign_id: str):
        raise NotImplementedError

    @abstractmethod
    async def restore(self, campaign_id: str):
        ''' Restores a soft-deleted campaign by setting its deleted_at field to None. '''
        raise NotImplementedError
    
    @abstractmethod
    async def assign_entity(self, campaign_id: str, entity_id: str):
        ''' Assigns an entity to a campaign by updating the campaign's entity_id field with the provided entity_id. '''
        raise NotImplementedError