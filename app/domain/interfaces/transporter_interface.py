from abc import ABC, abstractmethod
from ..entities.transporter_entity import TransporterUpdate, TransporterRead, TransporterCreate


class ITransporter(ABC):
    @abstractmethod
    async def create(self, data: TransporterCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> TransporterRead:
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
    async def update(self, id: str, data: TransporterUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
