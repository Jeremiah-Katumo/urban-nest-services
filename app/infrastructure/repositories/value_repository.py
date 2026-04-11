from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from sqlalchemy import select
from .base_repository import BaseRepository
from ...domain.interfaces.value_interface import IValue
from ...models.models import ValueModel
from ...infrastructure.db.database import db


class ValueRepository(BaseRepository[ValueModel], IValue):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, ValueModel)
        
    async def get_by_entity(self, module: str, entity_id: str) -> List[ValueModel]:
        result = await self.db.execute(
            select(ValueModel).where(
                ValueModel.module == module, 
                ValueModel.entity_id == entity_id
            )
        )
        return result.scalars().all()
    
    
# value_repo = ValueRepository(db)
