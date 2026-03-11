from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import Session
from app.database import get_db, APIKey as DBAPIKey
from app.core.encryption import encrypt_value, decrypt_value
from app.core.auth import get_current_user_optional, TokenData
import secrets

router = APIRouter(prefix="/api/keys", tags=["API Keys"])


def generate_api_key() -> tuple[str, str, str]:
    key = f"dg_{secrets.token_urlsafe(32)}"
    hashed = encrypt_value(key)
    prefix = key[:12] + "..."
    return key, hashed, prefix


PLAN_QUOTAS = {
    "free": 50,
    "pro": 500,
    "enterprise": -1
}


class CreateAPIKeyRequest(BaseModel):
    name: str
    plan: str = "free"
    expires_days: Optional[int] = None


class APIKeyResponse(BaseModel):
    key_id: str
    key_prefix: str
    name: str
    plan: str
    monthly_quota: int
    scans_used: int
    remaining: int
    created_at: str
    expires_at: Optional[str]
    last_used: Optional[str]
    is_active: bool


class APIKeyWithSecret(BaseModel):
    key_id: str
    api_key: str
    name: str
    plan: str
    monthly_quota: int
    created_at: str
    expires_at: Optional[str]


class UsageStatsResponse(BaseModel):
    plan: str
    monthly_quota: int
    scans_used: int
    remaining: int
    reset_date: str


@router.post("", response_model=APIKeyWithSecret)
async def create_api_key(
    request: CreateAPIKeyRequest,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Create a new API key"""
    user_id = current_user.user_id if current_user else "anonymous"
    user_email = current_user.email if current_user and hasattr(current_user, 'email') else "anonymous@devguardian.ai"
    valid_plans = ["free", "pro", "enterprise"]
    if request.plan not in valid_plans:
        raise HTTPException(status_code=400, detail=f"Invalid plan")
    
    key_id = f"key_{datetime.now().timestamp()}"
    full_key, hashed_key, prefix = generate_api_key()
    
    expires_at = None
    if request.expires_days:
        from datetime import timedelta
        expires_at = datetime.now() + timedelta(days=request.expires_days)
    
    db_key = DBAPIKey(
        key_id=key_id,
        key_prefix=prefix,
        hashed_key=hashed_key,
        user_id=user_id,
        name=request.name,
        plan=request.plan,
        monthly_quota=PLAN_QUOTAS.get(request.plan, 50),
        scans_used=0,
        expires_at=expires_at,
        is_active=True
    )
    db.add(db_key)
    db.commit()
    
    return APIKeyWithSecret(
        key_id=key_id,
        api_key=full_key,
        name=request.name,
        plan=request.plan,
        monthly_quota=PLAN_QUOTAS.get(request.plan, 50),
        created_at=datetime.now().isoformat(),
        expires_at=expires_at.isoformat() if expires_at else None
    )


@router.get("", response_model=List[APIKeyResponse])
async def list_api_keys(
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """List all API keys for the current user"""
    user_id = current_user.user_id if current_user else "anonymous"
    keys = db.query(DBAPIKey).filter(DBAPIKey.user_id == user_id).all()
    
    result = []
    for key in keys:
        remaining = key.monthly_quota - key.scans_used if key.monthly_quota > 0 else -1
        result.append(APIKeyResponse(
            key_id=key.key_id,
            key_prefix=key.key_prefix,
            name=key.name,
            plan=key.plan,
            monthly_quota=key.monthly_quota,
            scans_used=key.scans_used,
            remaining=remaining,
            created_at=key.created_at.isoformat() if key.created_at else "",
            expires_at=key.expires_at.isoformat() if key.expires_at else None,
            last_used=key.last_used.isoformat() if key.last_used else None,
            is_active=key.is_active
        ))
    
    return result


@router.get("/usage/stats", response_model=UsageStatsResponse)
async def get_usage_stats(
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Get usage statistics for the current user"""
    user_id = current_user.user_id if current_user else "anonymous"
    keys = db.query(DBAPIKey).filter(DBAPIKey.user_id == user_id).all()
    
    if not keys:
        return UsageStatsResponse(
            plan="free",
            monthly_quota=50,
            scans_used=0,
            remaining=50,
            reset_date="End of month"
        )
    
    total_quota = sum(k.monthly_quota for k in keys)
    total_used = sum(k.scans_used for k in keys)
    
    plan = "free"
    if any(k.plan == "enterprise" for k in keys):
        plan = "enterprise"
    elif any(k.plan == "pro" for k in keys):
        plan = "pro"
    
    from dateutil.relativedelta import relativedelta
    now = datetime.now()
    next_month = now + relativedelta(months=1)
    
    return UsageStatsResponse(
        plan=plan,
        monthly_quota=total_quota,
        scans_used=total_used,
        remaining=max(0, total_quota - total_used) if total_quota > 0 else -1,
        reset_date=f"{next_month.year}-{next_month.month:02d}-01"
    )


@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Delete an API key"""
    user_id = current_user.user_id if current_user else "anonymous"
    key = db.query(DBAPIKey).filter(
        DBAPIKey.key_id == key_id,
        DBAPIKey.user_id == user_id
    ).first()
    
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    db.delete(key)
    db.commit()
    
    return {"message": "API key deleted"}


@router.post("/{key_id}/revoke")
async def revoke_api_key(
    key_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Revoke an API key"""
    user_id = current_user.user_id if current_user else "anonymous"
    key = db.query(DBAPIKey).filter(
        DBAPIKey.key_id == key_id,
        DBAPIKey.user_id == user_id
    ).first()
    
    if not key:
        raise HTTPException(status_code=404, detail="API key not found")
    
    key.is_active = False
    db.commit()
    
    return {"message": "API key revoked"}
