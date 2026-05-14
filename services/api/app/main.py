import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.endpoints import chat, auth, search


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Run DB migrations on startup
    try:
        result = subprocess.run(
            ["alembic", "upgrade", "head"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode != 0:
            print("Migration warning:", result.stderr)
        else:
            print("Migrations OK:", result.stdout)
    except Exception as e:
        print("Migration error:", e)
    yield


app = FastAPI(
    title="VoyagerAgent API",
    version="0.1.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
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
