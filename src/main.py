from fastapi import FastAPI
from src.routers import query_router

app = FastAPI()

app.include_router(query_router.router)