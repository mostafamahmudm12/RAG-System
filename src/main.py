from fastapi import FastAPI
from routes.base import base_router  # More explicit import
from routes.data import date_router # Ensure this is imported after base_router
from routes.nlp import nlp_router
from motor.motor_asyncio import AsyncIOMotorClient
from helpers.config import get_settings
from stores.llm.LLMProviderFactory import LLMProviderFactory
from stores.vectordb.VectorDBProviderFactory import VectorDBProviderFactory
app = FastAPI()


async def startup_span():
    settings = get_settings()
    app.mongodb_client = AsyncIOMotorClient(settings.MONGO_URL)
    app.mongodb = app.mongodb_client[settings.MONGO_DATABASE]

    LLM_Provider_Factory = LLMProviderFactory(config=settings)
    vectorDB_Provider_Factory = VectorDBProviderFactory(config=settings)

    # generation client
    app.generation_client = LLM_Provider_Factory.create(Provider=settings.GENERATION_BACKEND)
    app.generation_client.set_generate_model(model_id=settings.GENERATION_MODEL_ID)

    # embedding client
    app.embedding_client = LLM_Provider_Factory.create(Provider=settings.EMBEDDING_BACKEND)
    app.embedding_client.set_embedding_model(model_id=settings.EMBEDDING_MODEL_ID,embedding_size=settings.EMBEDDING_MODEL_SIZE)

    # vector database client
    app.vectordb_client = vectorDB_Provider_Factory.create(
        Provider=settings.VECTOR_DB_BACKEND)
    
    app.vectordb_client.connect()

async def shutdown_span():
    app.mongodb_client.close()
    app.vectordb_client.disconnect()

# app.router.lifespan.on_startup.append(startup_span)
# app.router.lifespan.on_shutdown.append(shutdown_span)
app.on_event("startup")(startup_span)
app.on_event("shutdown")(shutdown_span)

app.include_router(base_router)
app.include_router(date_router)  # Ensure this is included after the base router
app.include_router(nlp_router)  # Ensure this is included after the base router