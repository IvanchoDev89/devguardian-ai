from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import secrets
import json
from sqlalchemy.orm import Session
from app.database import get_db, Webhook as DBWebhook
from app.core.auth import get_current_user_optional, TokenData

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])


class WebhookCreate(BaseModel):
    url: str
    events: List[str]
    name: str
    active: bool = True


class WebhookResponse(BaseModel):
    webhook_id: str
    url: str
    events: List[str]
    name: str
    active: bool
    created_at: str
    last_triggered: Optional[str]


async def send_webhook(url: str, event: str, data: dict):
    """Send webhook notification asynchronously"""
    import httpx
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            await client.post(url, json={
                "event": event,
                "timestamp": datetime.now().isoformat(),
                "data": data
            })
    except Exception as e:
        print(f"Webhook delivery failed: {e}")


@router.post("")
async def create_webhook(
    webhook: WebhookCreate,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Create a new webhook"""
    user_id = current_user.user_id if current_user else "anonymous"
    if not webhook.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    
    valid_events = ["scan.completed", "scan.failed", "user.login", "user.registered"]
    for event in webhook.events:
        if event not in valid_events:
            raise HTTPException(status_code=400, detail=f"Invalid event: {event}")
    
    webhook_id = f"wh_{secrets.token_urlsafe(12)}"
    
    db_webhook = DBWebhook(
        webhook_id=webhook_id,
        user_id=user_id,
        url=webhook.url,
        events=json.dumps(webhook.events),
        name=webhook.name,
        is_active=webhook.active
    )
    db.add(db_webhook)
    db.commit()
    
    return {
        "webhook_id": webhook_id,
        "url": webhook.url,
        "events": webhook.events,
        "name": webhook.name,
        "active": webhook.active,
        "created_at": datetime.now().isoformat(),
        "last_triggered": None
    }


@router.get("")
async def list_webhooks(
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """List all webhooks for the user"""
    user_id = current_user.user_id if current_user else "anonymous"
    webhooks = db.query(DBWebhook).filter(DBWebhook.user_id == user_id).all()
    
    result = []
    for w in webhooks:
        result.append({
            "webhook_id": w.webhook_id,
            "url": w.url,
            "events": json.loads(w.events) if w.events else [],
            "name": w.name,
            "active": w.is_active,
            "created_at": w.created_at.isoformat() if w.created_at else None,
            "last_triggered": w.last_triggered.isoformat() if w.last_triggered else None
        })
    
    return result


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Delete a webhook"""
    user_id = current_user.user_id if current_user else "anonymous"
    webhook = db.query(DBWebhook).filter(
        DBWebhook.webhook_id == webhook_id,
        DBWebhook.user_id == user_id
    ).first()
    
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    db.delete(webhook)
    db.commit()
    
    return {"message": "Webhook deleted"}


@router.post("/{webhook_id}/test")
async def test_webhook(
    webhook_id: str,
    db: Session = Depends(get_db),
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Test a webhook"""
    user_id = current_user.user_id if current_user else "anonymous"
    webhook = db.query(DBWebhook).filter(
        DBWebhook.webhook_id == webhook_id,
        DBWebhook.user_id == user_id
    ).first()
    
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    await send_webhook(webhook.url, "webhook.test", {"message": "This is a test"})
    
    return {"message": "Test event sent"}
