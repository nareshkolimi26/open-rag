from fastapi import FastAPI
from app.api.ingest import router as ingest_router
from app.api.query import router as query_router
from app.vectorstore.qdrant_client import create_collection
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    create_collection()
    print("openrag started successfully")
    yield
    # Shutdown (if needed)

app = FastAPI(title="OpenRAG", lifespan=lifespan)

@app.get("/")
def root():
    return {"message":"openrag is running"}

app.include_router(ingest_router)
app.include_router(query_router)