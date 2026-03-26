from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, desc, asc
from datetime import datetime, timezone
from ...domain.entities.user_entity import UserCreate, UserUpdate
from ...domain.interfaces.user_interface import IUser
from ...models.models import UserModel



class UserRepository(IUser):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session
        
    async def create(self, data):
        new_user = UserModel(**data)
        
        self.db_session.add(new_user)
        self.db_session.commit()
        self.db_session.refresh(new_user)
        
        return new_user
    
    async def get_by_id(self, id: str):
        stmt = select(UserModel).where(UserModel.id==id)
        result = await self.db_session.execute(stmt)
        
        db_user = result.scalar_one_or_none()
        if not db_user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No User found"
            )
            
        return db_user