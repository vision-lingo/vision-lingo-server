from contextlib import asynccontextmanager
from fastapi import FastAPI

from app.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="Vision Lingo Server",
    description="API for vision lingo training metrics",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(api_router, prefix="/api")


@app.get("/")
async def root():
    return {"message": "Vision Lingo Server"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
