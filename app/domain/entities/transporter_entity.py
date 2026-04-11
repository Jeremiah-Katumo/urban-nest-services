from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List, Dict
from ..enums.base_enum import Status
from ..enums.user_enum import UserRoles
from ..enums.transporter_enum import DriverStatus
from .user_entity import UserRead


class TransporterBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    base_price: Optional[float]
    price_per_km: Optional[float]
    rating: Optional[float]
    driver_status: Optional[DriverStatus] = DriverStatus.AVAILABLE
    status: Optional[Status] = Status.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    user_id: Optional[str] 


class TransporterCreate(TransporterBase):
    pass


class TransporterUpdate(TransporterBase):
    id: str


class TransporterRead(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    base_price: Optional[float]
    price_per_km: Optional[float]
    rating: Optional[float]
    driver_status: Optional[DriverStatus] = DriverStatus.AVAILABLE
    status: Optional[Status] = Status.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    entity_id: Optional[str] 
    entity: Optional[Dict[str, str]]
    user: Optional[UserRead]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TransporterPaginationList(BaseModel):
    items: Optional[List[TransporterRead]]
    page: int
    total: int
    pages: int
    page_size: int
