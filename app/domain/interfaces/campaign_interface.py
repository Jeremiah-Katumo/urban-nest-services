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
