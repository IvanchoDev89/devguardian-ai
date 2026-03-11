import hmac
import hashlib
import secrets
from fastapi import APIRouter, HTTPException, Depends, Request, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict
from datetime import datetime
import asyncio
import httpx
from app.core.auth import get_current_user, TokenData
from app.core.webhook_utils import get_github_webhook_secret, verify_github_signature

router = APIRouter(prefix="/api/github", tags=["GitHub Integration"])

github_integrations_db: Dict[str, dict] = {}


class GitHubIntegrationCreate(BaseModel):
    repo_owner: str
    repo_name: str
    installation_id: str
    auto_scan_pr: bool = True
    auto_comment: bool = True
    scan_on_push: bool = False


class GitHubIntegrationResponse(BaseModel):
    integration_id: str
    repo_owner: str
    repo_name: str
    installation_id: str
    auto_scan_pr: bool
    auto_comment: bool
    scan_on_push: bool
    created_at: str
    last_scan: Optional[str]


class PRScanResult(BaseModel):
    integration_id: str
    pr_number: int
    commit_sha: str
    scan_id: str
    score: int
    vulnerabilities_count: int
    status: str


async def run_github_scan(integration: dict, pr_number: int, commit_sha: str, files_changed: List[str]) -> dict:
    """Run a scan on PR changes"""
    # Get code from GitHub
    async with httpx.AsyncClient() as client:
        # Get the commit diff
        url = f"https://api.github.com/repos/{integration['repo_owner']}/{integration['repo_name']}/commits/{commit_sha}"
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {integration.get('token')}" if integration.get('token') else None
        }
        
        # For now, return a placeholder - in production you'd fetch actual code
        return {
            "scan_id": f"gh_{secrets.token_urlsafe(8)}",
            "pr_number": pr_number,
            "commit_sha": commit_sha,
            "files_changed": files_changed,
            "score": 85,
            "vulnerabilities": []
        }


async def comment_on_pr(integration: dict, pr_number: int, scan_result: dict):
    """Comment scan results on PR"""
    if not integration.get('auto_comment'):
        return
    
    comment_body = f"""
## 🔒 DevGuardian AI Security Scan

**Security Score:** {scan_result['score']}/100

**Vulnerabilities Found:** {len(scan_result.get('vulnerabilities', []))}

{'✅ No security issues detected!' if scan_result['score'] >= 80 else '⚠️ Please review the security issues above.'}

---
*Scanned by DevGuardian AI* | [View Full Report](https://devguardian.ai/scans/{scan_result['scan_id']})
"""
    
    # In production, this would post to GitHub API


@router.post("/integrations")
async def create_github_integration(
    integration: GitHubIntegrationCreate,
    current_user: TokenData = Depends(get_current_user)
):
    """Create a GitHub integration"""
    integration_id = f"ghi_{secrets.token_urlsafe(8)}"
    
    integration_data = {
        "integration_id": integration_id,
        "user_id": current_user.user_id,
        "repo_owner": integration.repo_owner,
        "repo_name": integration.repo_name,
        "installation_id": integration.installation_id,
        "auto_scan_pr": integration.auto_scan_pr,
        "auto_comment": integration.auto_comment,
        "scan_on_push": integration.scan_on_push,
        "created_at": datetime.now().isoformat(),
        "last_scan": None,
        "token": None,  # Would be set via OAuth
    }
    
    github_integrations_db[integration_id] = integration_data
    
    return integration_data


@router.get("/integrations")
async def list_github_integrations(current_user: TokenData = Depends(get_current_user)):
    """List all GitHub integrations"""
    user_integrations = [
        i for i in github_integrations_db.values() 
        if i["user_id"] == current_user.user_id
    ]
    return user_integrations


@router.get("/integrations/{integration_id}")
async def get_github_integration(
    integration_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Get a specific GitHub integration"""
    integration = github_integrations_db.get(integration_id)
    if not integration or integration["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Integration not found")
    return integration


@router.delete("/integrations/{integration_id}")
async def delete_github_integration(
    integration_id: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Delete a GitHub integration"""
    integration = github_integrations_db.get(integration_id)
    if not integration or integration["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    del github_integrations_db[integration_id]
    return {"message": "Integration deleted"}


@router.post("/webhook")
async def github_webhook(
    request: Request,
    background_tasks: BackgroundTasks,
    x_github_event: str = None,
    x_hub_signature_256: str = None
):
    """Handle GitHub webhook events"""
    payload = await request.json()
    
    # Handle different event types
    if x_github_event == "pull_request":
        await handle_pull_request(payload, background_tasks)
    elif x_github_event == "push":
        await handle_push(payload, background_tasks)
    elif x_github_event == "check_run":
        await handle_check_run(payload)
    
    return {"status": "received"}


async def handle_pull_request(payload: dict, background_tasks: BackgroundTasks):
    """Handle pull request events"""
    action = payload.get("action")
    if action not in ["opened", "synchronize", "ready_for_review"]:
        return
    
    pr = payload.get("pull_request", {})
    repo = payload.get("repository", {})
    
    # Find matching integration
    integration = None
    for i in github_integrations_db.values():
        if i["repo_owner"] == repo.get("owner", {}).get("login") and i["repo_name"] == repo.get("name"):
            integration = i
            break
    
    if not integration or not integration.get("auto_scan_pr"):
        return
    
    pr_number = pr.get("number")
    commit_sha = pr.get("head", {}).get("sha")
    
    # Get changed files
    files_changed = []
    if pr.get("changed_files"):
        files_changed = list(pr.get("changed_files", []))[:10]  # Limit to 10 files
    
    # Schedule scan in background
    background_tasks.add_task(
        run_pr_scan,
        integration,
        pr_number,
        commit_sha,
        files_changed
    )


async def handle_push(payload: dict, background_tasks: BackgroundTasks):
    """Handle push events"""
    repo = payload.get("repository", {})
    commits = payload.get("commits", [])
    
    # Find matching integration
    integration = None
    for i in github_integrations_db.values():
        if i["repo_owner"] == repo.get("owner", {}).get("login") and i["repo_name"] == repo.get("name"):
            integration = i
            break
    
    if not integration or not integration.get("scan_on_push"):
        return
    
    for commit in commits:
        background_tasks.add_task(
            run_commit_scan,
            integration,
            commit.get("id"),
            commit.get("added", []) + commit.get("modified", [])
        )


async def handle_check_run(payload: dict):
    """Handle GitHub Check Run events"""
    # Could be used for status checks
    pass


async def run_pr_scan(integration: dict, pr_number: int, commit_sha: str, files_changed: List[str]):
    """Run scan on PR and comment results"""
    try:
        result = await run_github_scan(integration, pr_number, commit_sha, files_changed)
        
        # Update last scan time
        integration["last_scan"] = datetime.now().isoformat()
        
        # Comment on PR if enabled
        if integration.get("auto_comment"):
            await comment_on_pr(integration, pr_number, result)
            
    except Exception as e:
        print(f"PR scan failed: {e}")


async def run_commit_scan(integration: dict, commit_sha: str, files_changed: List[str]):
    """Run scan on push"""
    try:
        await run_github_scan(integration, 0, commit_sha, files_changed)
        integration["last_scan"] = datetime.now().isoformat()
    except Exception as e:
        print(f"Commit scan failed: {e}")


@router.post("/scan")
async def trigger_github_scan(
    integration_id: str,
    pr_number: int,
    commit_sha: str,
    current_user: TokenData = Depends(get_current_user)
):
    """Manually trigger a GitHub PR scan"""
    integration = github_integrations_db.get(integration_id)
    if not integration or integration["user_id"] != current_user.user_id:
        raise HTTPException(status_code=404, detail="Integration not found")
    
    result = await run_github_scan(integration, pr_number, commit_sha, [])
    return result
