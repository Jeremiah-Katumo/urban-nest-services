from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ...models.models import SubscriptionModel
from ...domain.interfaces.subscription_interface import ISubscription



class SubscriptionRepository(BaseRepository[SubscriptionModel], ISubscription):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, SubscriptionModel)