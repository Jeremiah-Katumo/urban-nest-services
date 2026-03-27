from sqlalchemy.ext.asyncio import AsyncSession 
from .base_repository import BaseRepository
from ...models.models import AgentModel 
from ...domain.interfaces.agent_interface import IAgent


class AgentRepository(BaseRepository[AgentModel], IAgent):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, AgentModel)
