from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field

class UserAuth(BaseModel):
    email: EmailStr = Field(..., description="User's email")
    username: str = Field(..., min_length=5, max_length=50, description="User's username")
    password: str = Field(..., min_length=5, max_length=24,description="User's password")

class UserAuthResponse(BaseModel):
    user_id: UUID = Field(..., description="User's id")
    email: EmailStr = Field(..., description="User's email")
    username: str = Field(..., min_length=5, max_length=50, description="User's username")
    created_at: datetime = Field(..., description="User's creation date")
    updated_at: datetime = Field(..., description="User's last update date")
