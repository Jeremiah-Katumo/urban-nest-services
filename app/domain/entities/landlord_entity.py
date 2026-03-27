from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from ..enums.landlord_enum import LandlordStatus
from ..enums.user_enum import UserRoles


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
    user_id: Optional[str] 
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
    