"""
SBOM Generator API Endpoints
Software Bill of Materials generation
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
import logging
from datetime import datetime
import uuid

from app.scanners.sbom_generator import create_sbom_generator, SBOMGenerator

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/sbom", tags=["SBOM Generator"])

scanner = create_sbom_generator()


class SBOMScanRequest(BaseModel):
    repo_url: str
    branch: str = "main"
    format: str = "cyclonedx"  # cyclonedx, spdx


class SBOMResponse(BaseModel):
    scan_id: str
    total_dependencies: int
    by_ecosystem: Dict[str, int]
    sbom: Dict[str, Any]
    format: str
    timestamp: str


@router.post("/generate", response_model=SBOMResponse)
async def generate_sbom(request: SBOMScanRequest):
    """
    Generate Software Bill of Materials for a repository
    """
    import tempfile
    import subprocess
    
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Generating SBOM for {request.repo_url}")
    
    try:
        # Clone repository
        with tempfile.TemporaryDirectory() as tmpdir:
            result = subprocess.run(
                ['git', 'clone', '--depth', '1', '--branch', request.branch, request.repo_url, tmpdir],
                capture_output=True,
                timeout=120
            )
            
            if result.returncode != 0:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to clone repository"
                )
            
            # Scan for dependencies
            dependencies = scanner.scan_directory(tmpdir)
            
            # Generate SBOM in requested format
            if request.format == "spdx":
                sbom = scanner.generate_spdx()
            else:
                sbom = scanner.generate_cyclonedx()
            
            summary = scanner.generate_summary()
            
            logger.info(f"Scan {scan_id}: Found {len(dependencies)} dependencies")
            
            return SBOMResponse(
                scan_id=scan_id,
                total_dependencies=len(dependencies),
                by_ecosystem=summary["by_ecosystem"],
                sbom=sbom,
                format=request.format,
                timestamp=datetime.utcnow().isoformat()
            )
            
    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Repository clone timeout")
    except Exception as e:
        logger.error(f"SBOM generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/formats")
async def get_supported_formats():
    """Get supported SBOM formats"""
    return {
        "formats": [
            {
                "id": "cyclonedx",
                "name": "CycloneDX",
                "version": "1.4",
                "description": "OWASP CycloneDX - Modern SBOM standard"
            },
            {
                "id": "spdx",
                "name": "SPDX",
                "version": "2.3",
                "description": "Software Package Data Exchange - ISO standard"
            }
        ]
    }


@router.get("/ecosystems")
async def get_supported_ecosystems():
    """Get supported package ecosystems"""
    return {
        "ecosystems": list(scanner.PACKAGE_FILES.keys()),
        "files": scanner.PACKAGE_FILES
    }
