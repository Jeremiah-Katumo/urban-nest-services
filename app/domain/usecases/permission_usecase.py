from .base_usecase import BaseUseCase
from pydantic import StrictBool


class PermissionUseCase(BaseUseCase):
    
    async def assign_permission_to_role(self, role_id: str, permission_id: str):
        return self.repo.assign_permission_to_role(role_id, permission_id)
    
    async def assign_permission_to_user(self, user_id: str, permission_id: str):
        return self.repo.assign_permission_to_user(user_id, permission_id)
    
    async def user_has_permission(self, user_id: str, permission_name: str) -> StrictBool:
        return self.repo.user_has_permission(user_id, permission_name)
    