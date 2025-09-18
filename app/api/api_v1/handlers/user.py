from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserAuth, UserAuthResponse
from app.services.user_service import UserService
import pymongo

users_router = APIRouter()
#I think we need tokens here but lets just fnish the tutoiral and see 
@users_router.post("/create", summary="Create a new user")
async def create_user(user: UserAuth) -> UserAuthResponse:
    try:
        return await UserService.create_user(user)
    except pymongo.errors.DuplicateKeyError:
        raise HTTPException(status_code=400, detail="User already exists")