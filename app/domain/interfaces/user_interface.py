from abc import ABC, abstractmethod
from ..entities.user_entity import UserCreate, UserUpdate, UserRead


class IUser(ABC):
    @abstractmethod
    async def create(self, data: UserCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> UserRead:
        raise NotImplementedError
    
    # @abstractmethod
    # async def get_all(self, page: int, limit: int, columns: str|None, filter: str|None, sort: str|None):
    #     raise NotImplementedError
    
    # @abstractmethod
    # async def update(self, id: str, data: UserUpdate):
    #     raise NotImplementedError
    
    # @abstractmethod
    # async def soft_delete(self, id: str):
    #     raise NotImplementedError