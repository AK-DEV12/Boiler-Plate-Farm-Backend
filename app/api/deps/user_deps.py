from datetime import datetime, timezone
from app.models.user_model import User
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings
from jose import jwt
from app.schemas.auth_schema import TokenPayload
from pydantic import ValidationError

reusable_oauth = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/auth/login", scheme_name="JWT")

async def get_current_user(token: str = Depends(reusable_oauth)) -> User:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.ALGORITHM])
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now(timezone.utc):
            raise HTTPException(status_code=401, detail="Token expired", headers={"WWW-Authenticate": "Bearer"})
    except(jwt.JWTError, ValidationError):
        raise HTTPException(status_code=403, detail="Invalid token", headers={"WWW-Authenticate": "Bearer"})
    
    user = await User.by_user_id(token_data.sub)

    if not user:
        raise HTTPException(status_code=404, detail="User not found", headers={"WWW-Authenticate": "Bearer"})
    
    return user