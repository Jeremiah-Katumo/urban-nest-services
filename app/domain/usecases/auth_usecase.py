from fastapi import HTTPException
from ..interfaces.auth_interface import IAuth
from ..entities.auth_entity import RegisterSchema, LoginSchema
from ...core.security import create_access_token, create_refresh_token


class AuthUseCase:
    def __init__(self, repo: IAuth):
        self.repo = repo
        
    async def register(self, data: RegisterSchema):
        return await self.repo.register(data)
    
    async def authenticate(self, data: LoginSchema):
        user = await self.repo.authenticate(data.email, data.password)
        
        if not user:
            raise HTTPException(401, "Invalid credentials")

        return {
            "access_token": create_access_token(user.id, user.role.value),
            "refresh_token": create_refresh_token(user.id)
        }

    async def reset_password(self, user_id: str, password: str):
        return await self.repo.reset_password(user_id, password)
