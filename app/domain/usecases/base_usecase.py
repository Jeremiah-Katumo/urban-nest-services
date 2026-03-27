from typing import Generic, TypeVar, Optional, Any, Dict
from fastapi import HTTPException, status

TModel = TypeVar("TModel")
TCreate = TypeVar("TCreate")
TUpdate = TypeVar("TUpdate")

class BaseUseCase(Generic[TModel, TCreate, TUpdate]):
    def __init__(self, repo):
        self.repo = repo

    # Hooks (Override in child)        
    async def before_create(self, data: Dict) -> Dict:
        return data
    
    async def before_update(self, instance: TModel, data: Dict) -> Dict:
        return data
    
    async def before_delete(self, instance: TModel) -> None:
        return None
    
    async def after_create(self, instance: TModel) -> TModel:
        return instance
    
    async def after_update(self, instance: TModel) -> TModel:
        return instance
    
    # Core Methods
    async def get_by_id(self, entity_id: str) -> TModel:
        instance = await self.repo.get_by_id(entity_id)
        if not instance:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Resource not found"
            )
        return instance
    
    async def get_all(
        self,
        page: int = 1,
        limit: int = 10,
        columns: Optional[str] = None,
        search_filter: Optional[str] = None,
        sort: Optional[str] = None,
    ):
        # GuardRails
        if page < 1:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Page must be >= 1"
            )
            
        if limit < 1 or limit > 100:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Limit must be between 1 and 100"
            )
            
        return await self.repo.get_all(page, limit, columns, search_filter, sort)
    
    async def create(self, data: TCreate) -> TModel:
        payload = data.dict() if hasattr(data, "dict") else data
        
        payload = await self.before_create(data)
        
        instance = await self.repo.add(payload)
        
        return await self.after_create(instance)
    
    async def update(self, entity_id: str, data: TUpdate) -> TModel:
        instance = await self.get_by_id(entity_id)
        
        payload = data.dict(exclude_unset=True) if hasattr(data, "dict") else data
        
        payload = await self.before_update(instance, payload)
        
        updated = await self.repo.update(entity_id, payload)
        
        return await self.after_update(updated)
    
    async def delete(self, entity_id: str, soft: bool = True) -> None:
        instance = await self.get_by_id(entity_id)
        
        await self.before_delete(instance)
        
        return await self.repo.soft_delete(entity_id, soft)
    