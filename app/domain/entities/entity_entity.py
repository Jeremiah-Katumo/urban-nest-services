from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from datetime import datetime
from ..enums import entity_enum, base_enum


class EntityBase(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = None
    email: Optional[EmailStr] = None
    currency: Optional[entity_enum.CurrencyEnum] = None
    status: base_enum.BaseStatus = base_enum.BaseStatus.ACTIVE
    logo_url: Optional[str] = None
    website_url: Optional[str] = None
    entity_heading: Optional[str] = Field(None, max_length=255)
    hero_section: Optional[dict] = None  # JSON field for hero section content
    about: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    motto: Optional[str] = Field(None, max_length=255)
    contacts: Optional[dict] = None  # JSON field for contact information
    footer: Optional[dict] = None  # JSON field for footer content
    
    
class EntityCreate(EntityBase):
    pass


class EntityUpdate(EntityBase):
    name: Optional[str] = Field(None, max_length=255)
    description: Optional[str] = Field(None, max_length=255)
    email: Optional[EmailStr] = Field(None, max_length=255)
    currency: Optional[entity_enum.CurrencyEnum] = Field(None)
    status: base_enum.BaseStatus = base_enum.BaseStatus.ACTIVE
    logo_url: Optional[str] = Field(None, max_length=255)
    website_url: Optional[str] = Field(None, max_length=255)
    entity_heading: Optional[str] = Field(None, max_length=255)
    hero_section: Optional[dict] = None  # JSON field for hero section content
    about: Optional[str] = None
    mission: Optional[str] = None
    vision: Optional[str] = None
    motto: Optional[str] = Field(None, max_length=255)
    contacts: Optional[dict] = None  # JSON field for contact information
    footer: Optional[dict] = None  # JSON field for footer content
    
    
class EntityRead(EntityBase):
    id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    deleted_at: Optional[datetime] = None
    
    class Config:
        orm_mode = True
        
        
class EntityPaginationList(BaseModel):
    items: Optional[List[EntityRead]]
    page: int
    total: int
    pages: int
    page_size: int