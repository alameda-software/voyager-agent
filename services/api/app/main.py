from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import chat, auth, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: init DB pool, Redis, etc.
    yield
    # Shutdown: close connections
    pass


app = FastAPI(
    title="VoyagerAgent API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8081",
        "http://127.0.0.1:8081",
        "http://localhost:19006",
        "http://127.0.0.1:19006",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])


@app.get("/health")
async def health():
    return {"status": "ok"}
