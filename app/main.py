from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routes.agent import router as agent_router
from app.config.database import Base, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield 

app = FastAPI(
    title="RAG Agent",
    lifespan=lifespan
)

app.include_router(agent_router, prefix='/v1')
