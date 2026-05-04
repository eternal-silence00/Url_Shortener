from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import url
from app.database import engine 
from app.models.url import Url, Base


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    await engine.dispose()
    
app = FastAPI(lifespan=lifespan)

app.include_router(url.router)
    
    