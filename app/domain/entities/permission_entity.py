from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PermissionBase(BaseModel):
    name: str
    description: str
    
class PermissionCreate(PermissionBase):
    pass 

class PermissionUpdate(PermissionBase):
    id: str
    
class PermissionRead(BaseModel):
    id: str
    name: str
    description: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        
class PermissionPaginationList(BaseModel):
    items: Optional[List[PermissionRead]]
    page: int
    total: int
    pages: int
    page_size: int

