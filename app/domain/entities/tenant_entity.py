from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional, List
from ..enums.tenant_enum import TenantStatus
from ..enums.user_enum import UserRoles


class TenantBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    status: Optional[TenantStatus] = TenantStatus.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    user_id: Optional[str] 


class TenantCreate(TenantBase):
    pass


class TenantUpdate(TenantBase):
    id: str


class TenantRead(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    status: Optional[TenantStatus] = TenantStatus.ACTIVE
    role: Optional[UserRoles] = UserRoles.CUSTOMER
    user_id: Optional[str] 
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
    class Config:
        from_attributes = True


class TenantPaginationList(BaseModel):
    items: Optional[List[TenantRead]]
    page: int
    total: int
    pages: int
    page_size: int
