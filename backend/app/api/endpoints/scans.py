from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List, Optional

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import Scan
from app.models.schemas import ScanCreate, ScanUpdate, ScanResponse

router = APIRouter(prefix="/api/scans", tags=["Scans"])


@router.get("", response_model=List[ScanResponse])
def list_scans(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    scan_type: Optional[str] = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_id = current_user.id
    query = db.query(Scan).filter(Scan.owner_id == user_id)
    
    if status:
        query = query.filter(Scan.status == status)
    if scan_type:
        query = query.filter(Scan.scan_type == scan_type)
    
    return query.order_by(Scan.created_at.desc()).offset(skip).limit(limit).all()


@router.post("", response_model=ScanResponse)
def create_scan(
    scan_data: ScanCreate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    scan = Scan(
        name=scan_data.name,
        scan_type=scan_data.scan_type,
        target=scan_data.target,
        owner_id=current_user.id
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    return scan


@router.get("/stats/summary")
def get_scan_stats(
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    user_scans = db.query(Scan).filter(Scan.owner_id == current_user.id).all()
    
    total = len(user_scans)
    completed = len([s for s in user_scans if s.status == "completed"])
    running = len([s for s in user_scans if s.status == "running"])
    failed = len([s for s in user_scans if s.status == "failed"])
    
    return {
        "total": total,
        "completed": completed,
        "running": running,
        "failed": failed
    }


@router.get("/{scan_id}", response_model=ScanResponse)
def get_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.owner_id == current_user["sub"]
    ).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    return scan


@router.put("/{scan_id}", response_model=ScanResponse)
def update_scan(
    scan_id: int,
    scan_data: ScanUpdate,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.owner_id == current_user["sub"]
    ).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    for key, value in scan_data.model_dump(exclude_unset=True).items():
        setattr(scan, key, value)
    
    db.commit()
    db.refresh(scan)
    return scan


@router.delete("/{scan_id}")
def delete_scan(
    scan_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    scan = db.query(Scan).filter(
        Scan.id == scan_id,
        Scan.owner_id == current_user["sub"]
    ).first()
    
    if not scan:
        raise HTTPException(status_code=404, detail="Scan not found")
    
    db.delete(scan)
    db.commit()
    return {"message": "Scan deleted successfully"}
