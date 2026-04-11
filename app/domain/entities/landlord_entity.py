from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict
from ..enums.landlord_enum import LandlordStatus
from ..enums.user_enum import UserRoles
from .property_entity import PropertyRead
from .user_entity import UserRead


class LandlordBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    status: Optional[LandlordStatus] = LandlordStatus.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    user_id: Optional[str] 
    
    
class LandlordCreate(LandlordBase):
    pass


class LandlordUpdate(LandlordBase):
    id: str
    
    
class LandlordRead(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    status: Optional[LandlordStatus] = LandlordStatus.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    entity_id: Optional[str] 
    entity: Optional[Dict[str, str]]
    properties: Optional[List[PropertyRead]]
    user: Optional[UserRead]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True
        
        
class LandlordPaginationList(BaseModel):
    items: Optional[List[LandlordRead]]
    page: int
    total: int
    pages: int
    page_size: int
    