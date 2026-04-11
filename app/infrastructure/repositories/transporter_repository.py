from sqlalchemy.ext.asyncio import AsyncSession 
from .base_repository import BaseRepository
from ...models.models import TransporterModel 
from ...domain.interfaces.transporter_interface import ITransporter


class TransporterRepository(BaseRepository[TransporterModel], ITransporter):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, TransporterModel)
        