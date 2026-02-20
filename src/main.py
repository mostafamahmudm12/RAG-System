from fastapi import FastAPI
from routes.base import base_router  # More explicit import
from routes.data import date_router # Ensure this is imported after base_router
app = FastAPI()
app.include_router(base_router)
app.include_router(date_router)  # Ensure this is included after the base router