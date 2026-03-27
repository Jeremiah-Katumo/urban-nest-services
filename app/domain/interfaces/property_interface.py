from abc import ABC, abstractmethod
from ..entities.property_entity import PropertyUpdate, PropertyRead, PropertyCreate


class IProperty(ABC):
    @abstractmethod
    async def create(self, data: PropertyCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> PropertyRead:
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
    async def update(self, id: str, data: PropertyUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def assign_landlord(self, property_id: str, landlord_id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def assign_agent(self, property_id: str, agent_id):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError