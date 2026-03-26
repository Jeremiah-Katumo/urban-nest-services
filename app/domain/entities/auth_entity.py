from pydantic import BaseModel, EmailStr
from ..enums.user_enum import UserRoles


class RegisterSchema(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    phone: str
    password: str
    role: UserRoles  # tenant / landlord / agent


class LoginSchema(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str