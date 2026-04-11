from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from .base_repository import BaseRepository
from ...domain.interfaces.field_interface import IField
from ...models.models import FieldModel


class FieldRepository(BaseRepository[FieldModel], IField):
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, FieldModel)
        
    async def get_all_by_module(self, module: str) -> List[FieldModel]:
        result = await self.db.execute(
            select(FieldModel).where(
                FieldModel.module == module,
                FieldModel.deleted_at.is_(None)
            )
        )
        return result.scalars().all()