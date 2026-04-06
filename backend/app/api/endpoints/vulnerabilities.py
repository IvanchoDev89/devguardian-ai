from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Vulnerability
from app.models.schemas import (
    VulnerabilityCreate,
    VulnerabilityUpdate,
    VulnerabilityResponse
)

router = APIRouter(prefix="/api/vulnerabilities", tags=["Vulnerabilities"])


@router.get("", response_model=List[VulnerabilityResponse])
def list_vulnerabilities(
    skip: int = 0,
    limit: int = 100,
    severity: str = None,
    status: str = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    query = db.query(Vulnerability).filter(Vulnerability.owner_id == current_user.id)
    
    if severity:
        query = query.filter(Vulnerability.severity == severity)
    if status:
        query = query.filter(Vulnerability.status == status)
    
    return query.order_by(Vulnerability.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=VulnerabilityResponse)
def create_vulnerability(
    vulnerability: VulnerabilityCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_vuln = Vulnerability(
        **vulnerability.model_dump(),
        owner_id=current_user.id
    )
    db.add(db_vuln)
    db.commit()
    db.refresh(db_vuln)
    return db_vuln


@router.get("/{vuln_id}", response_model=VulnerabilityResponse)
def get_vulnerability(
    vuln_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vuln = db.query(Vulnerability).filter(
        Vulnerability.id == vuln_id,
        Vulnerability.owner_id == current_user.id
    ).first()
    
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    return vuln


@router.put("/{vuln_id}", response_model=VulnerabilityResponse)
def update_vulnerability(
    vuln_id: int,
    data: VulnerabilityUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vuln = db.query(Vulnerability).filter(
        Vulnerability.id == vuln_id,
        Vulnerability.owner_id == current_user.id
    ).first()
    
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vuln, key, value)
    
    db.commit()
    db.refresh(vuln)
    return vuln


@router.delete("/{vuln_id}")
def delete_vulnerability(
    vuln_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    vuln = db.query(Vulnerability).filter(
        Vulnerability.id == vuln_id,
        Vulnerability.owner_id == current_user.id
    ).first()
    
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    
    db.delete(vuln)
    db.commit()
    
    return {"message": "Vulnerability deleted"}


@router.get("/stats/summary")
def get_vulnerability_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    total = db.query(Vulnerability).filter(Vulnerability.owner_id == current_user.id).count()
    critical = db.query(Vulnerability).filter(
        Vulnerability.owner_id == current_user.id,
        Vulnerability.severity == "critical"
    ).count()
    high = db.query(Vulnerability).filter(
        Vulnerability.owner_id == current_user.id,
        Vulnerability.severity == "high"
    ).count()
    medium = db.query(Vulnerability).filter(
        Vulnerability.owner_id == current_user.id,
        Vulnerability.severity == "medium"
    ).count()
    low = db.query(Vulnerability).filter(
        Vulnerability.owner_id == current_user.id,
        Vulnerability.severity == "low"
    ).count()
    resolved = db.query(Vulnerability).filter(
        Vulnerability.owner_id == current_user.id,
        Vulnerability.status == "resolved"
    ).count()
    
    return {
        "total": total,
        "by_severity": {
            "critical": critical,
            "high": high,
            "medium": medium,
            "low": low
        },
        "resolved": resolved,
        "open": total - resolved
    }
