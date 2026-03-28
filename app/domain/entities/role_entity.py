from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class RoleBase(BaseModel):
    name: str
    description: str
    
class RoleCreate(RoleBase):
    pass 

class RoleUpdate(RoleBase):
    id: str
    
class RoleRead(BaseModel):
    id: str
    name: str
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        
class RolePaginationList(BaseModel):
    items: Optional[List[RoleRead]]
    page: int
    total: int
    pages: int
    page_size: int

