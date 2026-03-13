"""
Security Posture API Endpoints
Historical security metrics and trend tracking
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
import logging
from datetime import datetime
import uuid

from app.scanners.security_posture import SecurityPostureTracker

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/posture", tags=["Security Posture"])

tracker = SecurityPostureTracker()


class RecordScanRequest(BaseModel):
    score: int = Field(..., ge=0, le=100)
    vulnerabilities: Dict[str, int]
    repo_url: Optional[str] = None


class TrendResponse(BaseModel):
    trend: str
    period_days: int
    total_scans: int
    average_score: float
    latest_score: int
    score_change: int
    historical_scores: List[int]


@router.post("/record", response_model=Dict)
async def record_security_scan(request: RecordScanRequest):
    """Record a security scan result"""
    scan_id = str(uuid.uuid4())[:12]
    
    logger.info(f"Recording security scan {scan_id}")
    
    try:
        tracker.record_scan(request.score, request.vulnerabilities)
        
        return {
            "scan_id": scan_id,
            "recorded": True,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to record scan: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/trend", response_model=TrendResponse)
async def get_security_trend(days: int = 30):
    """Get security trend over specified period"""
    try:
        trend = tracker.get_trend(days)
        
        if trend.get("trend") == "insufficient_data":
            return TrendResponse(
                trend="insufficient_data",
                period_days=days,
                total_scans=0,
                average_score=0,
                latest_score=0,
                score_change=0,
                historical_scores=[]
            )
        
        return TrendResponse(**trend)
    except Exception as e:
        logger.error(f"Failed to get trend: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/statistics")
async def get_statistics(days: int = 30):
    """Get detailed security statistics"""
    try:
        stats = tracker.get_statistics(days)
        return stats
    except Exception as e:
        logger.error(f"Failed to get statistics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/history")
async def get_history(days: int = 90):
    """Get full security history"""
    try:
        history = tracker.get_history(days)
        return history
    except Exception as e:
        logger.error(f"Failed to get history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/recommendations")
async def get_recommendations():
    """Get security recommendations based on posture"""
    try:
        trend = tracker.get_trend(30)
        stats = tracker.get_statistics(30)
        
        recommendations = []
        
        if trend.get("trend") == "declining":
            recommendations.append({
                "priority": "high",
                "message": "Security posture is declining. Review recent vulnerability fixes."
            })
        elif trend.get("trend") == "improving":
            recommendations.append({
                "priority": "info",
                "message": "Security posture is improving. Keep up the good work!"
            })
        
        if stats.get("score", {}).get("average", 100) < 70:
            recommendations.append({
                "priority": "high",
                "message": "Average score below 70. Consider immediate security review."
            })
        
        return {
            "recommendations": recommendations,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Failed to get recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))
