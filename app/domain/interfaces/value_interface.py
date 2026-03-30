from abc import ABC, abstractmethod
from typing import List
from ..entities.value_entity import ValueCreate, ValueRead, ValueUpdate
from ...models.models import ValueModel


class IValue(ABC):
    @abstractmethod
    async def create(self, data: ValueCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, value_id: str) -> ValueRead:
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
    async def update(self, value_id: str, data: ValueUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, value_id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_entity(self, module: str, entity_id: str) -> List[ValueModel]:
        raise NotImplementedError
    