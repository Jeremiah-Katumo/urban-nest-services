from .base_usecase import BaseUseCase
from ..entities.role_entity import RoleCreate


class RoleUseCase(BaseUseCase):
    
    async def assign_role_to_user(self, user_id: str, role_id: str):
        return await self.repo.assign_role_to_user(user_id, role_id)
    
    async def create_role_with_permissions(self, role_data: RoleCreate, permission_list: list):
        return await self.repo.create_role_with_permissions(role_data, permission_list)
    