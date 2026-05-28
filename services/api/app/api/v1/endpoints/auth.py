from __future__ import annotations

from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.models.user import User

router = APIRouter()

# ── JWT helpers ──────────────────────────────────────────────────────────────

def _jwt_secret() -> str:
    from app.config import settings
    return settings.jwt_secret

def create_token(user_id: int, email: str, role: str, expires_hours: int = 24 * 30) -> str:
    from jose import jwt
    payload = {
        "sub": str(user_id),
        "email": email,
        "role": role,
        "exp": datetime.utcnow() + timedelta(hours=expires_hours),
    }
    return jwt.encode(payload, _jwt_secret(), algorithm="HS256")

def decode_token(token: str) -> dict:
    from jose import jwt, JWTError
    try:
        return jwt.decode(token, _jwt_secret(), algorithms=["HS256"])
    except JWTError as e:
        raise ValueError(str(e))

def hash_password(password: str) -> str:
    import hashlib, os
    salt = os.urandom(16).hex()
    hashed = hashlib.sha256(f"{salt}{password}".encode()).hexdigest()
    return f"{salt}:{hashed}"

def verify_password(password: str, hashed: str) -> bool:
    import hashlib
    try:
        salt, h = hashed.split(":", 1)
        return hashlib.sha256(f"{salt}{password}".encode()).hexdigest() == h
    except Exception:
        return False

# ── DB session dep ────────────────────────────────────────────────────────────

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session

# ── Auth dep ──────────────────────────────────────────────────────────────────

async def get_current_user(
    authorization: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> User:
    from fastapi import Header
    raise HTTPException(status_code=401, detail="Not implemented as dep — use _resolve_user")

async def _resolve_user(token: str, db: AsyncSession) -> User:
    try:
        payload = decode_token(token)
        user_id = int(payload["sub"])
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or inactive")
    return user

# ── Schemas ───────────────────────────────────────────────────────────────────

class RegisterRequest(BaseModel):
    email: str
    password: str
    display_name: Optional[str] = None
    role: Optional[str] = "user"  # user | vendor | superadmin

class LoginRequest(BaseModel):
    email: str
    password: str

class UpdateProfileRequest(BaseModel):
    display_name: Optional[str] = None
    partner_name: Optional[str] = None
    wedding_date: Optional[str] = None
    city: Optional[str] = None
    budget: Optional[int] = None

class UserResponse(BaseModel):
    id: int
    email: str
    display_name: Optional[str]
    role: str
    partner_name: Optional[str]
    wedding_date: Optional[str]
    city: Optional[str]
    budget: Optional[int]

    class Config:
        from_attributes = True

# ── Endpoints ─────────────────────────────────────────────────────────────────

@router.post("/register", response_model=dict)
async def register(body: RegisterRequest, db: AsyncSession = Depends(get_db)):
    # Check duplicate
    result = await db.execute(select(User).where(User.email == body.email.lower()))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Email already registered")

    role = body.role if body.role in ("user", "vendor", "superadmin") else "user"
    user = User(
        email=body.email.lower(),
        hashed_password=hash_password(body.password),
        display_name=body.display_name,
        role=role,
        is_active=True,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    token = create_token(user.id, user.email, user.role)
    return {"token": token, "user": UserResponse.from_orm(user).dict()}


@router.post("/login", response_model=dict)
async def login(body: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == body.email.lower()))
    user = result.scalar_one_or_none()
    if not user or not verify_password(body.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account deactivated")

    token = create_token(user.id, user.email, user.role)
    return {"token": token, "user": UserResponse.from_orm(user).dict()}


@router.get("/me", response_model=UserResponse)
async def me(authorization: str = "", db: AsyncSession = Depends(get_db)):
    from fastapi import Request
    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    user = await _resolve_user(token, db)
    return UserResponse.from_orm(user)


@router.patch("/me", response_model=UserResponse)
async def update_me(
    body: UpdateProfileRequest,
    authorization: str = "",
    db: AsyncSession = Depends(get_db),
):
    token = authorization.replace("Bearer ", "").strip()
    if not token:
        raise HTTPException(status_code=401, detail="Missing token")
    user = await _resolve_user(token, db)

    if body.display_name is not None:
        user.display_name = body.display_name
    if body.partner_name is not None:
        user.partner_name = body.partner_name
    if body.wedding_date is not None:
        user.wedding_date = body.wedding_date
    if body.city is not None:
        user.city = body.city
    if body.budget is not None:
        user.budget = body.budget

    await db.commit()
    await db.refresh(user)
    return UserResponse.from_orm(user)
