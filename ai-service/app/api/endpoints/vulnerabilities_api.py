"""
Vulnerabilities API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from sqlalchemy.orm import Session
import uuid
import random

from app.database import get_db, Vulnerability, Scan

router = APIRouter(prefix="/api/v1", tags=["Vulnerabilities"])


class VulnerabilityResponse(BaseModel):
    id: int
    title: str
    description: str
    severity: str
    status: str
    file: str
    line_number: Optional[int] = None
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    discovered_at: str

    class Config:
        from_attributes = True


class VulnerabilityUpdate(BaseModel):
    status: Optional[str] = None
    assignee_id: Optional[str] = None
    notes: Optional[str] = None
    false_positive: Optional[bool] = None
    false_positive_reason: Optional[str] = None


def _get_severity_score(severity: str) -> int:
    scores = {"critical": 9, "high": 7, "medium": 5, "low": 3}
    return scores.get(severity.lower(), 5)


def _create_demo_data(db: Session):
    """Create demo vulnerabilities if database is empty"""
    try:
        existing = db.query(Vulnerability).first()
        if existing:
            return
    except Exception:
        pass
    
    # Get or create a demo scan
    scan = db.query(Scan).first()
    if not scan:
        scan = Scan(
            scan_id="demo-scan-001",
            user_id="demo-user",
            code="demo",
            language="python",
            score=75,
            total_vulnerabilities=0,
            status="completed"
        )
        db.add(scan)
        db.commit()
        db.refresh(scan)
    
    # Demo vulnerabilities
    vulns_data = [
        {"title": "SQL Injection", "severity": "critical", "cwe": "CWE-89", "file": "src/database/query_builder.py", "line": 45, "desc": "Unparameterized SQL query allows SQL injection attacks"},
        {"title": "XSS Reflected", "severity": "high", "cwe": "CWE-79", "file": "src/api/views.py", "line": 128, "desc": "User input reflected without sanitization"},
        {"title": "Command Injection", "severity": "critical", "cwe": "CWE-78", "file": "src/utils/shell.py", "line": 67, "desc": "Shell command built from user input"},
        {"title": "Path Traversal", "severity": "high", "cwe": "CWE-22", "file": "src/api/files.py", "line": 89, "desc": "File path not validated against traversal attacks"},
        {"title": "Insecure Deserialization", "severity": "critical", "cwe": "CWE-502", "file": "src/core/serializer.py", "line": 34, "desc": "Deserializing untrusted data"},
        {"title": "Broken Authentication", "severity": "high", "cwe": "CWE-287", "file": "src/auth/login.py", "line": 112, "desc": "Authentication mechanism bypassed"},
        {"title": "Sensitive Data Exposure", "severity": "medium", "cwe": "CWE-200", "file": "src/api/user.py", "line": 78, "desc": "Sensitive data exposed in response"},
        {"title": "Security Misconfiguration", "severity": "medium", "cwe": "CWE-16", "file": "config/settings.py", "line": 23, "desc": "Debug mode enabled in production"},
        {"title": "XXE Injection", "severity": "high", "cwe": "CWE-611", "file": "src/api/xml.py", "line": 56, "desc": "XML external entity processing enabled"},
        {"title": "CSRF Protection Missing", "severity": "medium", "cwe": "CWE-352", "file": "src/api/forms.py", "line": 41, "desc": "No CSRF tokens in forms"},
    ]
    
    for vuln_data in vulns_data:
        vuln = Vulnerability(
            scan_id=scan.scan_id,
            file=vuln_data["file"],
            line_number=vuln_data["line"],
            line_content=f"# Line {vuln_data['line']}",
            vulnerability_type=vuln_data["title"],
            severity=vuln_data["severity"],
            description=vuln_data["desc"],
            match=f"Vulnerability at line {vuln_data['line']}",
            cwe_id=vuln_data["cwe"],
            owasp_category="A1:2017-Injection" if vuln_data["severity"] == "critical" else "A3:2017-Sensitive Data Exposure",
            status="open",
            severity_score=_get_severity_score(vuln_data["severity"]),
            false_positive=False
        )
        db.add(vuln)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        print(f"Error creating demo data: {e}")


@router.get("/vulnerabilities", response_model=List[VulnerabilityResponse])
async def get_vulnerabilities(db: Session = Depends(get_db)):
    """Get all vulnerabilities"""
    _create_demo_data(db)
    vulnerabilities = db.query(Vulnerability).order_by(Vulnerability.discovered_at.desc()).all()
    
    return [
        VulnerabilityResponse(
            id=v.id,
            title=v.vulnerability_type,
            description=v.description,
            severity=v.severity,
            status=v.status,
            file=v.file or "unknown",
            line_number=v.line_number,
            cwe_id=v.cwe_id,
            cvss_score=float(v.severity_score) / 10 * 9 if v.severity_score else None,
            discovered_at=v.discovered_at.isoformat()
        )
        for v in vulnerabilities
    ]


@router.get("/vulnerabilities/{vuln_id}")
async def get_vulnerability(vuln_id: int, db: Session = Depends(get_db)):
    """Get a specific vulnerability"""
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    return {
        "id": vuln.id,
        "title": vuln.vulnerability_type,
        "description": vuln.description,
        "severity": vuln.severity,
        "status": vuln.status,
        "file": vuln.file,
        "line_number": vuln.line_number,
        "line_content": vuln.line_content,
        "cwe_id": vuln.cwe_id,
        "owasp_category": vuln.owasp_category,
        "cvss_score": float(vuln.severity_score) / 10 * 9 if vuln.severity_score else None,
        "discovered_at": vuln.discovered_at.isoformat(),
        "notes": vuln.notes,
        "false_positive": vuln.false_positive
    }


@router.put("/vulnerabilities/{vuln_id}")
async def update_vulnerability(vuln_id: int, data: VulnerabilityUpdate, db: Session = Depends(get_db)):
    """Update a vulnerability"""
    vuln = db.query(Vulnerability).filter(Vulnerability.id == vuln_id).first()
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    if data.status:
        vuln.status = data.status
        if data.status == "resolved":
            vuln.resolved_at = datetime.utcnow()
    
    if data.assignee_id is not None:
        vuln.assignee_id = data.assignee_id
    
    if data.notes is not None:
        vuln.notes = data.notes
    
    if data.false_positive is not None:
        vuln.false_positive = data.false_positive
        if data.false_positive and data.false_positive_reason:
            vuln.false_positive_reason = data.false_positive_reason
            vuln.status = "false_positive"
    
    db.commit()
    db.refresh(vuln)
    
    return {"message": "Vulnerability updated", "id": vuln.id, "status": vuln.status}


@router.get("/vulnerabilities/stats/summary")
async def get_vulnerabilities_summary(db: Session = Depends(get_db)):
    """Get vulnerability statistics summary"""
    _create_demo_data(db)
    
    total = db.query(Vulnerability).count()
    critical = db.query(Vulnerability).filter(Vulnerability.severity == "critical").count()
    high = db.query(Vulnerability).filter(Vulnerability.severity == "high").count()
    medium = db.query(Vulnerability).filter(Vulnerability.severity == "medium").count()
    low = db.query(Vulnerability).filter(Vulnerability.severity == "low").count()
    open_vulns = db.query(Vulnerability).filter(Vulnerability.status == "open").count()
    resolved = db.query(Vulnerability).filter(Vulnerability.status == "resolved").count()
    false_positive = db.query(Vulnerability).filter(Vulnerability.false_positive == True).count()
    
    return {
        "total": total,
        "by_severity": {
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low
        },
        "by_status": {
            "open": open_vulns,
            "resolved": resolved,
            "false_positive": false_positive
        },
        "critical_percentage": round(critical / total * 100, 1) if total > 0 else 0
    }
