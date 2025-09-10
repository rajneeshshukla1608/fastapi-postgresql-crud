from fastapi import FastAPI
from contextlib import asynccontextmanager

from .database import prisma
from .routers.items import router as items_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await prisma.connect()
    try:
        yield
    finally:
        await prisma.disconnect()


app = FastAPI(title="FastAPI + Prisma CRUD Service", lifespan=lifespan)

app.include_router(items_router, prefix="/items", tags=["items"]) 


@app.get("/healthz")
async def healthcheck():
    return {"status": "ok"} 