from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class CampaignBase(BaseModel):
    title: str = Field(..., example="Summer Sale")
    content: Optional[str] = Field(None, example="Discounts on all properties for the summer season")
    sent_at: datetime = Field(..., example="2024-06-01T00:00:00Z")
    expires_at: datetime = Field(..., example="2024-08-31T23:59:59Z")
    status: str = Field(default="active", example="active")
    target_user_segment: Optional[str] = Field(None, example="All tenants in New York")
    entity_id: Optional[str] = Field(None, example="123e4567-e89b-12d3-a456-426614174000")  # For property-specific campaigns
    
    
class CampaignCreate(CampaignBase):
    pass

class CampaignUpdate(BaseModel):
    title: Optional[str] = Field(None, example="Summer Sale")
    content: Optional[str] = Field(None, example="Discounts on all properties for the summer season")
    sent_at: Optional[datetime] = Field(None, example="2024-06-01T00:00:00Z")
    expires_at: Optional[datetime] = Field(None, example="2024-08-31T23:59:59Z")
    status: Optional[str] = Field(None, example="active")
    target_user_segment: Optional[str] = Field(None, example="All tenants in New York")
    entity_id: Optional[str] = Field(None, example="123e4567-e89b-12d3-a456-426614174000")  # For property-specific campaigns
    
    
class CampaignRead(CampaignBase):
    id: str = Field(..., example="123e4567-e89b-12d3-a456-426614174000")
    created_at: Optional[datetime] = Field(None, example="2024-06-01T00:00:00Z")
    updated_at: Optional[datetime] = Field(None, example="2024-06-01T00:00:00Z")
    deleted_at: Optional[datetime] = Field(None, example="2024-06-01T00:00:00Z")
    # entity: Optional[str] = Field(None, example="property")  # Indicates the type of entity the campaign is associated with (e.g., "property", "booking", etc.)
    
    
class CampaignPaginationList(BaseModel):
    items: Optional[List[CampaignRead]]
    page: int = Field(..., example=1)
    total: int = Field(..., example=100)
    pages: int = Field(..., example=10)
    page_size: int = Field(..., example=10)