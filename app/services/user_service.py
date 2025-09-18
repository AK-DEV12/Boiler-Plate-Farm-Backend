from typing import Optional
from app.schemas.user_schema import UserAuth
from app.models.user_model import User
from app.core.security import get_password_hash, verify_password

class UserService:
    @staticmethod
    async def create_user(user: UserAuth):
        newUser = User(
            username=user.username,
            email=user.email,
            hashed_password=get_password_hash(user.password)
        )
        await newUser.save()
        return newUser
    
    @staticmethod
    async def authenticate(email: str, password: str) -> Optional[User]:
        user = await User.by_email(email)
        if not user or not verify_password(password, user.hashed_password):
            return False
        return user