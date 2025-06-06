from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict
from sqlmodel import Field, SQLModel
from datetime import datetime
class UserBase(BaseModel):
    email: EmailStr = Field(max_length=255) 
class UserCreate(UserBase):
    password: str = Field(min_length=8)

class UserLogin(BaseModel):
    email: EmailStr
    password: str
class UserUpdate(UserBase):
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_superuser: Optional[bool] = None
class UserResponse(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True, json_schema_extra={
        "example": {
            "id": 1,
            "email": "user@example.com",
            "is_active": True,
            "is_superuser": False,
            "created_at": "2025-05-28T10:00:00.000Z",
            "updated_at": "2025-05-28T10:00:00.000Z",
        }
    })
class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

    model_config = ConfigDict(json_schema_extra={
        "example": {
            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
            "token_type": "bearer",
        }
    })
class TokenPayload(BaseModel):
    sub: Optional[int] = None