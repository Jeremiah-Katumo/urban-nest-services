from abc import ABC, abstractmethod
from ..entities.landlord_entity import LandlordUpdate, LandlordRead, LandlordCreate


class ILandlord(ABC):
    @abstractmethod
    async def create(self, data: LandlordCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> LandlordRead:
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
    async def update(self, id: str, data: LandlordUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
