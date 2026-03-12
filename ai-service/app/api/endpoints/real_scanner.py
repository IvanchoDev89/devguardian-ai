"""
Real Security Scanner API Endpoints
Uses actual SAST tools: Semgrep, Bandit, npm audit, pip-audit
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import logging
from datetime import datetime
import uuid
import json

from app.scanners.real_security_scanner import create_real_scanner, RealSecurityScanner
from app.database import get_db, RealScan, RealVulnerability, User
from app.core.auth import get_current_user_optional, get_current_user, TokenData

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/security", tags=["Real Security Scanner"])
security = HTTPBearer(auto_error=False)

# Initialize real scanner
scanner = create_real_scanner()


class CodeScanRequest(BaseModel):
    code: str = Field(..., min_length=1, max_length=50000)
    language: str = Field(default="python")


class RepoScanRequest(BaseModel):
    repo_url: str
    provider: str = "github"
    branch: str = "main"


class ScanResponse(BaseModel):
    scan_id: str
    vulnerabilities: List[Dict[str, Any]]
    total_vulnerabilities: int
    score: int
    tools_used: List[str]
    language: Optional[str] = None
    scan_type: str
    timestamp: str
    repo_url: Optional[str] = None


class ScannerStatus(BaseModel):
    semgrep: bool
    bandit: bool
    git: bool
    available_tools: List[str]


@router.get("/scanner/status", response_model=ScannerStatus)
async def get_scanner_status():
    """Check which security tools are available"""
    return ScannerStatus(
        semgrep=scanner.tools.get('semgrep', False),
        bandit=scanner.tools.get('bandit', False),
        git=scanner.tools.get('git', False),
        available_tools=[k for k, v in scanner.tools.items() if v]
    )


@router.post("/scan/code", response_model=ScanResponse)
async def scan_code_real(
    request: CodeScanRequest,
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """
    Scan code using real SAST tools (Semgrep, Bandit)
    """
    scan_id = str(uuid.uuid4())[:12]
    user_id = current_user.user_id if current_user else "anonymous"
    
    logger.info(f"Starting real SAST scan for {request.language}")
    
    try:
        start_time = datetime.utcnow()
        result = scanner.scan_code(request.code, request.language)
        
        # Count severities
        critical = sum(1 for v in result['vulnerabilities'] if v.get('severity') == 'critical')
        high = sum(1 for v in result['vulnerabilities'] if v.get('severity') == 'high')
        medium = sum(1 for v in result['vulnerabilities'] if v.get('severity') == 'medium')
        low = sum(1 for v in result['vulnerabilities'] if v.get('severity') == 'low')
        
        # Save to database
        db = next(get_db())
        try:
            db_scan = RealScan(
                scan_id=scan_id,
                user_id=user_id,
                scan_type='code',
                language=request.language,
                score=result['score'],
                total_vulnerabilities=result['total_vulnerabilities'],
                critical_count=critical,
                high_count=high,
                medium_count=medium,
                low_count=low,
                tools_used=json.dumps(result.get('tools_used', [])),
                status='completed',
                duration_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                completed_at=datetime.utcnow()
            )
            db.add(db_scan)
            
            # Save vulnerabilities
            for vuln in result['vulnerabilities']:
                db_vuln = RealVulnerability(
                    scan_id=scan_id,
                    vulnerability_type=vuln.get('vulnerability_type', 'unknown'),
                    severity=vuln.get('severity', 'medium'),
                    description=vuln.get('description', ''),
                    file_path=vuln.get('file_path'),
                    line_number=vuln.get('line_number'),
                    line_content=vuln.get('line_content'),
                    match=vuln.get('match'),
                    cwe_id=vuln.get('cwe_id'),
                    owasp_category=vuln.get('owasp_category'),
                    tool=vuln.get('tool', 'semgrep'),
                    confidence=vuln.get('confidence')
                )
                db.add(db_vuln)
            
            db.commit()
            logger.info(f"Scan {scan_id} saved to database")
        except Exception as db_err:
            logger.error(f"Failed to save scan: {db_err}")
            db.rollback()
        
        response = ScanResponse(
            scan_id=scan_id,
            vulnerabilities=result['vulnerabilities'],
            total_vulnerabilities=result['total_vulnerabilities'],
            score=result['score'],
            tools_used=result.get('tools_used', []),
            language=request.language,
            scan_type=result.get('scan_type', 'real_sast'),
            timestamp=datetime.utcnow().isoformat()
        )
        
        logger.info(f"Scan {scan_id} completed: {response.total_vulnerabilities} vulns, score: {response.score}")
        return response
        
    except Exception as e:
        logger.error(f"Scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@router.post("/scan/repository", response_model=ScanResponse)
async def scan_repository_real(
    request: RepoScanRequest,
    background_tasks: BackgroundTasks,
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """
    Clone and scan a repository using real SAST tools
    Supports GitHub, GitLab, Bitbucket
    """
    scan_id = str(uuid.uuid4())[:12]
    user_id = current_user.user_id if current_user else "anonymous"
    
    logger.info(f"Starting repository scan: {request.repo_url}")
    
    # Validate URL
    if not request.repo_url.startswith(('http://', 'https://', 'git@')):
        raise HTTPException(status_code=400, detail="Invalid repository URL")
    
    start_time = datetime.utcnow()
    
    try:
        result = scanner.scan_repository(request.repo_url, request.provider)
        
        if 'error' in result and 'vulnerabilities' not in result:
            raise HTTPException(status_code=400, detail=result['error'])
        
        vulns = result.get('vulnerabilities', [])
        
        # Count severities
        critical = sum(1 for v in vulns if v.get('severity') == 'critical')
        high = sum(1 for v in vulns if v.get('severity') == 'high')
        medium = sum(1 for v in vulns if v.get('severity') == 'medium')
        low = sum(1 for v in vulns if v.get('severity') == 'low')
        
        # Save to database
        db = next(get_db())
        try:
            db_scan = RealScan(
                scan_id=scan_id,
                user_id=user_id,
                repo_url=request.repo_url,
                provider=request.provider,
                branch=request.branch,
                scan_type='repository',
                score=result.get('score', 100),
                total_vulnerabilities=len(vulns),
                critical_count=critical,
                high_count=high,
                medium_count=medium,
                low_count=low,
                tools_used=json.dumps(result.get('tools_used', [])),
                status='completed',
                duration_ms=int((datetime.utcnow() - start_time).total_seconds() * 1000),
                completed_at=datetime.utcnow()
            )
            db.add(db_scan)
            
            # Save vulnerabilities
            for vuln in vulns:
                db_vuln = RealVulnerability(
                    scan_id=scan_id,
                    vulnerability_type=vuln.get('vulnerability_type', 'unknown'),
                    severity=vuln.get('severity', 'medium'),
                    description=vuln.get('description', ''),
                    file_path=vuln.get('file_path'),
                    line_number=vuln.get('line_number'),
                    line_content=vuln.get('line_content'),
                    match=vuln.get('match'),
                    cwe_id=vuln.get('cwe_id'),
                    tool=vuln.get('tool', 'semgrep')
                )
                db.add(db_vuln)
            
            db.commit()
        except Exception as db_err:
            logger.error(f"Failed to save scan: {db_err}")
            db.rollback()
        
        response = ScanResponse(
            scan_id=scan_id,
            vulnerabilities=vulns,
            total_vulnerabilities=len(vulns),
            score=result.get('score', 100),
            tools_used=result.get('tools_used', []),
            scan_type=result.get('scan_type', 'repo_scan'),
            timestamp=datetime.utcnow().isoformat(),
            repo_url=request.repo_url
        )
        
        logger.info(f"Repo scan {scan_id}: {response.total_vulnerabilities} vulns, score: {response.score}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Repository scan failed: {e}")
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@router.get("/tools")
async def list_available_tools():
    """List all available security scanning tools"""
    return {
        "tools": [
            {
                "name": "semgrep",
                "description": "Multi-language static analysis engine",
                "languages": ["python", "javascript", "typescript", "java", "go", "rust", "c", "cpp", "csharp", "php", "ruby"],
                "available": scanner.tools.get('semgrep', False)
            },
            {
                "name": "bandit",
                "description": "Python security issues scanner",
                "languages": ["python"],
                "available": scanner.tools.get('bandit', False)
            },
            {
                "name": "npm audit",
                "description": "JavaScript/Node.js dependency vulnerability scanner",
                "available": True  # Checked at runtime
            },
            {
                "name": "pip-audit",
                "description": "Python dependency vulnerability scanner",
                "available": True  # Checked at runtime
            },
            {
                "name": "bundle-audit",
                "description": "Ruby dependency vulnerability scanner",
                "available": True  # Checked at runtime
            }
        ]
    }


@router.get("/scans")
async def list_real_scans(
    limit: int = 20,
    offset: int = 0,
    scan_type: Optional[str] = None,
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """List user's real security scans"""
    user_id = current_user.user_id if current_user else None
    
    db = next(get_db())
    try:
        query = db.query(RealScan)
        
        if user_id:
            query = query.filter(RealScan.user_id == user_id)
        
        if scan_type:
            query = query.filter(RealScan.scan_type == scan_type)
        
        total = query.count()
        scans = query.order_by(RealScan.created_at.desc()).offset(offset).limit(limit).all()
        
        return {
            "scans": [
                {
                    "scan_id": s.scan_id,
                    "repo_url": s.repo_url,
                    "scan_type": s.scan_type,
                    "language": s.language,
                    "score": s.score,
                    "total_vulnerabilities": s.total_vulnerabilities,
                    "critical_count": s.critical_count,
                    "high_count": s.high_count,
                    "medium_count": s.medium_count,
                    "low_count": s.low_count,
                    "tools_used": json.loads(s.tools_used) if s.tools_used else [],
                    "status": s.status,
                    "created_at": s.created_at.isoformat() if s.created_at else None,
                    "completed_at": s.completed_at.isoformat() if s.completed_at else None,
                    "duration_ms": s.duration_ms
                }
                for s in scans
            ],
            "total": total,
            "limit": limit,
            "offset": offset
        }
    finally:
        db.close()


@router.get("/scans/{scan_id}")
async def get_real_scan_details(
    scan_id: str,
    current_user: Optional[TokenData] = Depends(get_current_user_optional)
):
    """Get detailed scan results including vulnerabilities"""
    user_id = current_user.user_id if current_user else None
    
    db = next(get_db())
    try:
        scan = db.query(RealScan).filter(RealScan.scan_id == scan_id).first()
        
        if not scan:
            raise HTTPException(status_code=404, detail="Scan not found")
        
        # Allow if user owns scan or is admin
        if user_id and scan.user_id != user_id and current_user.role != 'admin':
            raise HTTPException(status_code=403, detail="Access denied")
        
        vulnerabilities = db.query(RealVulnerability).filter(
            RealVulnerability.scan_id == scan_id
        ).all()
        
        return {
            "scan": {
                "scan_id": scan.scan_id,
                "user_id": scan.user_id,
                "repo_url": scan.repo_url,
                "provider": scan.provider,
                "scan_type": scan.scan_type,
                "language": scan.language,
                "score": scan.score,
                "total_vulnerabilities": scan.total_vulnerabilities,
                "critical_count": scan.critical_count,
                "high_count": scan.high_count,
                "medium_count": scan.medium_count,
                "low_count": scan.low_count,
                "tools_used": json.loads(scan.tools_used) if scan.tools_used else [],
                "status": scan.status,
                "error_message": scan.error_message,
                "created_at": scan.created_at.isoformat() if scan.created_at else None,
                "completed_at": scan.completed_at.isoformat() if scan.completed_at else None,
                "duration_ms": scan.duration_ms
            },
            "vulnerabilities": [
                {
                    "id": v.id,
                    "vulnerability_type": v.vulnerability_type,
                    "severity": v.severity,
                    "description": v.description,
                    "file_path": v.file_path,
                    "line_number": v.line_number,
                    "line_content": v.line_content,
                    "cwe_id": v.cwe_id,
                    "owasp_category": v.owasp_category,
                    "tool": v.tool,
                    "confidence": v.confidence,
                    "status": v.status,
                    "false_positive": v.false_positive,
                    "discovered_at": v.discovered_at.isoformat() if v.discovered_at else None
                }
                for v in vulnerabilities
            ]
        }
    finally:
        db.close()


@router.get("/admin/stats")
async def get_admin_stats(
    current_user: TokenData = Depends(get_current_user)
):
    """Get admin statistics for real scanner"""
    if current_user.role != 'admin':
        raise HTTPException(status_code=403, detail="Admin access required")
    
    db = next(get_db())
    try:
        total_scans = db.query(RealScan).count()
        total_vulns = db.query(RealVulnerability).count()
        
        # Severity breakdown
        critical = db.query(RealVulnerability).filter(RealVulnerability.severity == 'critical').count()
        high = db.query(RealVulnerability).filter(RealVulnerability.severity == 'high').count()
        medium = db.query(RealVulnerability).filter(RealVulnerability.severity == 'medium').count()
        low = db.query(RealVulnerability).filter(RealVulnerability.severity == 'low').count()
        
        # Recent scans
        recent = db.query(RealScan).order_by(RealScan.created_at.desc()).limit(10).all()
        
        # Unique users
        unique_users = db.query(RealScan.user_id).distinct().count()
        
        return {
            "total_scans": total_scans,
            "total_vulnerabilities": total_vulns,
            "severity_breakdown": {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },
            "unique_users": unique_users,
            "recent_scans": [
                {
                    "scan_id": s.scan_id,
                    "user_id": s.user_id,
                    "scan_type": s.scan_type,
                    "score": s.score,
                    "total_vulnerabilities": s.total_vulnerabilities,
                    "created_at": s.created_at.isoformat() if s.created_at else None
                }
                for s in recent
            ]
        }
    finally:
        db.close()
