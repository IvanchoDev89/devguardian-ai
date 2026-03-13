"""
Cloud Security Scanner API Endpoints
Scan AWS, Azure, GCP, Kubernetes, Docker configurations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import uuid

from app.scanners.cloud_scanner import CloudSecurityScanner

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/cloud", tags=["Cloud Scanner"])

scanner = CloudSecurityScanner()


class CloudScanRequest(BaseModel):
    config: str = Field(..., max_length=100000)
    provider: str = Field(..., pattern="^(aws|azure|gcp|k8s|docker)$")


class CloudScanResponse(BaseModel):
    scan_id: str
    provider: str
    total_issues: int
    critical: int
    high: int
    medium: int
    low: int
    findings: List[Dict[str, Any]]
    timestamp: str
    recommendation: str


@router.post("/scan", response_model=CloudScanResponse)
async def scan_cloud_config(request: CloudScanRequest):
    """Scan cloud configuration for security issues"""
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Scanning {request.provider} config {scan_id}")
    
    try:
        if request.provider == "aws":
            findings = scanner.scan_terraform(request.config)
        elif request.provider == "azure":
            findings = scanner.scan_terraform(request.config)
        elif request.provider == "gcp":
            findings = scanner.scan_terraform(request.config)
        elif request.provider == "k8s":
            findings = scanner.scan_kubernetes(request.config)
        elif request.provider == "docker":
            findings = scanner.scan_docker_compose(request.config)
        else:
            findings = []
        
        critical = sum(1 for f in findings if f.get("severity") == "critical")
        high = sum(1 for f in findings if f.get("severity") == "high")
        medium = sum(1 for f in findings if f.get("severity") == "medium")
        low = sum(1 for f in findings if f.get("severity") == "low")
        
        return CloudScanResponse(
            scan_id=scan_id,
            provider=request.provider,
            total_issues=len(findings),
            critical=critical,
            high=high,
            medium=medium,
            low=low,
            findings=findings,
            timestamp=datetime.utcnow().isoformat(),
            recommendation="Review and fix critical issues immediately" if critical > 0 else "No critical issues found"
        )
    except Exception as e:
        logger.error(f"Cloud scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/providers")
async def get_supported_providers():
    """Get list of supported cloud providers"""
    return {
        "providers": [
            {"id": "aws", "name": "Amazon Web Services"},
            {"id": "azure", "name": "Microsoft Azure"},
            {"id": "gcp", "name": "Google Cloud Platform"},
            {"id": "k8s", "name": "Kubernetes"},
            {"id": "docker", "name": "Docker"}
        ],
        "total": 5
    }


@router.get("/rules/{provider}")
async def get_cloud_rules(provider: str):
    """Get security rules for a specific provider"""
    try:
        rules = []
        if provider == "aws":
            rules = scanner.AWS_RULES
        elif provider == "azure":
            rules = scanner.AZURE_RULES
        elif provider == "gcp":
            rules = scanner.GCP_RULES
        elif provider == "k8s":
            rules = scanner.K8S_RULES
            
        return {
            "provider": provider,
            "rules": rules,
            "total": len(rules)
        }
    except Exception as e:
        logger.error(f"Failed to get rules: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/scan/file")
async def scan_cloud_file(
    provider: str,
    file_content: str
):
    """Scan a cloud configuration file"""
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Scanning cloud file {scan_id}")
    
    try:
        if provider == "aws":
            findings = scanner.scan_terraform(file_content)
        elif provider == "azure":
            findings = scanner.scan_terraform(file_content)
        elif provider == "gcp":
            findings = scanner.scan_terraform(file_content)
        elif provider == "k8s":
            findings = scanner.scan_kubernetes(file_content)
        elif provider == "docker":
            findings = scanner.scan_docker_compose(file_content)
        else:
            findings = []
        
        return {
            "scan_id": scan_id,
            "provider": provider,
            "total_issues": len(findings),
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Cloud file scan failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))
