from abc import ABC, abstractmethod
from ..entities.user_entity import UserUpdate, UserRead
from ..enums.user_enum import UserRoles


class IUser(ABC):    
    @abstractmethod
    async def get_by_id(self, id: str) -> UserRead:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(
        self,
        page: int,
        limit: int,
        columns: str | None,
        filter: str | None,
        sort: str | None,
    ):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_email(self, email: str) -> UserRead:
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_username(self, username: str) -> UserRead:
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, id: str, data: UserUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def assign_role(self, user_id: str, role: UserRoles) -> UserRead:
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError