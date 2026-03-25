from ..interfaces.user_interface import IUser
from ..repository.user_repository import UserRepository
from ..entities.user_entity import UserCreate, UserRead, UserUpdate


class UserUseCase:
    def __init__(self, repo: IUser):
        self.repo = repo
        
    async def create(self, data):
        return await self.repo.create(**data)
    
    async def get_by_id(self, id: str):
        return await self.repo.get_by_id(id)