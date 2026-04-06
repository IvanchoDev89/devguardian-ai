from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User
from app.models.schemas import UserProfile, UserProfileUpdate, Settings, SettingsUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.get("/me", response_model=UserProfile)
def get_current_user_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@router.put("/me", response_model=UserProfile)
def update_current_user_profile(
    profile_data: UserProfileUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if profile_data.full_name is not None:
        user.full_name = profile_data.full_name
    if profile_data.username is not None:
        existing = db.query(User).filter(
            User.username == profile_data.username,
            User.id != current_user.id
        ).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already taken")
        user.username = profile_data.username
    
    db.commit()
    db.refresh(user)
    
    return {
        "id": user.id,
        "email": user.email,
        "username": user.username,
        "full_name": user.full_name,
        "role": user.role,
        "is_active": user.is_active,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


@router.get("/me/settings", response_model=Settings)
def get_user_settings(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "theme": user.settings.get("theme", "dark") if user.settings else "dark",
        "language": user.settings.get("language", "en") if user.settings else "en",
        "notifications_email": user.settings.get("notifications_email", True) if user.settings else True,
        "notifications_scan": user.settings.get("notifications_scan", True) if user.settings else True,
    }


@router.put("/me/settings", response_model=Settings)
def update_user_settings(
    settings_data: SettingsUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == current_user.id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.settings:
        user.settings = {}
    
    if settings_data.theme is not None:
        user.settings["theme"] = settings_data.theme
    if settings_data.language is not None:
        user.settings["language"] = settings_data.language
    if settings_data.notifications_email is not None:
        user.settings["notifications_email"] = settings_data.notifications_email
    if settings_data.notifications_scan is not None:
        user.settings["notifications_scan"] = settings_data.notifications_scan
    
    db.commit()
    
    return {
        "theme": user.settings.get("theme", "dark"),
        "language": user.settings.get("language", "en"),
        "notifications_email": user.settings.get("notifications_email", True),
        "notifications_scan": user.settings.get("notifications_scan", True),
    }