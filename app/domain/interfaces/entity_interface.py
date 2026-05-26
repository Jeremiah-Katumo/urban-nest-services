from abc import ABC, abstractmethod
from ..entities.entity_entity import EntityUpdate, EntityRead, EntityCreate


class IEntity(ABC):
    @abstractmethod
    async def create(self, data: EntityCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> EntityRead:
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
    async def update(self, entity_id: str, data: EntityUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, entity_id: str):
        raise NotImplementedError

    @abstractmethod
    async def restore(self, entity_id: str):
        ''' Restores a soft-deleted entity by setting its deleted_at field to None. '''
        raise NotImplementedError