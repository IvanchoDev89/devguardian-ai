from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, Dict, List
from datetime import datetime
import httpx
import asyncio
from app.core.auth import get_current_user, TokenData

router = APIRouter(prefix="/api/webhooks", tags=["Webhooks"])

webhooks_db: Dict[str, dict] = {}


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
    current_user: TokenData = Depends(get_current_user)
):
    """Create a new webhook"""
    import secrets
    
    # Validate URL
    if not webhook.url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    
    valid_events = ["scan.completed", "scan.failed", "user.login", "user.registered"]
    for event in webhook.events:
        if event not in valid_events:
            raise HTTPException(status_code=400, detail=f"Invalid event: {event}")
    
    webhook_id = f"wh_{secrets.token_urlsafe(12)}"
    
    webhook_data = {
        "webhook_id": webhook_id,
        "user_id": current_user.user_id,
        "url": webhook.url,
        "events": webhook.events,
        "name": webhook.name,
        "active": webhook.active,
        "created_at": datetime.now().isoformat(),
        "last_triggered": None
    }
    
    webhooks_db[webhook_id] = webhook_data
    
    return webhook_data


@router.get("")
async def list_webhooks(current_user: TokenData = Depends(get_current_user)):
    """List all webhooks for the user"""
    user_webhooks = [w for w in webhooks_db.values() if w["user_id"] == current_user.user_id]
    return user_webhooks


@router.get("/{webhook_id}")
async def get_webhook(
    webhook_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get a specific webhook"""
    webhook = webhooks_db.get(webhook_id)
    if not webhook or webhook["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Webhook not found")
    return webhook


@router.delete("/{webhook_id}")
async def delete_webhook(
    webhook_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Delete a webhook"""
    webhook = webhooks_db.get(webhook_id)
    if not webhook or webhook["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    del webhooks_db[webhook_id]
    return {"message": "Webhook deleted"}


@router.post("/{webhook_id}/test")
async def test_webhook(
    webhook_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Test a webhook by sending a test event"""
    webhook = webhooks_db.get(webhook_id)
    if not webhook or webhook["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    await send_webhook(webhook["url"], "webhook.test", {"message": "This is a test"})
    
    return {"message": "Test event sent"}


@router.put("/{webhook_id}")
async def update_webhook(
    webhook_id: str,
    webhook: WebhookCreate,
    current_user: TokenData = Depends(get_current_user)
):
    """Update a webhook"""
    existing = webhooks_db.get(webhook_id)
    if not existing or existing["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Webhook not found")
    
    existing["url"] = webhook.url
    existing["events"] = webhook.events
    existing["name"] = webhook.name
    existing["active"] = webhook.active
    
    return existing


async def trigger_webhook_event(event: str, user_id: str, data: dict):
    """Trigger webhooks for a specific event"""
    user_webhooks = [w for w in webhooks_db.values() 
                   if w["user_id"] == user_id and w["active"] and event in w["events"]]
    
    for webhook in user_webhooks:
        await send_webhook(webhook["url"], event, data)
        webhook["last_triggered"] = datetime.now().isoformat()
