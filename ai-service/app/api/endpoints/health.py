from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from typing import Dict, Any, List
from datetime import datetime
import psutil
import os

from app.database import get_db

router = APIRouter(prefix="/api/v1", tags=["Health & Monitoring"])


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str = "1.0.0"
    uptime_seconds: float
    services: Dict[str, Any]
    system: Dict[str, Any]
    database: Dict[str, Any]


class ComponentStatus(BaseModel):
    status: str
    latency_ms: float = 0
    details: Dict[str, Any] = {}


def get_uptime() -> float:
    """Get application uptime in seconds"""
    try:
        with open('/proc/uptime', 'r') as f:
            uptime = float(f.readline().split()[0])
            return uptime
    except:
        return 0


@router.get("/health", response_model=HealthResponse)
async def health_check(db: Session = Depends(get_db)) -> HealthResponse:
    """
    Comprehensive health check endpoint
    """
    services = {}
    system = {}
    database = {}
    
    # Check database
    try:
        start = datetime.now()
        db.execute(text("SELECT 1"))
        latency = (datetime.now() - start).total_seconds() * 1000
        
        # Get table counts
        tables = {}
        try:
            tables['users'] = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
            tables['scans'] = db.execute(text("SELECT COUNT(*) FROM scans")).scalar() or 0
            tables['vulnerabilities'] = db.execute(text("SELECT COUNT(*) FROM vulnerabilities")).scalar() or 0
            tables['api_keys'] = db.execute(text("SELECT COUNT(*) FROM api_keys")).scalar() or 0
            tables['webhooks'] = db.execute(text("SELECT COUNT(*) FROM webhooks")).scalar() or 0
        except:
            pass
        
        database = {
            "status": "healthy",
            "latency_ms": round(latency, 2),
            "tables": tables
        }
    except Exception as e:
        database = {
            "status": "unhealthy",
            "error": str(e)
        }
    
    # System metrics
    try:
        system = {
            "cpu_percent": psutil.cpu_percent(interval=0.1),
            "memory_percent": psutil.virtual_memory().percent,
            "memory_used_mb": psutil.virtual_memory().used / (1024 * 1024),
            "memory_total_mb": psutil.virtual_memory().total / (1024 * 1024),
            "disk_percent": psutil.disk_usage('/').percent,
            "process_count": len(psutil.pids())
        }
    except:
        system = {"status": "unavailable"}
    
    # Services status
    services = {
        "api": {
            "status": "healthy",
            "latency_ms": 0
        }
    }
    
    # Determine overall status
    overall_status = "healthy"
    if database.get("status") == "unhealthy":
        overall_status = "degraded"
    
    return HealthResponse(
        status=overall_status,
        timestamp=datetime.now().isoformat(),
        uptime_seconds=get_uptime(),
        services=services,
        system=system,
        database=database
    )


@router.get("/health/ready")
async def readiness_check(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Readiness probe for Kubernetes
    """
    checks = {}
    
    # Check database
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "ready"
    except:
        checks["database"] = "not_ready"
    
    is_ready = all(v == "ready" for v in checks.values())
    
    return {
        "ready": is_ready,
        "checks": checks
    }


@router.get("/health/live")
async def liveness_check() -> Dict[str, str]:
    """
    Liveness probe for Kubernetes
    """
    return {"status": "alive"}


@router.get("/metrics")
async def metrics(db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Prometheus-compatible metrics endpoint
    """
    metrics = {
        "app_info": {
            "version": "1.0.0",
            "timestamp": datetime.now().isoformat()
        }
    }
    
    # Database metrics
    try:
        metrics["db_scans_total"] = db.execute(text("SELECT COUNT(*) FROM scans")).scalar() or 0
        metrics["db_users_total"] = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        metrics["db_vulns_total"] = db.execute(text("SELECT COUNT(*) FROM vulnerabilities")).scalar() or 0
    except:
        pass
    
    # System metrics
    try:
        metrics["system_cpu_percent"] = psutil.cpu_percent(interval=0.1)
        metrics["system_memory_percent"] = psutil.virtual_memory().percent
    except:
        pass
    
    return metrics
