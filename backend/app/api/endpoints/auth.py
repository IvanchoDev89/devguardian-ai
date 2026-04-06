from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr
from datetime import timedelta, datetime
from collections import defaultdict
import secrets
import hashlib
from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
    verify_token,
    get_current_user
)
from app.core.config import settings
from app.models.models import User, RefreshToken, PasswordResetToken
from app.models.schemas import UserCreate, UserResponse, Token, TokenResponse, RefreshTokenResponse

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

# Rate limiting
rate_limit_store = defaultdict(list)
RATE_LIMIT = 5
RATE_WINDOW = 60


def check_rate_limit(request: Request):
    client_ip = request.client.host if request.client else "unknown"
    now = datetime.utcnow()
    rate_limit_store[client_ip] = [
        t for t in rate_limit_store[client_ip]
        if (now - t).total_seconds() < RATE_WINDOW
    ]
    if len(rate_limit_store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    rate_limit_store[client_ip].append(now)


class EmailSchema(BaseModel):
    email: EmailStr


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str


class VerificationResponse(BaseModel):
    message: str


# Register with email verification token
@router.post("/register", response_model=UserResponse)
def register(user: UserCreate, db: Session = Depends(get_db), request: Request = None):
    if request:
        check_rate_limit(request)
    
    db_user = db.query(User).filter(
        (User.email == user.email) | (User.username == user.username)
    ).first()
    
    if db_user:
        raise HTTPException(status_code=400, detail="Email or username already registered")
    
    hashed_password = get_password_hash(user.password)
    verification_token = secrets.token_urlsafe(32)
    
    db_user = User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password,
        verification_token=verification_token if settings.EMAIL_VERIFICATION_REQUIRED else None,
        is_active=not settings.EMAIL_VERIFICATION_REQUIRED
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    # TODO: Send verification email
    # In production, send email with verification link
    # For now, the token is stored but not sent via email
    
    return db_user


@router.post("/verify-email")
def verify_email(token: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user.is_active = True
    user.verification_token = None
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
    request: Request = None
):
    if request:
        check_rate_limit(request)
    
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active and settings.EMAIL_VERIFICATION_REQUIRED:
        raise HTTPException(
            status_code=403,
            detail="Please verify your email first"
        )
    
    # Create tokens
    access_token = create_access_token(data={"sub": str(user.id)})
    refresh_token = create_refresh_token(data={"sub": str(user.id)})
    
    # Store refresh token
    db_refresh = RefreshToken(
        token=hashlib.sha256(refresh_token.encode()).hexdigest(),
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(db_refresh)
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }


@router.post("/refresh", response_model=TokenResponse)
def refresh_token(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    # Verify refresh token
    payload = verify_token(request.refresh_token)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid refresh token")
    
    # Check if token exists in database
    token_hash = hashlib.sha256(request.refresh_token.encode()).hexdigest()
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token == token_hash,
        RefreshToken.expires_at > datetime.utcnow()
    ).first()
    
    if not db_token:
        raise HTTPException(status_code=401, detail="Refresh token expired or revoked")
    
    # Create new tokens
    access_token = create_access_token(data={"sub": str(db_token.user_id)})
    new_refresh_token = create_refresh_token(data={"sub": str(db_token.user_id)})
    
    # Revoke old refresh token
    db.delete(db_token)
    
    # Store new refresh token
    db_new_token = RefreshToken(
        token=hashlib.sha256(new_refresh_token.encode()).hexdigest(),
        user_id=db_token.user_id,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(db_new_token)
    db.commit()
    
    return {
        "access_token": access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(request: RefreshTokenRequest, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(request.refresh_token.encode()).hexdigest()
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token_hash).first()
    
    if db_token:
        db.delete(db_token)
        db.commit()
    
    return {"message": "Logged out successfully"}


@router.post("/request-password-reset")
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db), request: Request = None):
    if request:
        check_rate_limit(request)
    
    user = db.query(User).filter(User.email == data.email).first()
    
    # Always return success to prevent email enumeration
    if not user:
        return {"message": "If the email exists, a reset link has been sent"}
    
    # Generate reset token
    reset_token = secrets.token_urlsafe(32)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    
    # Store hashed token
    db_token = PasswordResetToken(
        token=hashlib.sha256(reset_token.encode()).hexdigest(),
        user_id=user.id,
        expires_at=expires_at
    )
    db.add(db_token)
    db.commit()
    
    # TODO: Send email with reset link
    # In production: send email with link containing reset_token
    print(f"Password reset token for {user.email}: {reset_token}")
    
    return {"message": "If the email exists, a reset link has been sent"}


@router.post("/reset-password")
def reset_password(data: PasswordResetConfirm, db: Session = Depends(get_db)):
    token_hash = hashlib.sha256(data.token.encode()).hexdigest()
    
    db_token = db.query(PasswordResetToken).filter(
        PasswordResetToken.token == token_hash,
        PasswordResetToken.expires_at > datetime.utcnow()
    ).first()
    
    if not db_token:
        raise HTTPException(status_code=400, detail="Invalid or expired reset token")
    
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    
    # Update password
    user.hashed_password = get_password_hash(data.new_password)
    
    # Delete used token
    db.delete(db_token)
    
    # Revoke all refresh tokens for this user
    db.query(RefreshToken).filter(RefreshToken.user_id == user.id).delete()
    
    db.commit()
    
    return {"message": "Password reset successfully"}


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user
