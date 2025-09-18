from jose import jwt
from app.core.config import settings
from app.core.security import create_access_token, create_refresh_token
from app.schemas.auth_schema import TokenSchema
from app.api.deps.user_deps import get_current_user
from app.models.user_model import User
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends, HTTPException, APIRouter, Body
from app.services.user_service import UserService
from app.schemas.user_schema import UserAuthResponse
from pydantic import ValidationError
from app.schemas.auth_schema import TokenPayload

auth_router = APIRouter()

@auth_router.post("/login", summary="Login for access token and refresh token", response_model=TokenSchema)
async def login(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    user = await UserService.authenticate(email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    

    access_token = create_access_token(user.user_id, settings.ACCESS_TOKEN_EXPIRATION)
    refresh_token = create_refresh_token(user.user_id, settings.REFRESH_TOKEN_EXPIRATION)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }

@auth_router.post("/refresh-token", summary="Refresh token", response_model=TokenSchema)
async def refresh_token(refresh_token: str = Body(...)) -> dict:
    try:
        payload = jwt.decode(refresh_token, settings.JWT_REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)

    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    
    user = await User.by_user_id(token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    
    access_token = create_access_token(user.user_id, settings.ACCESS_TOKEN_EXPIRATION)
    refresh_token = create_refresh_token(user.user_id, settings.REFRESH_TOKEN_EXPIRATION)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token
    }