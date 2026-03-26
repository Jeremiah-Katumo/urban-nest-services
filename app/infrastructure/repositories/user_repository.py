from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_, asc, desc, func
from datetime import datetime, timezone
from ...models.models import UserModel
from ...domain.enums.user_enum import UserRoles
from ...core import security, query_manager
from ...domain.interfaces.user_interface import IUser
from ...domain.entities.user_entity import UserUpdate


class UserRepository(IUser):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def get_by_id(self, user_id: str):
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.id == user_id,
                UserModel.deleted_at.is_(None)
            )
        )

        user = result.scalar_one_or_none()

        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User not found with id: {id}")

        return user

    async def get_all(
        self,
        page: int,
        limit: int,
        columns: str | None,
        filter: str | None,
        sort: str | None,
    ):
        stmt = select(UserModel).where(UserModel.deleted_at.is_(None))

        stmt = await query_manager.QueryManager.apply_columns(stmt, UserModel, columns) 
        stmt = await query_manager.QueryManager.apply_filters(stmt, UserModel, filter) 
        stmt = await query_manager.QueryManager.apply_sort(stmt, UserModel, sort) 
        result, total = await query_manager.QueryManager.paginate(self.db_session, stmt, page, limit)

        result = await self.db_session.execute(stmt)

        users = result.scalars().all()
        
        return await query_manager.QueryManager.build_response(users, page, limit, total)

    async def get_by_email(self, email: str):
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.email == email,
                UserModel.deleted_at.is_(None)
            )
        )

        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User not found with email: {email}")
            
        return user

    async def get_by_username(self, username: str):
        result = await self.db_session.execute(
            select(UserModel).where(
                UserModel.username == username,
                UserModel.deleted_at.is_(None)
            )
        )

        user = result.scalar_one_or_none()
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"User not found with username: {username}")
            
        return user

    async def update(self, user_id: str, data: UserUpdate):
        user = await self.get_by_id(user_id)

        for field, value in data.dict(exclude_unset=True).items():
            if field == "password":
                value = security.hash_password(value)

            setattr(user, field, value)

        user.updated_at = datetime.now(timezone.utc)

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def assign_role(self, user_id: str, role: UserRoles):
        user = await self.get_by_id(user_id)

        user.role = role
        user.updated_at = datetime.now(timezone.utc)

        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def soft_delete(self, user_id: str):
        user = await self.get_by_id(user_id)

        user.deleted_at = datetime.now(timezone.utc)

        await self.db_session.commit()

        return {"message": "User deleted successfully"}