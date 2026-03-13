"""
Secret Scanner API Endpoints
Detect exposed API keys, tokens, and credentials
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import uuid

from app.scanners.secret_scanner import create_secret_scanner, SecretScanner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/secrets", tags=["Secret Scanner"])

scanner = create_secret_scanner()


class SecretScanRequest(BaseModel):
    code: str = Field(..., max_length=100000)
    filename: Optional[str] = None


class SecretFindingResponse(BaseModel):
    type: str
    severity: str
    line_number: int
    line_content: str
    match: str
    description: str
    remediation: str


class SecretScanResponse(BaseModel):
    scan_id: str
    total_secrets: int
    critical: int
    high: int
    medium: int
    low: int
    findings: List[SecretFindingResponse]
    timestamp: str
    recommendation: str


@router.post("/scan", response_model=SecretScanResponse)
async def scan_for_secrets(request: SecretScanRequest):
    """
    Scan code for exposed secrets, API keys, and credentials
    """
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Starting secret scan {scan_id}")
    
    try:
        # Scan the code
        findings = scanner.scan_content(
            request.code, 
            request.filename or "code snippet"
        )
        
        # Count by severity
        critical = sum(1 for f in findings if f.severity == "critical")
        high = sum(1 for f in findings if f.severity == "high")
        medium = sum(1 for f in findings if f.severity == "medium")
        low = sum(1 for f in findings if f.severity == "low")
        
        logger.info(f"Scan {scan_id}: Found {len(findings)} secrets")
        
        return SecretScanResponse(
            scan_id=scan_id,
            total_secrets=len(findings),
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            findings=[
                SecretFindingResponse(
                    type=f.type,
                    severity=f.severity,
                    line_number=f.line_number,
                    line_content=f.line_content,
                    match=f.match,
                    description=f.description,
                    remediation=f.remediation
                )
                for f in findings
            ],
            timestamp=datetime.utcnow().isoformat(),
            recommendation="Immediately rotate all exposed credentials" if findings else "No secrets detected"
        )
        
    except Exception as e:
        logger.error(f"Secret scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@router.get("/patterns")
async def get_secret_patterns():
    """Get list of secret patterns being detected"""
    return {
        "patterns": [
            {
                "type": key,
                "description": config["description"],
                "severity": config["severity"]
            }
            for key, config in scanner.PATTERNS.items()
        ],
        "total_patterns": len(scanner.PATTERNS)
    }


@router.post("/scan/file")
async def scan_file_for_secrets(
    background_tasks: BackgroundTasks,
    repo_url: str,
    branch: str = "main"
):
    """
    Scan a repository for secrets (background task)
    """
    import tempfile
    import subprocess
    
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Starting repository secret scan {scan_id}: {repo_url}")
    
    try:
        # Clone repository
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', '--branch', branch, repo_url, tmpdir],
                capture_output=True,
                timeout=120
            )
            
            if result.returncode != 0:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Failed to clone repository: {result.stderr.decode()}"
                )
            
            # Scan directory
            findings = scanner.scan_directory(tmpdir)
            report = scanner.generate_report(findings)
            
            return {
                "scan_id": scan_id,
                "repo_url": repo_url,
                **report
            }
            
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Repository clone timeout")
    except Exception as e:
        logger.error(f"Secret scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
