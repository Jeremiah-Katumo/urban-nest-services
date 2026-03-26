from ..interfaces.user_interface import IUser
from ..entities.user_entity import UserRead, UserUpdate
from ..enums.user_enum import UserRoles


class UserUseCase:
    def __init__(self, repo: IUser):
        self.repo = repo
    
    async def get_by_id(self, id: str):
        return await self.repo.get_by_id(id)
    
    async def get_all(
        self,
        page: int,
        limit: int,
        columns: str | None,
        filter: str | None,
        sort: str | None,
    ):
        return self.repo.get_all(page, limit, columns, filter, sort)
    
    async def get_by_email(self, email: str) -> UserRead:
        return self.repo.get_by_email(email)
    
    async def get_by_username(self, username: str) -> UserRead:
        return self.repo.get_by_username(username)
    
    async def update(self, id: str, data: UserUpdate):
        return self.repo.update(id, data)
    
    async def assign_role(self, user_id: str, role: UserRoles) -> UserRead:
        return self.repo.assign_role(user_id, role)
    
    async def soft_delete(self, id: str):
        return self.repo.soft_delete(id)