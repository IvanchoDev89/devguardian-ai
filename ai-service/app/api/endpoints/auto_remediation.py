"""
Auto-Remediation API Endpoints
Automatically fix common security vulnerabilities
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import uuid

from app.scanners.auto_remediation import create_auto_remediator, AutoRemediator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/remediation", tags=["Auto Remediation"])

remediator = create_auto_remediator()


class RemediationScanRequest(BaseModel):
    code: str = Field(..., max_length=50000)
    language: str = Field(default="python")


class VulnerabilityFix(BaseModel):
    vulnerability_type: str
    severity: str
    line_number: int
    original_code: str
    explanation: str
    fix_suggestion: str
    confidence: float
    can_auto_fix: bool


class RemediationResponse(BaseModel):
    scan_id: str
    total_issues: int
    critical: int
    high: int
    medium: int
    low: int
    can_auto_fix: int
    fixes: List[VulnerabilityFix]
    timestamp: str


@router.post("/scan", response_model=RemediationResponse)
async def scan_for_remediation(request: RemediationScanRequest):
    """
    Analyze code and suggest fixes for vulnerabilities
    """
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Starting remediation scan {scan_id}")
    
    try:
        fixes = remediator.analyze(request.code, request.language)
        
        # Count by severity
        critical = sum(1 for f in fixes if f["severity"] == "critical")
        high = sum(1 for f in fixes if f["severity"] == "high")
        medium = sum(1 for f in fixes if f["severity"] == "medium")
        low = sum(1 for f in fixes if f["severity"] == "low")
        can_fix = sum(1 for f in fixes if f["can_auto_fix"])
        
        logger.info(f"Scan {scan_id}: Found {len(fixes)} issues, {can_fix} auto-fixable")
        
        return RemediationResponse(
            scan_id=scan_id,
            total_issues=len(fixes),
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            can_auto_fix=can_fix,
            fixes=[
                VulnerabilityFix(
                    vulnerability_type=f["vulnerability_type"],
                    severity=f["severity"],
                    line_number=f["line_number"],
                    original_code=f["original_code"],
                    explanation=f["explanation"],
                    fix_suggestion=f["fix_suggestion"],
                    confidence=f["confidence"],
                    can_auto_fix=f["can_auto_fix"]
                )
                for f in fixes
            ],
            timestamp=datetime.utcnow().isoformat()
        )
        
    except Exception as e:
        logger.error(f"Remediation scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/rules")
async def get_remediation_rules():
    """
    Get all remediation rules
    """
    return {
        "rules": [
            {
                "type": vuln_type,
                "description": info.get("fix", "No description"),
                "can_auto_fix": bool(info.get("template"))
            }
            for vuln_type, info in remediator.RULES.items()
        ],
        "total_rules": len(remediator.RULES)
    }


@router.post("/fix/{vulnerability_type}")
async def generate_fix(
    code: str,
    vulnerability_type: str
):
    """
    Generate specific fix for a vulnerability type
    """
    try:
        fix = remediator.generate_fix(code, vulnerability_type)
        if not fix:
            raise HTTPException(
                status_code=404,
                detail=f"No fix available for {vulnerability_type}"
            )
        return fix
    except Exception as e:
        logger.error(f"Fix generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
