from .base_usecase import BaseUseCase


class PermissionUseCase(BaseUseCase):
    
    async def assign_permission_to_role(self, role_id: str, permission_id: str):
        return self.assign_permission_to_role(role_id, permission_id)
    
    async def assign_permission_to_user(self, user_id: str, permission_id: str):
        return self.assign_permission_to_user(user_id, permission_id)
    