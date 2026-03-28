from abc import ABC, abstractmethod
from ..entities.role_entity import RoleCreate, RoleRead, RoleUpdate
from ...models.models import RoleModel

class IRole(ABC):
    @abstractmethod
    async def create(self, data: RoleCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> RoleRead:
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
    async def update(self, id: str, data: RoleUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def assign_role_to_user(self, user_id: str, role_id: str):
        raise NotImplementedError
    