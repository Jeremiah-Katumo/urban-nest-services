from fastapi import HTTPException, status
from typing import Generic, Type, TypeVar, Sequence
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from datetime import datetime, timezone
from ...core import query_manager

TModel = TypeVar("TModel")

class BaseRepository(Generic[TModel]):
    
    def __init__(self, db: AsyncSession, model: Type[TModel]):
        self.db = db
        self.model = model
        
    async def get_by_id(self, entity_id: str) -> TModel | None:
        result = await self.db.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        return result.scalar_one_or_none()
    
    async def get_all(
        self,
        page: int,
        limit: int,
        columns: str | None,
        search_filter: str | None,
        sort: str | None,
    ):
        stmt = select(self.model).where(self.model.deleted_at.is_(None))
        
        stmt = await query_manager.QueryManager.apply_columns(stmt, self.model, columns) 
        stmt = await query_manager.QueryManager.apply_filters(stmt, self.model, search_filter) 
        stmt = await query_manager.QueryManager.apply_sort(stmt, self.model, sort) 
        result, total = await query_manager.QueryManager.paginate(self.db, stmt, page, limit)

        result = await self.db.execute(stmt)

        users = result.scalars().all()
        
        return await query_manager.QueryManager.build_response(users, page, limit, total)
    
    async def create(self, obj) -> TModel:
        # Convert dict/Pydantic → ORM model
        if not isinstance(obj, self.model):
            if isinstance(obj, dict):
                obj = self.model(**obj)
            elif hasattr(obj, "model_dump"):
                obj = self.model(**obj.model_dump())
            elif hasattr(obj, "dict"):
                obj = self.model(**obj.dict())
            else:
                raise TypeError("Invalid type for create()")

        self.db.add(obj)
        await self.db.commit()
        await self.db.refresh(obj)

        return obj
    
    async def update(self, entity_id: str, data: dict) -> TModel:
        instance = await self.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
        
        for field, value in data.items():
            if hasattr(instance, field):
                setattr(instance, field, value)
                
        if hasattr(instance, "updated_at"):
            instance.updated_at = datetime.now(timezone.utc)
            
        await self.db.commit()
        await self.db.refresh(instance)
        
        return instance
    
    async def soft_delete(self, entity_id: str, soft: bool = False) -> TModel | None:
        instance = await self.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
            
        if soft and hasattr(instance, "deleted_at"):
            instance.deleted_at = datetime.now(timezone.utc)
        else:
            self.db.delete(instance)
            
        await self.db.commit()
        
        return instance
    
    async def delete(self, entity_id: str) -> TModel:
        instance = await self.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found"
            )
            
        await self.db.delete(instance)
        await self.db.flush()
        
        return instance
        