from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.endpoints import auth, chat, search, wedding
from app.db.base import Base
from app.db.session import engine
from app import models  # noqa: F401 - ensure all models are registered


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create all DB tables on startup
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("DB tables created/verified OK")
    except Exception as e:
        print("DB init error:", e)
    yield


app = FastAPI(
    title="VoyagerAgent API",
    version="0.1.0",
    lifespan=lifespan,
    debug=True,
)

# Explicit OPTIONS handler to bypass Traefik CORS stripping
@app.options("/{rest_of_path:path}")
async def preflight_handler(request: Request, rest_of_path: str):
    return JSONResponse(
        content={},
        headers={
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS, PATCH",
            "Access-Control-Allow-Headers": "*",
            "Access-Control-Max-Age": "86400",
        },
    )

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(search.router, prefix="/api/v1/search", tags=["search"])
app.include_router(wedding.router, prefix="/api/v1/wedding", tags=["wedding"])


@app.get("/health")
async def health():
    return {"status": "ok"}
