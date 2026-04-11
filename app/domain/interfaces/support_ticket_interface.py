from abc import ABC, abstractmethod
from ..entities.support_ticket_entity import SupportTicketCreate, SupportTicketRead, SupportTicketUpdate


class ISupportTicket(ABC):
    @abstractmethod
    async def create(self, data: SupportTicketCreate):
        raise NotImplementedError
    
    @abstractmethod
    async def get_by_id(self, id: str) -> SupportTicketRead:
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
    async def update(self, id: str, data: SupportTicketUpdate):
        raise NotImplementedError
    
    @abstractmethod
    async def soft_delete(self, id: str):
        raise NotImplementedError
    
    @abstractmethod
    async def ai_support(self, session_id: str, role: str, user_id: str, query: str):
        raise NotImplementedError
