from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List 
from ..enums.user_enum import UserRoles
from ..enums.support_ticket_enum import TicketCategory, TicketStatus


class SupportTicketBase(BaseModel):
    user_id: Optional[str]
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    title: str
    description: str
    category: Optional[TicketCategory] = TicketCategory.OTHER
    status: Optional[TicketStatus] = TicketStatus.OPEN
    user_id: Optional[str] 


class SupportTicketCreate(SupportTicketBase):
    pass


class SupportTicketUpdate(SupportTicketBase):
    id: str


class SupportTicketRead(SupportTicketBase):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class SupportTicketPaginationList(BaseModel):
    items: Optional[List[SupportTicketRead]]
    page: int
    total: int
    pages: int
    page_size: int


class AISupportTicketRead(BaseModel):
    ai_response: str
    recommendations: List[str]
    ticket_created: bool