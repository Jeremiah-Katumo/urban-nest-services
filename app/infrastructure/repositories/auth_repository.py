from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timezone
from ...domain.entities.auth_entity import RegisterSchema
from ...domain.interfaces.auth_interface import IAuth
from ...models.models import UserModel
from ...core.security import hash_password, verify_password


class AuthRepository(IAuth):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def register(self, data: RegisterSchema):
        result = await self.db_session.execute(
            select(UserModel).where(UserModel.email == data.email)
        )
        if result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User Exists"
            )

        user = UserModel(
            username=data.username,
            first_name=data.first_name,
            last_name=data.last_name,
            email=data.email,
            phone=data.phone,
            password=hash_password(data.password),
            role=data.role,
            created_at=datetime.now(timezone.utc)
        )

        self.db_session.add(user)
        await self.db_session.commit()
        await self.db_session.refresh(user)

        return user

    async def authenticate(self, email: str, password: str):
        result = await self.db_session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.password):
            return None

        return user