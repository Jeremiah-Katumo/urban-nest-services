from sqlalchemy.ext.asyncio import AsyncSession 
from .base_repository import BaseRepository
from ...models.models import TenantModel 
from ...domain.interfaces.tenant_interface import ITenant


class TenantRepository(BaseRepository[TenantModel], ITenant):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, TenantModel)
        