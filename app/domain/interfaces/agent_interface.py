from abc import ABC, abstractmethod
from ..entities.agent_entity import AgentUpdate, AgentRead, AgentCreate


class IAgent(ABC):
    @abstractmethod
    async def create(self, data: AgentCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> AgentRead:
        raise NotImplementedError
    
    @abstractmethod
    async def get_all(
        self,
        page: int,
        limit: int,
        columns: str | None,
        search_filter: str | None,
        sort: str | None,
    ):
        raise NotImplementedError
    
    @abstractmethod
    async def update(self, id: str, data: AgentUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
