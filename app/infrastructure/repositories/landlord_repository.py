from sqlalchemy.ext.asyncio import AsyncSession 
from .base_repository import BaseRepository
from ...models.models import LandlordModel 
from ...domain.interfaces.landlord_interface import ILandlord


class LandlordRepository(BaseRepository[LandlordModel], ILandlord):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, LandlordModel)
