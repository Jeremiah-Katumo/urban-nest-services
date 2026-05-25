from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..infrastructure.db.database import db
from ..models.models import UserModel
from ..core.security import SECRET_KEY, ALGORITHM
from ..redis.redis_client import is_blacklisted

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

async def get_current_user_oauth_bearer(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(db.get_db)
):
    ''' Dependency to get the current user from an OAuth2 Bearer token.
        - Decodes the JWT token to extract the user ID and checks if the token is blacklisted.
        - If the token is valid and not blacklisted, retrieves the user from the database.
        - Raises HTTP exceptions for invalid tokens, revoked tokens, or if the user is not found.
    '''
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")
        
        if await is_blacklisted(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Token revoked"
            )
            
        user_id = payload.get("sub")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        ) from exc
        
    result = await session.execute(
        select(UserModel).where(UserModel.id==user_id)
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
        
    return user, payload




security = HTTPBearer()

async def get_current_user_http_bearer(
    token=Depends(security),
    session=Depends(db.get_db)
):
    ''' Dependency to get the current user from an HTTP Bearer token.
        - Decodes the JWT token to extract the user ID and checks if the token is blacklisted.
        - If the token is valid and not blacklisted, retrieves the user from the database.
        - Raises HTTP exceptions for invalid tokens, revoked tokens, or if the user is not found.
    '''
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=[ALGORITHM])

        if payload.get("type") != "access":
            raise HTTPException(401, "Invalid token type")

        if await is_blacklisted(payload["jti"]):
            raise HTTPException(401, "Token revoked")

        user_id = payload["sub"]

    except Exception as e:
        raise HTTPException(401, "Invalid token") from e

    result = await session.execute(
        select(UserModel).where(UserModel.id == user_id)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(404, "User not found")

    return user