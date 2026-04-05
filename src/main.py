from fastapi import FastAPI
from routes.base import base_router  # More explicit import
from routes.data import date_router # Ensure this is imported after base_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
app = FastAPI()

@app.on_event("startup")
async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DATABASE]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()

app.include_router(base_router)
app.include_router(date_router)  # Ensure this is included after the base router
