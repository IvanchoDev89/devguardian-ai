"""
Notifications Integration - Slack, Discord, JIRA
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import httpx

router = APIRouter(prefix="/api/notifications", tags=["Notifications"])


class SlackWebhookConfig(BaseModel):
    """Slack webhook configuration"""
    webhook_url: str
    channel: Optional[str] = None
    mention_users: Optional[List[str]] = None
    mention_on_critical: bool = True


class DiscordWebhookConfig(BaseModel):
    """Discord webhook configuration"""
    webhook_url: str
    mention_role: Optional[str] = None


class JIRAConfig(BaseModel):
    """JIRA integration configuration"""
    jira_url: str
    email: str
    api_token: str
    project_key: str
    issue_type: str = "Bug"
    auto_create: bool = False
    severity_to_priority: Optional[Dict[str, str]] = None


class NotificationRequest(BaseModel):
    """Request to send a notification"""
    title: str
    message: str
    severity: str = "info"  # info, warning, error, critical
    findings: Optional[List[Dict[str, Any]]] = None
    scan_id: Optional[str] = None
    repository: Optional[str] = None


class TicketCreateRequest(BaseModel):
    """Request to create a JIRA ticket"""
    title: str
    description: str
    severity: str = "medium"
    labels: Optional[List[str]] = None


# Configuration storage
slack_config: Optional[SlackWebhookConfig] = None
discord_config: Optional[DiscordWebhookConfig] = None
jira_config: Optional[JIRAConfig] = None


def _get_severity_emoji(severity: str) -> str:
    emojis = {
        "critical": "🔴",
        "high": "🟠",
        "medium": "🟡",
        "low": "🔵",
        "info": "ℹ️"
    }
    return emojis.get(severity.lower(), "ℹ️")


def _format_slack_message(notification: NotificationRequest) -> dict:
    """Format message for Slack"""
    blocks = [
        {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": f"{_get_severity_emoji(notification.severity)} {notification.title}"
            }
        },
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": notification.message
            }
        }
    ]
    
    if notification.findings:
        findings_text = "*Top Findings:*\n"
        for i, f in enumerate(notification.findings[:5], 1):
            findings_text += f"• {f.get('severity', '?').upper()}: {f.get('message', 'N/A')} ({f.get('file', 'N/A')}:{f.get('line', '?')})\n"
        
        blocks.append({
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": findings_text
            }
        })
    
    if notification.scan_id:
        blocks.append({
            "type": "context",
            "elements": [
                {
                    "type": "mrkdwn",
                    "text": f"🔍 Scan ID: `{notification.scan_id}` | Repository: {notification.repository or 'N/A'}"
                }
            ]
        })
    
    return {"blocks": blocks}


def _format_discord_message(notification: NotificationRequest) -> dict:
    """Format message for Discord"""
    embed = {
        "title": f"{_get_severity_emoji(notification.severity)} {notification.title}",
        "description": notification.message,
        "color": {
            "critical": 16711680,  # Red
            "high": 16744448,       # Orange
            "medium": 16776960,     # Yellow
            "low": 65280,           # Green
            "info": 3447003         # Blue
        }.get(notification.severity.lower(), 3447003),
        "timestamp": datetime.utcnow().isoformat()
    }
    
    if notification.findings:
        fields = []
        for f in notification.findings[:5]:
            fields.append({
                "name": f"{f.get('severity', '?').upper()}: {f.get('file', 'N/A')}",
                "value": f"Line {f.get('line', '?')}: {f.get('message', 'N/A')}",
                "inline": False
            })
        embed["fields"] = fields
    
    if notification.scan_id:
        embed["footer"] = {
            "text": f"Scan ID: {notification.scan_id} | Repository: {notification.repository or 'N/A'}"
        }
    
    return {"embeds": [embed]}


@router.post("/slack/configure")
async def configure_slack(config: SlackWebhookConfig):
    """Configure Slack webhook"""
    global slack_config
    # Validate webhook
    try:
        async with httpx.AsyncClient() as client:
            test_msg = {"text": "DevGuardian AI connected successfully! 🔒"}
            resp = await client.post(config.webhook_url, json=test_msg, timeout=10)
            if resp.status_code not in [200, 204]:
                raise HTTPException(status_code=400, detail="Invalid Slack webhook URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to validate Slack webhook: {str(e)}")
    
    slack_config = config
    return {"status": "configured", "channel": config.channel}


@router.post("/discord/configure")
async def configure_discord(config: DiscordWebhookConfig):
    """Configure Discord webhook"""
    global discord_config
    # Validate webhook
    try:
        async with httpx.AsyncClient() as client:
            test_msg = {"content": "DevGuardian AI connected successfully! 🔒"}
            resp = await client.post(config.webhook_url, json=test_msg, timeout=10)
            if resp.status_code not in [200, 204]:
                raise HTTPException(status_code=400, detail="Invalid Discord webhook URL")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to validate Discord webhook: {str(e)}")
    
    discord_config = config
    return {"status": "configured"}


@router.post("/jira/configure")
async def configure_jira(config: JIRAConfig):
    """Configure JIRA integration"""
    global jira_config
    
    # Validate credentials
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.get(
                f"{config.jira_url}/rest/api/3/myself",
                auth=(config.email, config.api_token),
                timeout=10
            )
            if resp.status_code != 200:
                raise HTTPException(status_code=400, detail="Invalid JIRA credentials")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to validate JIRA: {str(e)}")
    
    jira_config = config
    return {"status": "configured", "project": config.project_key}


@router.post("/send")
async def send_notification(
    notification: NotificationRequest,
    background_tasks: BackgroundTasks
):
    """Send notification to all configured channels"""
    results = {}
    
    # Send to Slack
    if slack_config:
        try:
            msg = _format_slack_message(notification)
            if slack_config.mention_on_critical and notification.severity == "critical":
                # Add mention
                msg["text"] = f"<!channel> New critical security alert!"
            
            async with httpx.AsyncClient() as client:
                resp = await client.post(slack_config.webhook_url, json=msg, timeout=10)
                results["slack"] = "sent" if resp.status_code in [200, 204] else "failed"
        except Exception as e:
            results["slack"] = f"error: {str(e)}"
    else:
        results["slack"] = "not configured"
    
    # Send to Discord
    if discord_config:
        try:
            msg = _format_discord_message(notification)
            async with httpx.AsyncClient() as client:
                resp = await client.post(discord_config.webhook_url, json=msg, timeout=10)
                results["discord"] = "sent" if resp.status_code in [200, 204] else "failed"
        except Exception as e:
            results["discord"] = f"error: {str(e)}"
    else:
        results["discord"] = "not configured"
    
    return {"status": "completed", "results": results}


@router.post("/jira/ticket")
async def create_jira_ticket(request: TicketCreateRequest):
    """Create a JIRA ticket"""
    if not jira_config:
        raise HTTPException(status_code=400, detail="JIRA not configured")
    
    priority_map = jira_config.severity_to_priority or {
        "critical": "Highest",
        "high": "High",
        "medium": "Medium",
        "low": "Low"
    }
    
    issue_data = {
        "fields": {
            "project": {"key": jira_config.project_key},
            "summary": f"[Security] {request.title}",
            "description": {
                "type": "doc",
                "version": 1,
                "content": [
                    {
                        "type": "paragraph",
                        "content": [
                            {"type": "text", "text": request.description}
                        ]
                    }
                ]
            },
            "issuetype": {"name": jira_config.issue_type},
            "priority": {"name": priority_map.get(request.severity, "Medium")},
            "labels": request.labels or ["security", "devguardian"]
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{jira_config.jira_url}/rest/api/3/issue",
                json=issue_data,
                auth=(jira_config.email, jira_config.api_token),
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if resp.status_code == 201:
                data = resp.json()
                return {
                    "status": "created",
                    "ticket_key": data["key"],
                    "ticket_url": f"{jira_config.jira_url}/browse/{data['key']}"
                }
            else:
                raise HTTPException(status_code=400, detail=f"JIRA error: {resp.text}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create ticket: {str(e)}")


@router.get("/status")
async def get_notification_status():
    """Get notification configuration status"""
    return {
        "slack": {
            "configured": slack_config is not None,
            "channel": slack_config.channel if slack_config else None
        },
        "discord": {
            "configured": discord_config is not None
        },
        "jira": {
            "configured": jira_config is not None,
            "project": jira_config.project_key if jira_config else None,
            "url": jira_config.jira_url if jira_config else None
        }
    }


@router.delete("/slack")
async def remove_slack():
    """Remove Slack configuration"""
    global slack_config
    slack_config = None
    return {"status": "removed"}


@router.delete("/discord")
async def remove_discord():
    """Remove Discord configuration"""
    global discord_config
    discord_config = None
    return {"status": "removed"}


@router.delete("/jira")
async def remove_jira():
    """Remove JIRA configuration"""
    global jira_config
    jira_config = None
    return {"status": "removed"}
