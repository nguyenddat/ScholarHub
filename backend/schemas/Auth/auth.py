from typing import *
from datetime import datetime

from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

from helpers.Enums import UserRoleEnum

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    email: str
    password: str
    
class UserLogin(UserBase):
    password: str

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[str] = None

class UserResponse(UserBase):
    id: UUID
    role: UserRoleEnum
    avatar: Optional[str] = None
    banner: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class RefreshToken(BaseModel):
    refresh_token: str