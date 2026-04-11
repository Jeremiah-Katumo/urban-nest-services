from abc import ABC, abstractmethod
from ..entities.subscription_entity import SubscriptionRead, SubscriptionCreate, SubscriptionUpdate


class ISubscription(ABC):
    @abstractmethod
    async def create(self, data: SubscriptionCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> SubscriptionRead:
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
    async def update(self, id: str, data: SubscriptionUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
