from fastapi import FastAPI
from routes.base import base_router  # More explicit import
from routes.data import date_router # Ensure this is imported after base_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
app = FastAPI()


async def startup_db_client():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DATABASE]

    LLM_Provider_Factory = LLMProviderFactory(config=settings)

    # generation client
    app.generation_client = LLM_Provider_Factory.create(Provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generate_model(model_id=settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = LLM_Provider_Factory.create(Provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBEDDING_MODEL_SIZE)

async def shutdown_db_client():
    app.mongodb_client.close()

app.router.lifespan.on_startup.append(startup_db_client)
app.router.lifespan.on_shutdown.append(shutdown_db_client)
app.include_router(base_router)
app.include_router(date_router)  # Ensure this is included after the base router
