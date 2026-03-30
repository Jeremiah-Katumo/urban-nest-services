from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class ValueBase(BaseModel):
    module: str
    entity_id: str
    field_id: str
    value: Any
    
    
class ValueCreate(ValueBase):
    pass


class ValueUpdate(ValueBase):
    pass


class ValueRead(ValueBase):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_atrributes=True
        
        
class ValuePaginationList(BaseModel):
    items: Optional[List[ValueRead]]
    page: int
    total: int
    pages: int
    page_size: int