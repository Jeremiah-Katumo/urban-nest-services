from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional


class SubscriptionBase(BaseModel):
    name: str
    price: int
    interval: str
    role: str
    description: str
    features: List[str]
    
    
class SubscriptionCreate(SubscriptionBase):
    pass


class SubscriptionUpdate(BaseModel):
    pass


class SubscriptionRead(SubscriptionBase):
    id: str
    deleted_at: Optional[datetime]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        
        
class SubscriptionPaginationList(BaseModel):
    items: Optional[List[SubscriptionRead]]
    page: int
    total: int
    pages: int
    page_size: int