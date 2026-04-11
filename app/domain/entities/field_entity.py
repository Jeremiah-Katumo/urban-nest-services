from pydantic import BaseModel
from typing import Optional, List, Any
from datetime import datetime


class FieldBase(BaseModel):
    module: str
    feature_id: Optional[str]
    name: str
    key: str
    type: str
    options: Optional[List[Any]] = None
    required: bool = False
    

class FieldCreate(FieldBase):
    pass 


class FieldUpdate(FieldBase):
    pass


class FieldRead(FieldBase):
    id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes=True
        
        
class FieldPaginationList(BaseModel):
    items: Optional[List[FieldRead]]
    page: int
    total: int
    pages: int
    page_size: int
    