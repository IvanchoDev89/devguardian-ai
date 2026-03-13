"""
Ticketing Integration API Endpoints
Create GitHub Issues and JIRA tickets
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging

from app.services.ticketing import create_ticketing_service, TicketingService

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/tickets", tags=["Ticketing"])

# Global ticketing service instance
ticketing = create_ticketing_service()


class GitHubIssueRequest(BaseModel):
    owner: str
    repo: str
    title: str
    body: str
    labels: Optional[List[str]] = None
    severity: str = "medium"


class JIRATicketRequest(BaseModel):
    project_key: str
    issue_type: str = "Bug"
    summary: str
    description: str
    priority: str = "Medium"
    labels: Optional[List[str]] = None


class CreateTicketsRequest(BaseModel):
    provider: str  # github, jira
    vulnerabilities: List[Dict[str, Any]]
    owner: Optional[str] = None  # For GitHub
    repo: Optional[str] = None  # For GitHub
    project_key: Optional[str] = None  # For JIRA


@router.post("/github/issue")
async def create_github_issue(request: GitHubIssueRequest):
    """Create a GitHub issue"""
    try:
        # Configure with token from header (would normally use auth)
        token = "GITHUB_TOKEN"  # Would come from config
        
        issue = await ticketing.create_github_issue(
            owner=request.owner,
            repo=request.repo,
            title=request.title,
            body=request.body,
            labels=request.labels,
            severity=request.severity
        )
        
        return {
            "success": True,
            "ticket": {
                "id": issue.id,
                "url": issue.url,
                "status": issue.status
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to create GitHub issue: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/jira/ticket")
async def create_jira_ticket(request: JIRATicketRequest):
    """Create a JIRA ticket"""
    try:
        issue = await ticketing.create_jira_ticket(
            project_key=request.project_key,
            issue_type=request.issue_type,
            summary=request.summary,
            description=request.description,
            priority=request.priority,
            labels=request.labels
        )
        
        return {
            "success": True,
            "ticket": {
                "id": issue.id,
                "url": issue.url,
                "status": issue.status
            }
        }
        
    except Exception as e:
        logger.error(f"Failed to create JIRA ticket: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/batch")
async def create_tickets_batch(request: CreateTicketsRequest):
    """Create tickets for multiple vulnerabilities"""
    created = []
    failed = []
    
    for vuln in request.vulnerabilities:
        try:
            # Create ticket from vulnerability
            ticket_data = ticketing.create_ticket_from_vulnerability(
                vuln=vuln,
                integration=request.provider
            )
            
            if request.provider == "github" and request.owner and request.repo:
                issue = await ticketing.create_github_issue(
                    owner=request.owner,
                    repo=request.repo,
                    title=ticket_data["title"],
                    body=ticket_data["body"],
                    labels=ticket_data["labels"],
                    severity=vuln.get("severity", "medium")
                )
                created.append({
                    "vulnerability": vuln.get("type"),
                    "ticket_id": issue.id,
                    "url": issue.url
                })
                
            elif request.provider == "jira" and request.project_key:
                ticket = await ticketing.create_jira_ticket(
                    project_key=request.project_key,
                    issue_type="Bug",
                    summary=ticket_data["title"],
                    description=ticket_data["body"],
                    priority=vuln.get("severity", "medium").replace("critical", "Highest").replace("high", "High").replace("medium", "Medium").replace("low", "Low")
                )
                created.append({
                    "vulnerability": vuln.get("type"),
                    "ticket_id": ticket.id,
                    "url": ticket.url
                })
                
        except Exception as e:
            failed.append({
                "vulnerability": vuln.get("type"),
                "error": str(e)
            })
    
    return {
        "created": created,
        "failed": failed,
        "total_created": len(created),
        "total_failed": len(failed)
    }


@router.get("/providers")
async def get_providers():
    """Get supported ticketing providers"""
    return {
        "providers": [
            {
                "id": "github",
                "name": "GitHub Issues",
                "features": ["labels", "milestones", "assignees"]
            },
            {
                "id": "jira", 
                "name": "JIRA",
                "features": ["projects", "issue types", "priorities", "components"]
            }
        ]
    }
