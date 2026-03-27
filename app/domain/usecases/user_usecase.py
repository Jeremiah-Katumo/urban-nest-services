from fastapi import HTTPException, status
from ..entities.user_entity import UserUpdate
from ..enums.user_enum import UserRoles
from .base_usecase import BaseUseCase


class UserUseCase(BaseUseCase):

    async def get_by_email(self, email: str):
        user = await self.repo.get_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def get_by_username(self, username: str):
        user = await self.repo.get_by_username(username)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return user

    async def before_update(self, instance, data: UserUpdate):
        if "role" in data:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Use assign_role instead")
        return data

    async def assign_role(self, user_id: str, role: UserRoles):
        user = await self.get_by_id(user_id)

        if user.role == role:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Role already assigned")

        return await self.repo.assign_role(user_id, role)

    async def before_delete(self, instance):
        if instance.role == UserRoles.ADMIN:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Admins cannot be deleted")