"""
Compliance Reporting API Endpoints
Generate SOC2, ISO 27001, HIPAA, PCI-DSS reports
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime
import uuid

from app.scanners.compliance_reporter import create_compliance_reporter, ComplianceReporter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/compliance", tags=["Compliance"])

reporter = create_compliance_reporter()


class ComplianceRequest(BaseModel):
    framework: str = Field(..., description="soc2, iso27001, hipaa, pci_dss")
    project_name: str = Field(default="DevGuardian Project")
    vulnerabilities: List[Dict[str, Any]] = Field(default_factory=list)


class ComplianceResponse(BaseModel):
    report_id: str
    project_name: str
    framework: str
    version: str
    score: float
    compliance_level: str
    summary: Dict[str, int]
    controls: List[Dict]
    recommendations: List[str]
    generated_at: str


@router.post("/report", response_model=ComplianceResponse)
async def generate_compliance_report(request: ComplianceRequest):
    """
    Generate compliance report for a framework
    """
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Generating {request.framework} compliance report")
    
    try:
        # Validate framework
        valid_frameworks = list(reporter.FRAMEWORKS.keys())
        if request.framework not in valid_frameworks:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid framework. Choose from: {valid_frameworks}"
            )
        
        # Generate report
        report = reporter.generate_report(
            framework=request.framework,
            vulnerabilities=request.vulnerabilities,
            project_name=request.project_name
        )
        
        logger.info(f"Report {report['report_id']}: Score {report['score']}%")
        
        return ComplianceResponse(**report)
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Report generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/frameworks")
async def get_supported_frameworks():
    """Get supported compliance frameworks"""
    return {
        "frameworks": [
            {
                "id": key,
                "name": info["name"],
                "version": info["version"],
                "controls": len(info["controls"])
            }
            for key, info in reporter.FRAMEWORKS.items()
        ]
    }


@router.get("/frameworks/{framework}/controls")
async def get_framework_controls(framework: str):
    """Get controls for a specific framework"""
    if framework not in reporter.FRAMEWORKS:
        raise HTTPException(status_code=404, detail="Framework not found")
    
    return reporter.FRAMEWORKS[framework]
