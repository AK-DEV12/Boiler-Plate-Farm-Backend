from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserAuth, UserAuthResponse
from app.services.user_service import UserService
import pymongo

users_router = APIRouter()
#I think we need tokens here but lets just fnish the tutoiral and see 
@users_router.post("/create", summary="Create a new user")
async def create_user(user: UserAuth) -> UserAuthResponse:
    try:
        created_user = await UserService.create_user(user)
        
        # Generate tokens for the new user
        access_token = create_access_token(created_user.user_id, settings.ACCESS_TOKEN_EXPIRATION)
        refresh_token = create_refresh_token(created_user.user_id, settings.REFRESH_TOKEN_EXPIRATION)
        
        return {
            "user": UserAuthResponse(
                user_id=created_user.user_id,
                email=created_user.email,
                username=created_user.username,
                created_at=created_user.created_at,
                updated_at=created_user.updated_at
            ),
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")