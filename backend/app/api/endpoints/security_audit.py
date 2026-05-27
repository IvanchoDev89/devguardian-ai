from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Vulnerability, Scan

router = APIRouter(prefix="/api/security-audit", tags=["Security Audit"])


@router.get("/summary")
def get_security_audit_summary(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vulnerabilities = db.query(Vulnerability).filter(
        Vulnerability.owner_id == current_user.id
    ).all()
    
    total_scans = db.query(Scan).filter(
        Scan.owner_id == current_user.id
    ).count()
    
    critical = len([v for v in vulnerabilities if v.severity and v.severity.lower() == 'critical'])
    high = len([v for v in vulnerabilities if v.severity and v.severity.lower() == 'high'])
    medium = len([v for v in vulnerabilities if v.severity and v.severity.lower() == 'medium'])
    low = len([v for v in vulnerabilities if v.severity and v.severity.lower() == 'low'])
    
    open_vulns = len([v for v in vulnerabilities if v.status == 'open'])
    fixed_vulns = len([v for v in vulnerabilities if v.status == 'resolved'])
    
    total_weight = (critical * 15) + (high * 10) + (medium * 5) + (low * 2)
    security_score = max(0, min(100, 100 - total_weight))
    
    fix_rate = (fixed_vulns / len(vulnerabilities) * 100) if vulnerabilities else 0
    performance_score = min(100, int(fix_rate + (total_scans * 2))) if total_scans > 0 else 50
    
    recommendations = []
    if critical > 0:
        recommendations.append(f"URGENT: Address {critical} critical vulnerabilities immediately")
    if high > 0:
        recommendations.append(f"High priority: Review and fix {high} high-severity vulnerabilities")
    if security_score >= 90:
        recommendations.append("Excellent security posture! Continue regular scanning")
    elif security_score >= 70:
        recommendations.append("Good security score. Address medium-severity issues")
    else:
        recommendations.append("Security needs attention. Run comprehensive scans")
    recommendations.append("Enable automated scanning in CI/CD for continuous monitoring")
    
    return {
        "summary": {
            "total_issues": len(vulnerabilities),
            "total_scans": total_scans,
            "severity_breakdown": {
                "critical": critical,
                "high": high,
                "medium": medium,
                "low": low
            },
            "status_breakdown": {
                "open": open_vulns,
                "fixed": fixed_vulns
            },
            "security_score": security_score,
            "performance_score": performance_score,
            "recommendations": recommendations
        }
    }


@router.get("/vulnerabilities")
def get_audit_vulnerabilities(
    skip: int = 0,
    limit: int = 50,
    severity: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Vulnerability).filter(
        Vulnerability.owner_id == current_user.id
    )
    
    if severity:
        query = query.filter(Vulnerability.severity == severity)
    
    from sqlalchemy import case
    severity_order = case(
        (Vulnerability.severity == 'critical', 0),
        (Vulnerability.severity == 'high', 1),
        (Vulnerability.severity == 'medium', 2),
        (Vulnerability.severity == 'low', 3),
        else_=4
    )
    vulnerabilities = query.order_by(
        severity_order,
        Vulnerability.created_at.desc()
    ).offset(skip).limit(limit).all()
    
    return [
        {
            "id": v.id,
            "type": v.title,
            "severity": v.severity,
            "status": v.status,
            "title": v.title,
            "description": v.description,
            "file": v.file_path,
            "line": v.line_number,
            "code": v.code_snippet,
            "cwe_id": v.cwe_id,
            "cvss_score": v.cvss_score,
            "confidence": 0.85,
            "created_at": v.created_at.isoformat() if v.created_at else None
        }
        for v in vulnerabilities
    ]
