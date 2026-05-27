from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr, field_validator
from datetime import timedelta, datetime
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
from app.models.schemas import UserCreate, UserResponse, TokenResponse
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

CSRF_TOKEN_EXPIRE_MINUTES = 60
csrf_tokens: dict[str, tuple[str, datetime]] = {}


def generate_csrf_token(user_id: int) -> str:
    token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=CSRF_TOKEN_EXPIRE_MINUTES)
    csrf_tokens[token] = (str(user_id), expires)
    return token


def validate_csrf_token(token: str, user_id: int) -> bool:
    stored = csrf_tokens.get(token)
    if stored is None:
        return False
    stored_user_id, expires = stored
    if datetime.utcnow() > expires:
        del csrf_tokens[token]
        return False
    return stored_user_id == str(user_id)


RATE_LIMIT = 5
RATE_WINDOW = 60


def check_rate_limit(request: Request, endpoint: str = "default"):
    """Rate limiting with Redis fallback to in-memory"""
    client_ip = request.client.host if request and request.client else "unknown"
    now = datetime.utcnow()
    key = f"rate_limit:{endpoint}:{client_ip}"
    
    if settings.USE_REDIS and settings.REDIS_URL:
        try:
            import redis
            if not hasattr(check_rate_limit, 'redis_client') or check_rate_limit.redis_client is None:
                check_rate_limit.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            redis_client = check_rate_limit.redis_client
            current_count = redis_client.get(key)
            
            if current_count and int(current_count) >= RATE_LIMIT:
                raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
            
            pipe = redis_client.pipeline()
            pipe.incr(key)
            pipe.expire(key, RATE_WINDOW)
            pipe.execute()
            return
        except Exception as e:
            logger.warning(f"Redis rate limiting failed, falling back to in-memory: {e}")
    
    # In-memory fallback with automatic cleanup
    if not hasattr(check_rate_limit, 'store'):
        check_rate_limit.store = {}
        check_rate_limit.last_cleanup = now
    
    store = check_rate_limit.store
    
    if client_ip not in store:
        store[client_ip] = []
    
    store[client_ip] = [
        t for t in store[client_ip]
        if (now - t).total_seconds() < RATE_WINDOW
    ]
    
    if len(store[client_ip]) >= RATE_LIMIT:
        raise HTTPException(status_code=429, detail="Too many requests. Please try again later.")
    
    store[client_ip].append(now)
    
    # Periodic cleanup
    if len(store) > 10000:
        expired_keys = [
            k for k, v in store.items()
            if not v or (now - max(v)).total_seconds() > RATE_WINDOW * 2
        ]
        for k in expired_keys[:5000]:
            del store[k]


class EmailSchema(BaseModel):
    email: EmailStr


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    token: str
    new_password: str

    @field_validator('new_password')
    @classmethod
    def validate_new_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v


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


class VerifyEmailRequest(BaseModel):
    token: str


@router.post("/verify-email")
def verify_email(data: VerifyEmailRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.verification_token == data.token).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid verification token")
    
    user.is_active = True
    user.verification_token = None
    db.commit()
    
    return {"message": "Email verified successfully"}


@router.post("/login")
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
    
    # Generate CSRF token
    csrf_token = generate_csrf_token(user.id)
    
    # Store refresh token
    db_refresh = RefreshToken(
        token=hashlib.sha256(refresh_token.encode()).hexdigest(),
        user_id=user.id,
        expires_at=datetime.utcnow() + timedelta(days=30)
    )
    db.add(db_refresh)
    db.commit()
    
    # Audit logging
    client_host = request.client.host if request.client else 'unknown'
    logger.info(f"User {user.id} ({user.email}) logged in from IP {client_host}")
    
    # Set httpOnly cookies for tokens (production)
    response = JSONResponse({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "csrf_token": csrf_token
    })
    
    # In production, these cookies would be httpOnly and Secure
    # For now, we include them in response body for backward compatibility
    # But also set cookies for enhanced security
    is_production = not settings.DEBUG
    
    if is_production:
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=30 * 60,
            path="/"
        )
        response.set_cookie(
            key="refresh_token", 
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
            max_age=30 * 24 * 60 * 60,
            path="/"
        )
    
    return response


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
def logout(
    token_data: RefreshTokenRequest,
    fastapi_request: Request,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate CSRF token
    csrf_from_header = fastapi_request.headers.get("X-CSRF-Token")
    if not csrf_from_header or not validate_csrf_token(csrf_from_header, current_user.id):
        raise HTTPException(status_code=403, detail="Invalid CSRF token")
    
    token_hash = hashlib.sha256(token_data.refresh_token.encode()).hexdigest()
    db_token = db.query(RefreshToken).filter(RefreshToken.token == token_hash).first()
    
    if db_token:
        user_email = db_token.user.email if db_token.user else "unknown"
        logger.info(f"User {user_email} logged out")
        db.delete(db_token)
        db.commit()
    
    return {"message": "Logged out successfully"}


@router.post("/request-password-reset")
def request_password_reset(data: PasswordResetRequest, db: Session = Depends(get_db), request: Request = None):
    if request:
        check_rate_limit(request, "password_reset")
    
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
    
    logger.info(f"Password reset requested for user {user.id} ({user.email})")
    
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
