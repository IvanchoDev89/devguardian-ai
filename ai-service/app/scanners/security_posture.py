"""
Historical Security Posture Tracking
Track security metrics over time
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
from collections import defaultdict
import statistics


@dataclass
class SecurityMetric:
    date: str
    score: int
    vulnerabilities: Dict[str, int]
    scans: int


class SecurityPostureTracker:
    """Track security metrics over time"""
    
    def __init__(self):
        self.metrics: List[SecurityMetric] = []
        
    def record_scan(self, score: int, vulnerabilities: Dict[str, int]):
        """Record a security scan"""
        metric = SecurityMetric(
            date=datetime.utcnow().strftime("%Y-%m-%d"),
            score=score,
            vulnerabilities=vulnerabilities,
            scans=1
        )
        self.metrics.append(metric)
        
    def get_trend(self, days: int = 30) -> Dict:
        """Get security trend over time"""
        cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        
        recent = [m for m in self.metrics if m.date >= cutoff]
        
        if not recent:
            return {
                "trend": "insufficient_data",
                "message": "Not enough scan data to determine trend"
            }
            
        scores = [m.score for m in recent]
        avg_score = sum(scores) / len(scores)
        
        # Calculate trend
        if len(scores) >= 7:
            first_half = scores[:len(scores)//2]
            second_half = scores[len(scores)//2:]
            
            first_avg = sum(first_half) / len(first_half)
            second_avg = sum(second_half) / len(second_half)
            
            if second_avg > first_avg + 5:
                trend = "improving"
            elif second_avg < first_avg - 5:
                trend = "declining"
            else:
                trend = "stable"
        else:
            trend = "stable"
            
        return {
            "trend": trend,
            "period_days": days,
            "total_scans": len(recent),
            "average_score": round(avg_score, 2),
            "latest_score": scores[-1],
            "score_change": scores[-1] - scores[0] if len(scores) > 1 else 0,
            "historical_scores": scores
        }
    
    def get_statistics(self, days: int = 30) -> Dict:
        """Get detailed statistics"""
        cutoff = (datetime.utcnow() - timedelta(days=days)).strftime("%Y-%m-%d")
        recent = [m for m in self.metrics if m.date >= cutoff]
        
        if not recent:
            return {"message": "No data available"}
            
        scores = [m.score for m in recent]
        total_vulns = sum(sum(m.vulnerabilities.values()) for m in recent)
        
        vuln_breakdown = defaultdict(int)
        for m in recent:
            for k, v in m.vulnerabilities.items():
                vuln_breakdown[k] += v
        
        return {
            "period_days": days,
            "total_scans": len(recent),
            "score": {
                "average": round(statistics.mean(scores), 2),
                "median": statistics.median(scores),
                "min": min(scores),
                "max": max(scores),
                "stdev": round(statistics.stdev(scores), 2) if len(scores) > 1 else 0
            },
            "vulnerabilities": {
                "total": total_vulns,
                "by_severity": dict(vuln_breakdown),
                "per_scan": round(total_vulns / len(recent), 2)
            },
            "mttr_estimate": self._estimate_mttr(recent)
        }
    
    def _estimate_mttr(self, metrics: List[SecurityMetric]) -> Optional[float]:
        """Estimate Mean Time To Remediate (simplified)"""
        # Simplified - would need proper tracking
        return None
    
    def get_benchmark(self) -> Dict:
        """Compare against industry benchmarks"""
        if not self.metrics:
            return {"message": "No data available"}
            
        recent_scores = [m.score for m in self.metrics[-30:]]
        avg = sum(recent_scores) / len(recent_scores)
        
        # Industry benchmarks (simplified)
        benchmarks = {
            "excellent": 90,
            "good": 75,
            "average": 60,
            "poor": 40
        }
        
        rating = "poor"
        if avg >= benchmarks["excellent"]:
            rating = "excellent"
        elif avg >= benchmarks["good"]:
            rating = "good"
        elif avg >= benchmarks["average"]:
            rating = "average"
            
        return {
            "your_score": round(avg, 2),
            "rating": rating,
            "benchmarks": benchmarks,
            "percentile_estimate": self._estimate_percentile(avg)
        }
    
    def _estimate_percentile(self, score: float) -> str:
        """Estimate percentile based on score"""
        if score >= 90:
            return "Top 10%"
        elif score >= 80:
            return "Top 25%"
        elif score >= 70:
            return "Top 50%"
        elif score >= 60:
            return "Below Average"
        else:
            return "Needs Improvement"
    
    def generate_report(self) -> Dict:
        """Generate comprehensive report"""
        return {
            "summary": self.get_trend(),
            "statistics": self.get_statistics(),
            "benchmark": self.get_benchmark(),
            "generated_at": datetime.utcnow().isoformat()
        }


def create_tracker() -> SecurityPostureTracker:
    return SecurityPostureTracker()
