from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict
from ..enums.agent_enum import AgentStatus
from ..enums.user_enum import UserRoles
from .user_entity import UserRead


class AgentBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    status: Optional[AgentStatus] = AgentStatus.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    user_id: Optional[str] 
    
    
class AgentCreate(AgentBase):
    pass


class AgentUpdate(AgentBase):
    id: str
    
    
class AgentRead(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    status: Optional[AgentStatus] = AgentStatus.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    entity_id: Optional[str] 
    entity: Optional[Dict[str, str]]
    user: Optional[UserRead]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        
        
class AgentPaginationList(BaseModel):
    items: Optional[List[AgentRead]]
    page: int
    total: int
    pages: int
    page_size: int
    