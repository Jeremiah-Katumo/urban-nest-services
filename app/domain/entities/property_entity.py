from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime
from ..enums.house_enum import HouseStatus


class PropertyBase(BaseModel):
    title: str = Field(..., max_length=100)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=50)
    price: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    images: Optional[List[Any]] = None
    amenities: Optional[List[Any]] = None
    is_available: Optional[HouseStatus] = HouseStatus.AVAILABLE
    
    
class PropertyCreate(PropertyBase):
    landlord_id: str
    agent_id: Optional[str] = None
    
    
class PropertyUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    location: Optional[str] = Field(None, max_length=50)
    price: Optional[int] = None
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    images: Optional[List[Any]] = None
    amenities: Optional[List[Any]] = None
    is_available: Optional[HouseStatus] = None
    agent_id: Optional[str] = None
    
    
class PropertyRead(PropertyBase):
    id: str
    landlord_id: str
    agent_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True
        
        
class PropertyPaginationList(BaseModel):
    items: Optional[List[PropertyRead]]
    page: int
    total: int
    pages: int
    page_size: int