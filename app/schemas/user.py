from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    phone_number: Optional[str]
    gender: Optional[str]
    date_of_birth: Optional[datetime]
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: dict

class UserResponse(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    email: EmailStr
    is_active: bool
    created_date: datetime
    modified_date: datetime
    class Config:
        from_attributes = True