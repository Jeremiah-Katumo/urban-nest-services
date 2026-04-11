from .base_usecase import BaseUseCase


class SupportTicketUseCase(BaseUseCase):
    
    async def ai_support(self, session_id: str, role: str, user_id: str, query: str):
        return self.ai_support(session_id, role, user_id, query)