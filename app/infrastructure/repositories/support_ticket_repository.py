from sqlalchemy.ext.asyncio import AsyncSession
from .base_repository import BaseRepository
from ...models.models import SupportTicketModel
from ...domain.interfaces.support_ticket_interface import ISupportTicket
from ..services.ai_support_service import AISupportService, AISupportServiceAdvanced
from ..services.ticket_service import TicketService
from ...domain.entities.support_ticket_entity import AISupportTicketRead


class SupportTicketRepository(BaseRepository[SupportTicketModel], ISupportTicket):
    
    def __init__(self, db_session: AsyncSession):
        super().__init__(db_session, SupportTicketModel)
        self.ai_support_service = AISupportService()
        self.ticket_service = TicketService()
        self.ai_support_service_advanced = AISupportServiceAdvanced()
        
    async def ai_support(self, session_id: str, role: str, user_id: str, query: str):
        response = self.ai_support_service.ask(session_id, role, query)
        
        recommendations = self.ai_support_service_advanced.get_recommended_properties(query)

        ticket_created = False
        if self.ticket_service.should_create_ticket(response):
            category = self.ticket_service.categorize_issue(query)

            ticket = SupportTicketModel(
                user_id=user_id,
                role=role,
                title="Auto-generated issue",
                description=query,
                category=category
            )

            self.repo.create(ticket)
            
            ticket_created = True

            return AISupportTicketRead(
                ai_response=response,
                recommendations=recommendations,
                ticket_created=ticket_created
            )

        return AISupportTicketRead(
            ai_response=response,
            recommendations=recommendations,
            ticket_created=ticket_created   
        )