from fastapi import FastAPI
from app.core.config import settings
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from app.models.user_model import User
from app.api.api_v1.router import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="FarmToDo is a task management system for farmers",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

@app.on_event("startup")
async def app_init():
    db_client = AsyncIOMotorClient(settings.MONGO_CONNECTION_STRING)
    db = db_client[settings.DATABASE_NAME]

    await init_beanie(
        database=db,
        document_models=[User]
    )

app.include_router(router, prefix=settings.API_V1_STR)