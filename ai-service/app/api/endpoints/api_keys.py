from fastapi import APIRouter, Depends, HTTPException, status, Header
from pydantic import BaseModel
from typing import List, Optional
from app.core.auth import get_current_user, TokenData
from app.core.api_keys import get_api_key_manager

router = APIRouter(prefix="/api/keys", tags=["API Keys"])


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
    current_user: TokenData = Depends(get_current_user)
):
    """Create a new API key"""
    valid_plans = ["free", "pro", "enterprise"]
    if request.plan not in valid_plans:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid plan. Must be one of: {valid_plans}"
        )
    
    manager = get_api_key_manager()
    api_key, full_key = manager.create_key(
        user_id=current_user.user_id,
        name=request.name,
        plan=request.plan,
        expires_days=request.expires_days
    )
    
    return APIKeyWithSecret(
        key_id=api_key.key_id,
        api_key=full_key,
        name=api_key.name,
        plan=api_key.plan,
        monthly_quota=api_key.monthly_quota,
        created_at=api_key.created_at,
        expires_at=api_key.expires_at
    )


@router.get("", response_model=List[APIKeyResponse])
async def list_api_keys(current_user: TokenData = Depends(get_current_user)):
    """List all API keys for the current user"""
    manager = get_api_key_manager()
    keys = manager.get_user_keys(current_user.user_id)
    return [key.to_dict() for key in keys]


@router.get("/{key_id}", response_model=APIKeyResponse)
async def get_api_key(
    key_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get details of a specific API key"""
    manager = get_api_key_manager()
    keys = manager.get_user_keys(current_user.user_id)
    
    for key in keys:
        if key.key_id == key_id:
            return key.to_dict()
    
    raise HTTPException(status_code=404, detail="API key not found")


@router.delete("/{key_id}")
async def delete_api_key(
    key_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Delete an API key"""
    manager = get_api_key_manager()
    keys = manager.get_user_keys(current_user.user_id)
    
    for key in keys:
        if key.key_id == key_id:
            manager.delete_key(key_id)
            return {"message": "API key deleted"}
    
    raise HTTPException(status_code=404, detail="API key not found")


@router.post("/{key_id}/revoke")
async def revoke_api_key(
    key_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Revoke an API key (can be reactivated)"""
    manager = get_api_key_manager()
    keys = manager.get_user_keys(current_user.user_id)
    
    for key in keys:
        if key.key_id == key_id:
            manager.revoke_key(key_id)
            return {"message": "API key revoked"}
    
    raise HTTPException(status_code=404, detail="API key not found")


@router.get("/usage/stats", response_model=UsageStatsResponse)
async def get_usage_stats(current_user: TokenData = Depends(get_current_user)):
    """Get usage statistics for the current user"""
    manager = get_api_key_manager()
    keys = manager.get_user_keys(current_user.user_id)
    
    if not keys:
        return UsageStatsResponse(
            plan="free",
            monthly_quota=50,
            scans_used=0,
            remaining=50,
            reset_date="End of month"
        )
    
    # Aggregate usage across all keys
    total_quota = sum(k.monthly_quota for k in keys)
    total_used = sum(k.scans_used for k in keys)
    
    # Get primary plan (highest tier)
    plan = "free"
    if any(k.plan == "enterprise" for k in keys):
        plan = "enterprise"
    elif any(k.plan == "pro" for k in keys):
        plan = "pro"
    
    from datetime import datetime
    from dateutil.relativedelta import relativedelta
    
    now = datetime.now()
    next_month = now + relativedelta(months=1)
    reset_date = f"{next_month.year}-{next_month.month:02d}-01"
    
    return UsageStatsResponse(
        plan=plan,
        monthly_quota=total_quota,
        scans_used=total_used,
        remaining=max(0, total_quota - total_used),
        reset_date=reset_date
    )
