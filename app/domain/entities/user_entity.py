from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from ..enums.user_enum import UserStatus, UserRoles


class UserBase(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: UserStatus
    role: UserRoles
    
class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: UserStatus

class UserRead(BaseModel):
    id: str
    username: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: UserStatus
    role: UserRoles
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    
class UserPaginationList(BaseModel):
    items: Optional[List[UserRead]]
    page: int
    total: int
    pages: int
    page_size: int