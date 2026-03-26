from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from jose import jwt
from fastapi.security import OAuth2PasswordRequestForm
from ..infrastructure.db.database import db
from ..domain.entities.auth_entity import RegisterSchema, LoginSchema
from ..domain.usecases.auth_usecase import AuthUseCase
from ..infrastructure.repositories.auth_repository import AuthRepository
from ..core.security import (
    create_access_token,
    create_refresh_token,
    SECRET_KEY,
    ALGORITHM
)
from ..dependencies.auth import get_current_user
from ..redis.redis_client import blacklist_token

router = APIRouter()


@router.post("/register")
async def register(data: RegisterSchema, session: AsyncSession = Depends(db.get_db)):
    repo = AuthRepository(session)
    use_case = AuthUseCase(repo)
    
    user = await use_case.register(data)

    return {
        "access_token": create_access_token(user.id, user.role.value),
        "refresh_token": create_refresh_token(user.id)
    }


@router.post("/login")
async def login(data: OAuth2PasswordRequestForm, session: AsyncSession = Depends(db.get_db)):
    repo = AuthRepository(session)
    use_case = AuthUseCase(repo)
    
    user = await use_case.authenticate(data.username, data.password)

    if not user:
        raise HTTPException(401, "Invalid credentials")

    return {
        "access_token": create_access_token(user.id, user.role.value),
        "refresh_token": create_refresh_token(user.id)
    }


@router.post("/refresh")
async def refresh_token(refresh_token: str):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "refresh":
            raise Exception()

        user_id = payload.get("sub")

        return {
            "access_token": create_access_token(user_id, "user")
        }

    except:
        raise HTTPException(401, "Invalid refresh token")


@router.post("/logout")
async def logout(token_data = Depends(get_current_user)):
    _, payload = token_data

    jti = payload.get("jti")
    exp = payload.get("exp")

    await blacklist_token(jti, exp)

    return {"message": "Logged out successfully"}