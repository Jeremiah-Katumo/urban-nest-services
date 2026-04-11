from ..interfaces.auth_interface import IAuth
from ..entities.auth_entity import RegisterSchema


class AuthUseCase:
    def __init__(self, repo: IAuth):
        self.repo = repo
        
    async def register(self, data):
        return await self.repo.register(data)
    
    async def authenticate(self, email: str, password: str):
        return await self.repo.authenticate(email, password)

    async def reset_password(self, user_id: str, password: str):
        return await self.repo.reset_password(user_id, password)
