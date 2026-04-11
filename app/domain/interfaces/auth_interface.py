from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession
from ..entities.auth_entity import RegisterSchema


class IAuth(ABC):
    @abstractmethod
    async def register(self, data):
        raise NotImplementedError
    
    @abstractmethod
    async def authenticate(self, plain: str, password: str):
        raise NotImplementedError
    
    
