from .base_usecase import BaseUseCase


class RoleUseCase(BaseUseCase):
    
    async def assign_role_to_user(self, user_id: str, role_id: str):
        return self.assign_role_to_user(user_id, role_id)
    