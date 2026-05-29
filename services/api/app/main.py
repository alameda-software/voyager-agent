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
    # Create/migrate all tables using raw asyncpg for DDL reliability
    try:
        from app.config import settings
        import asyncpg
        # Use plain asyncpg for DDL (most reliable for ALTER TABLE)
        raw_url = settings.database_url.replace("postgresql+asyncpg://", "postgresql://")
        conn = await asyncpg.connect(raw_url)
        try:
            for sql in [
                """CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    email VARCHAR(255) UNIQUE NOT NULL,
                    hashed_password TEXT NOT NULL,
                    is_active BOOLEAN DEFAULT TRUE,
                    display_name VARCHAR(255),
                    role VARCHAR(50) NOT NULL DEFAULT 'user',
                    partner_name VARCHAR(255),
                    wedding_date VARCHAR(50),
                    city VARCHAR(255),
                    budget INTEGER
                )""",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) NOT NULL DEFAULT 'user'",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS partner_name VARCHAR(255)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS wedding_date VARCHAR(50)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS city VARCHAR(255)",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS budget INTEGER",
                "ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR(255)",
            ]:
                try:
                    await conn.execute(sql)
                except Exception as ex:
                    print(f"DDL skip: {ex}")
        finally:
            await conn.close()
        print("DB users table OK")
    except Exception as e:
        print("DB raw DDL error:", e)

    # Create all other tables via SQLAlchemy
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        print("DB create_all OK")
    except Exception as e:
        print("DB create_all error:", e)

    # Seed wedding vendors if table is empty
    try:
        from sqlalchemy import text, select, func
        from app.models.wedding import Vendor
        from app.db.session import AsyncSessionLocal
        import json
        from pathlib import Path

        vendors_path = Path(__file__).parent / "domains" / "wedding" / "data" / "vendors.json"
        if vendors_path.exists():
            data = json.loads(vendors_path.read_text(encoding="utf-8"))
            vendors_data = data.get("vendors", [])
            valid_cols = {c.key for c in Vendor.__table__.columns}

            async with AsyncSessionLocal() as session:
                result = await session.execute(select(func.count()).select_from(Vendor))
                count = result.scalar()

                if count != len(vendors_data):
                    await session.execute(text("DELETE FROM wedding_vendors"))
                    for vd in vendors_data:
                        filtered = {k: v for k, v in vd.items() if k in valid_cols}
                        filtered.pop("id", None)
                        session.add(Vendor(**filtered))
                    await session.commit()
                    print(f"Re-seeded {len(vendors_data)} wedding vendors (was {count})")
                else:
                    print(f"Wedding vendors up to date ({count} rows)")
    except Exception as e:
        print("Wedding vendor seed error:", e)

    # Seed test users
    try:
        from sqlalchemy import select
        from app.models.user import User
        from app.db.session import AsyncSessionLocal
        from app.api.v1.endpoints.auth import hash_password

        TEST_USERS = [
            {"email": "fer@gmail.com", "password": "123456", "display_name": "Fernando", "role": "superadmin"},
            {"email": "fer@g.com", "password": "123456", "display_name": "Fernando", "role": "superadmin"},
            {"email": "vendor@livegate.es", "password": "123456", "display_name": "Vendor Demo", "role": "vendor"},
            {"email": "demo@livegate.es", "password": "123456", "display_name": "Caterina & Francisco", "role": "user",
             "partner_name": "Francisco", "wedding_date": "2027-06-15", "city": "Sevilla"},
        ]

        async with AsyncSessionLocal() as session:
            for u in TEST_USERS:
                result = await session.execute(select(User).where(User.email == u["email"]))
                if not result.scalar_one_or_none():
                    user = User(
                        email=u["email"],
                        hashed_password=hash_password(u["password"]),
                        display_name=u.get("display_name"),
                        role=u["role"],
                        partner_name=u.get("partner_name"),
                        wedding_date=u.get("wedding_date"),
                        city=u.get("city"),
                        is_active=True,
                    )
                    session.add(user)
            await session.commit()
            print("Test users seeded OK")
    except Exception as e:
        print("Test user seed error:", e)

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
