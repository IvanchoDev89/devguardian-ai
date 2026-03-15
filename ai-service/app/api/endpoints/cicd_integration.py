"""
Semgrep CI/CD Integration Endpoints
Handles PR scanning, pre-commit hooks, and policy enforcement
"""

from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
import uuid
import hashlib

router = APIRouter(prefix="/api/cicd", tags=["CI/CD Integration"])


class PRScanRequest(BaseModel):
    """Request to scan a pull request"""
    repository_url: str
    pr_number: int
    commit_sha: str
    branch: str
    base_branch: str
    files_changed: List[str]
    author: str
    github_token: Optional[str] = None


class PRScanResponse(BaseModel):
    """Response for PR scan"""
    scan_id: str
    pr_number: int
    commit_sha: str
    status: str
    score: int
    findings_count: int
    critical_findings: List[Dict[str, Any]]
    can_merge: bool
    block_reason: Optional[str]


class PreCommitScanRequest(BaseModel):
    """Request for pre-commit hook scan"""
    commit_sha: str
    branch: str
    files_changed: List[str]
    repository_url: str


class PreCommitResponse(BaseModel):
    """Response for pre-commit scan"""
    scan_id: str
    can_commit: bool
    block_reason: Optional[str]
    findings_count: int
    critical_findings: List[Dict[str, Any]]


class PolicyConfig(BaseModel):
    """Policy configuration for CI/CD"""
    policy_id: str
    name: str
    enabled: bool = True
    block_on_critical: bool = True
    block_on_high: bool = False
    block_on_medium: bool = False
    max_critical: int = 0
    max_high: int = 10
    max_medium: int = 50
    require_approval_for: List[str] = []  # ["critical", "high"]
    auto_remediate_severities: List[str] = []


class PolicyResponse(BaseModel):
    """Policy response"""
    policy_id: str
    name: str
    enabled: bool
    block_on_critical: bool
    block_on_high: bool
    can_merge: bool
    findings_count: int
    block_reason: Optional[str]


# In-memory policy storage
policies_db: Dict[str, PolicyConfig] = {
    "default": PolicyConfig(
        policy_id="default",
        name="Default Security Policy",
        enabled=True,
        block_on_critical=True,
        block_on_high=False,
        block_on_medium=False,
        max_critical=0,
        max_high=10,
        max_medium=50
    ),
    "strict": PolicyConfig(
        policy_id="strict",
        name="Strict Policy",
        enabled=False,
        block_on_critical=True,
        block_on_high=True,
        block_on_medium=True,
        max_critical=0,
        max_high=0,
        max_medium=0,
        require_approval_for=["critical", "high"]
    ),
    "compliance": PolicyConfig(
        policy_id="compliance",
        name="Compliance Policy (SOC2/HIPAA)",
        enabled=False,
        block_on_critical=True,
        block_on_high=True,
        block_on_medium=False,
        max_critical=0,
        max_high=5,
        max_medium=25,
        require_approval_for=["critical"]
    )
}

# Scan results storage
pr_scans: Dict[str, Dict[str, Any]] = {}


def _check_policy(findings: List[Dict[str, Any]], policy: PolicyConfig) -> tuple[bool, Optional[str]]:
    """Check if findings violate policy"""
    by_severity = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    
    for f in findings:
        sev = f.get("severity", "medium").lower()
        by_severity[sev] = by_severity.get(sev, 0) + 1
    
    # Check critical
    if policy.block_on_critical and by_severity.get("critical", 0) > policy.max_critical:
        return False, f"Blocked: {by_severity['critical']} critical findings (max: {policy.max_critical})"
    
    # Check high
    if policy.block_on_high and by_severity.get("high", 0) > policy.max_high:
        return False, f"Blocked: {by_severity['high']} high findings (max: {policy.max_high})"
    
    # Check medium
    if policy.block_on_medium and by_severity.get("medium", 0) > policy.max_medium:
        return False, f"Blocked: {by_severity['medium']} medium findings (max: {policy.max_medium})"
    
    return True, None


def _calculate_security_score(findings: List[Dict[str, Any]]) -> int:
    """Calculate security score based on findings"""
    if not findings:
        return 100
    
    deductions = {
        "critical": 25,
        "high": 15,
        "medium": 5,
        "low": 1
    }
    
    score = 100
    for f in findings:
        sev = f.get("severity", "low").lower()
        score -= deductions.get(sev, 1)
    
    return max(0, score)


@router.post("/scan/pr", response_model=PRScanResponse)
async def scan_pull_request(
    request: PRScanRequest,
    background_tasks: BackgroundTasks,
    policy_id: str = "default"
):
    """
    Scan a pull request for security vulnerabilities
    
    This endpoint is designed to be called from CI/CD pipelines
    or GitHub Actions to scan PRs before merging.
    """
    scan_id = f"pr-scan-{uuid.uuid4().hex[:12]}"
    
    # Get policy
    policy = policies_db.get(policy_id, policies_db["default"])
    
    # Simulate findings (in production, run actual Semgrep scan)
    findings = _simulate_pr_scan(request.files_changed)
    critical_findings = [f for f in findings if f.get("severity") == "critical"]
    
    # Check policy
    can_merge, block_reason = _check_policy(findings, policy)
    score = _calculate_security_score(findings)
    
    result = {
        "scan_id": scan_id,
        "pr_number": request.pr_number,
        "commit_sha": request.commit_sha[:8],
        "status": "completed",
        "score": score,
        "findings_count": len(findings),
        "critical_findings": critical_findings[:5],  # Top 5 critical
        "can_merge": can_merge,
        "block_reason": block_reason,
        "repository": request.repository_url,
        "branch": request.branch,
        "author": request.author,
        "policy": policy_id,
        "scanned_at": datetime.utcnow().isoformat()
    }
    
    pr_scans[scan_id] = result
    
    return PRScanResponse(**result)


@router.post("/scan/pre-commit", response_model=PreCommitResponse)
async def scan_pre_commit(request: PreCommitScanRequest):
    """
    Scan code before commit (pre-commit hook)
    
    Returns whether the commit is allowed based on findings.
    """
    scan_id = f"precommit-{uuid.uuid4().hex[:12]}"
    
    # Run scan on changed files
    findings = _simulate_pr_scan(request.files_changed)
    critical_findings = [f for f in findings if f.get("severity") == "critical"]
    
    # Strict policy for pre-commit
    policy = policies_db["strict"]
    can_commit, block_reason = _check_policy(findings, policy)
    
    result = {
        "scan_id": scan_id,
        "can_commit": can_commit and len(critical_findings) == 0,
        "block_reason": block_reason or ("Critical vulnerabilities found" if critical_findings else None),
        "findings_count": len(findings),
        "critical_findings": critical_findings[:3]
    }
    
    return PreCommitResponse(**result)


@router.get("/scan/{scan_id}")
async def get_scan_result(scan_id: str):
    """Get the result of a previous scan"""
    if scan_id not in pr_scans:
        raise HTTPException(status_code=404, detail="Scan not found")
    return pr_scans[scan_id]


@router.get("/policies")
async def list_policies():
    """List all available policies"""
    return [
        {
            "policy_id": p.policy_id,
            "name": p.name,
            "enabled": p.enabled,
            "block_on_critical": p.block_on_critical,
            "block_on_high": p.block_on_high,
            "block_on_medium": p.block_on_medium
        }
        for p in policies_db.values()
    ]


@router.post("/policies/{policy_id}/toggle")
async def toggle_policy(policy_id: str, enabled: bool):
    """Enable or disable a policy"""
    if policy_id not in policies_db:
        raise HTTPException(status_code=404, detail="Policy not found")
    
    policies_db[policy_id].enabled = enabled
    return {"policy_id": policy_id, "enabled": enabled}


@router.post("/policies")
async def create_policy(policy: PolicyConfig):
    """Create a new policy"""
    if policy.policy_id in policies_db:
        raise HTTPException(status_code=400, detail="Policy already exists")
    
    policies_db[policy.policy_id] = policy
    return {"message": "Policy created", "policy_id": policy.policy_id}


@router.get("/status")
async def get_cicd_status():
    """Get CI/CD integration status"""
    return {
        "status": "active",
        "policies_count": len(policies_db),
        "scans_today": len(pr_scans),
        "integrations": {
            "github_actions": "configured",
            "gitlab_ci": "available",
            "jenkins": "available",
            "pre_commit": "available"
        }
    }


def _simulate_pr_scan(files_changed: List[str]) -> List[Dict[str, Any]]:
    """Simulate finding vulnerabilities in PR (replace with real Semgrep)"""
    import random
    
    findings = []
    
    for file in files_changed:
        if file.endswith(".py"):
            if "query" in file.lower() or "db" in file.lower():
                findings.append({
                    "type": "sql-injection",
                    "severity": "critical",
                    "file": file,
                    "line": random.randint(10, 100),
                    "message": "SQL injection risk - use parameterized queries",
                    "cwe": "CWE-89"
                })
            if "eval(" in file or "exec(" in file:
                findings.append({
                    "type": "code-injection",
                    "severity": "high",
                    "file": file,
                    "line": random.randint(10, 50),
                    "message": "Dangerous function usage - potential code injection",
                    "cwe": "CWE-94"
                })
        elif file.endswith((".js", ".ts", ".jsx", ".tsx")):
            if "innerHTML" in file or "dangerouslySetInnerHTML" in file:
                findings.append({
                    "type": "xss",
                    "severity": "high",
                    "file": file,
                    "line": random.randint(10, 80),
                    "message": "Potential XSS vulnerability",
                    "cwe": "CWE-79"
                })
        elif file.endswith((".ts", ".tsx")):
            if "process.env" in file:
                findings.append({
                    "type": "secrets",
                    "severity": "critical",
                    "file": file,
                    "line": random.randint(1, 20),
                    "message": "Hardcoded environment variable detected",
                    "cwe": "CWE-798"
                })
    
    return findings
