from abc import ABC, abstractmethod
from typing import List
from ..entities.field_entity import FieldUpdate, FieldRead, FieldCreate
from ...models.models import FieldModel


class IField(ABC):
    @abstractmethod
    async def create(self, data: FieldCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, field_id: str) -> FieldRead:
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
    async def update(self, field_id: str, data: FieldUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, field_id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def get_all_by_module(self, module: str) -> List[FieldModel]:
        raise NotImplementedError