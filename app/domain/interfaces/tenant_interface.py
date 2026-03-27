from abc import ABC, abstractmethod
from ..entities.tenant_entity import TenantUpdate, TenantRead, TenantCreate


class ITenant(ABC):
    @abstractmethod
    async def create(self, data: TenantCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> TenantRead:
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
    async def update(self, id: str, data: TenantUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
