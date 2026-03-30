from abc import ABC, abstractmethod
from ..entities.role_entity import RoleCreate, RoleRead, RoleUpdate


class IRole(ABC):
    @abstractmethod
    async def create(self, data: RoleCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, role_id: str) -> RoleRead:
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
    async def update(self, role_id: str, data: RoleUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, role_id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def assign_role_to_user(self, user_id: str, role_id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def create_role_with_permissions(self, role_data: RoleCreate, permission_list: list):
        raise NotImplementedError