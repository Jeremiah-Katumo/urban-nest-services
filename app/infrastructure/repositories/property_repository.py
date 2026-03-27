from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession 
from sqlalchemy import select 
from datetime import datetime, timezone
from .base_repository import BaseRepository
from ...models.models import PropertyModel 
from ...domain.interfaces.property_interface import IProperty
from ...domain.entities.property_entity import PropertyCreate


class PropertyRepository(BaseRepository[PropertyModel], IProperty):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, PropertyModel)
        
    async def _assign_field(self, property_id: str, field: str, value: str):
        result = await self.db.execute(
            select(self.model).where(
                self.model.id == property_id,
                self.model.deleted_at.is_(None)
            )
        )
        prop = result.scalar_one_or_none()

        if not prop:
            return None

        setattr(prop, field, value)
        prop.updated_at = datetime.now(timezone.utc)

        await self.db.commit()
        await self.db.refresh(prop)

        return prop

    async def assign_landlord(self, property_id: str, landlord_id: str):
        return await self._assign_field(property_id, "landlord_id", landlord_id)

    async def assign_agent(self, property_id: str, agent_id: str):
        return await self._assign_field(property_id, "agent_id", agent_id)