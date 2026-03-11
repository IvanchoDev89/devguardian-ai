from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import HTTPBearer
from pydantic import BaseModel, EmailStr
from datetime import timedelta
from app.core.auth import (
    get_password_hash, verify_password, create_access_token, 
    create_refresh_token, decode_token, get_current_user, TokenData
)
from app.core.config import get_settings
from app.core.encryption import encrypt_value, decrypt_value
from app.core.audit import get_audit_logger

router = APIRouter(prefix="/api/auth", tags=["Authentication"])
settings = get_settings()
security = HTTPBearer()
audit = get_audit_logger()

SECRET_MASK = "***ENCRYPTED***"

users_db = {}


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class UserResponse(BaseModel):
    user_id: str
    email: str
    name: str
    role: str


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    if user.email in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    if len(user.password) < 8:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 8 characters"
        )
    
    user_id = f"user_{len(users_db) + 1}"
    hashed_password = get_password_hash(user.password)
    
    users_db[user.email] = {
        "user_id": user_id,
        "email": user.email,
        "name": user.name,
        "password": hashed_password,
        "password_encrypted": encrypt_value(hashed_password),
        "role": "user"
    }
    
    return UserResponse(
        user_id=user_id,
        email=user.email,
        name=user.name,
        role="user"
    )


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin, request: Request):
    client_ip = request.headers.get("x-forwarded-for", request.client.host if request.client else "unknown")
    
    user = users_db.get(credentials.email)
    
    if not user or not verify_password(credentials.password, user["password"]):
        audit.log_event(
            event_type="login",
            user_id=None,
            ip_address=client_ip,
            action="login",
            resource="/api/auth/login",
            success=False,
            metadata={"email": credentials.email}
        )
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    audit.log_event(
        event_type="login",
        user_id=user["user_id"],
        ip_address=client_ip,
        action="login",
        resource="/api/auth/login",
        success=True,
        metadata={"email": user["email"]}
    )
    
    access_token = create_access_token(
        data={"sub": user["user_id"], "email": user["email"], "role": user["role"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    refresh_token = create_refresh_token(
        data={"sub": user["user_id"], "email": user["email"]}
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(refresh_token: str):
    payload = decode_token(refresh_token)
    
    if payload is None or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )
    
    user_id = payload.get("sub")
    email = payload.get("email")
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    user = users_db.get(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    new_access_token = create_access_token(
        data={"sub": user["user_id"], "email": user["email"], "role": user["role"]},
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    new_refresh_token = create_refresh_token(
        data={"sub": user["user_id"], "email": user["email"]}
    )
    
    return Token(
        access_token=new_access_token,
        refresh_token=new_refresh_token
    )


@router.get("/me", response_model=UserResponse)
async def get_me(current_user: TokenData = Depends(get_current_user)):
    user = users_db.get(current_user.email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        user_id=user["user_id"],
        email=user["email"],
        name=user["name"],
        role=user["role"]
    )


def init_default_admin():
    if "admin@devguardian.ai" not in users_db:
        admin_password = get_password_hash("admin123")
        users_db["admin@devguardian.ai"] = {
            "user_id": "admin_1",
            "email": "admin@devguardian.ai",
            "name": "Admin",
            "password": admin_password,
            "password_encrypted": encrypt_value(admin_password),
            "role": "admin"
        }


init_default_admin()


@router.get("/audit")
async def get_audit_logs(
    limit: int = 50,
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    logs = audit.get_logs(limit=limit)
    return {"logs": logs, "total": len(logs)}


@router.get("/audit/suspicious")
async def get_suspicious_activity(
    current_user: TokenData = Depends(get_current_user)
):
    if current_user.role not in ["admin", "super_admin"]:
        raise HTTPException(status_code=403, detail="Admin access required")
    
    return audit.get_suspicious_activity()
