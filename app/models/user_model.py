from beanie import Document, Indexed
from pydantic import EmailStr, Field
from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime, timezone

class User(Document):
    user_id: UUID = Field(default_factory=uuid4)
    username: str = Indexed(str, unique=True)
    email: EmailStr = Indexed(EmailStr, unique=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)
    is_verified: bool = Field(default=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    def before_save(self):
        now = datetime.now(timezone.utc)
        if not self.created_at:
            self.created_at = now
        self.updated_at = now

    def __repr__(self):
        return f"<User {self.email}>"

    def __str__(self):
        return self.email

    def __hash__(self):
        return hash(self.email)
    
    def __eq__(self, other):
        if isinstance(other, User):
            return self.email == other.email
        return False

    @classmethod
    async def by_email(cls, email: EmailStr):
        return await cls.find_one(cls.email == email)
    
    @classmethod
    async def by_user_id(cls, user_id: UUID):
        return await cls.find_one(cls.user_id == user_id)
    
    class Settings:
        name = "users"
        
        