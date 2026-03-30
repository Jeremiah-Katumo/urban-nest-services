from abc import ABC, abstractmethod
from pydantic import StrictBool
from ..entities.permission_entity import PermissionCreate, PermissionRead, PermissionUpdate

class IPermission(ABC):
    @abstractmethod
    async def create(self, data: PermissionCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> PermissionRead:
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
    async def update(self, id: str, data: PermissionUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def assign_permission_to_role(self, role_id: str, permission_id: str ):
        raise NotImplementedError
    
    @abstractmethod
    async def assign_permission_to_user(self, user_id: str, permission_id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def user_has_permission(self, user_id: str, permission_name: str) -> StrictBool:
        raise NotImplementedError