from pydantic_settings import BaseSettings
from pydantic import HttpUrl, AnyHttpUrl
from decouple import config
from typing import List

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    JWT_SECRET_KEY: str = config("JWT_SECRET_KEY", cast=str)
    JWT_REFRESH_SECRET_KEY: str = config("JWT_REFRESH_SECRET_KEY", cast=str)
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRATION: int = 15
    REFRESH_TOKEN_EXPIRATION: int= 60 * 24 * 7

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    PROJECT_NAME: str = "FARMToDO"

    #database
    MONGO_CONNECTION_STRING: str = config("MONGO_CONNECTION_STRING", cast=str)
    DATABASE_NAME: str = config("DATABASE_NAME", default="farm_todo", cast=str)

    class Config:
        case_sensitive = True

settings = Settings()
