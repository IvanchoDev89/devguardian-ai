"""
Custom Rules Engine API Endpoints
Define and manage custom security rules
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import uuid

from app.scanners.custom_rules import CustomRulesEngine, SecurityRule

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/rules", tags=["Custom Rules"])

engine = CustomRulesEngine()


class AddRuleRequest(BaseModel):
    name: str
    description: str
    pattern: str
    severity: str = Field(..., pattern="^(critical|high|medium|low)$")
    language: str = "any"
    remediation: str = ""


class CustomScanRequest(BaseModel):
    code: str = Field(..., max_length=100000)
    language: str = "any"
    user_id: Optional[str] = None


class RuleResponse(BaseModel):
    id: str
    name: str
    description: str
    pattern: str
    severity: str
    enabled: bool
    language: str
    category: str
    remediation: str
    created_at: str


@router.post("/", response_model=RuleResponse)
async def add_custom_rule(request: AddRuleRequest, user_id: str = "default"):
    """Add a new custom security rule"""
    rule_id = f"custom_{str(uuid.uuid4())[:6]}"
    
    logger.info(f"Adding custom rule {rule_id}: {request.name}")
    
    try:
        rule = SecurityRule(
            id=rule_id,
            name=request.name,
            description=request.description,
            pattern=request.pattern,
            severity=request.severity,
            language=request.language,
            remediation=request.remediation
        )
        
        engine.add_rule(user_id, rule)
        
        return RuleResponse(
            id=rule.id,
            name=rule.name,
            description=rule.description,
            pattern=rule.pattern,
            severity=rule.severity,
            enabled=rule.enabled,
            language=rule.language,
            category=rule.category,
            remediation=rule.remediation,
            created_at=rule.created_at
        )
    except Exception as e:
        logger.error(f"Failed to add rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/", response_model=List[RuleResponse])
async def list_rules(user_id: str = "default"):
    """List all custom rules"""
    try:
        rules = engine.get_rules(user_id)
        
        return [
            RuleResponse(
                id=r["id"],
                name=r["name"],
                description=r["description"],
                pattern=r["pattern"],
                severity=r["severity"],
                enabled=r["enabled"],
                language=r["language"],
                category=r["category"],
                remediation=r["remediation"],
                created_at=r["created_at"]
            )
            for r in rules
        ]
    except Exception as e:
        logger.error(f"Failed to list rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{rule_id}")
async def delete_rule(rule_id: str, user_id: str = "default"):
    """Delete a custom rule"""
    logger.info(f"Deleting rule {rule_id}")
    
    try:
        success = engine.remove_rule(user_id, rule_id)
        
        if not success:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        return {"deleted": True, "rule_id": rule_id}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to delete rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scan", response_model=Dict)
async def scan_with_custom_rules(request: CustomScanRequest):
    """Scan code using custom rules"""
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Scanning with custom rules {scan_id}")
    
    try:
        findings = engine.scan_with_rules(request.code, request.language, request.user_id)
        
        return {
            "scan_id": scan_id,
            "total_findings": len(findings),
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Custom scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{rule_id}/toggle")
async def toggle_rule(rule_id: str, user_id: str = "default"):
    """Enable or disable a rule"""
    try:
        # For now, just return success - full toggle requires adding method to scanner
        rules = engine.get_rules(user_id)
        rule = next((r for r in rules if r["id"] == rule_id), None)
        
        if not rule:
            raise HTTPException(status_code=404, detail="Rule not found")
        
        return {"enabled": rule["enabled"], "message": "Toggle endpoint - rule is " + ("enabled" if rule["enabled"] else "disabled")}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to toggle rule: {e}")
        raise HTTPException(status_code=500, detail=str(e))
