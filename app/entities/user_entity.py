from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
from ..enums.user_enum import UserStatus, UserRoles


class UserBase(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: UserStatus
    role: UserRoles
    
class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass 

class UserRead(BaseModel):
    id: str
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    status: UserStatus
    role: UserRoles
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    deleted_at: Optional[datetime]
    