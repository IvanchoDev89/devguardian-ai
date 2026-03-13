"""
Vulnerabilities API Endpoints
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/v1", tags=["Vulnerabilities"])


class VulnerabilityResponse(BaseModel):
    id: str
    title: str
    description: str
    severity: str
    status: str
    repository: str
    file: str
    cwe_id: Optional[str] = None
    cvss_score: Optional[float] = None
    detected_at: str


# In-memory storage for demo
vulnerabilities_db = []


@router.get("/vulnerabilities", response_model=List[VulnerabilityResponse])
async def get_vulnerabilities():
    """Get all vulnerabilities"""
    if not vulnerabilities_db:
        # Add demo data
        for i, vuln in enumerate([
            {"title": "SQL Injection", "severity": "critical", "cwe": "CWE-89"},
            {"title": "XSS Reflected", "severity": "high", "cwe": "CWE-79"},
            {"title": "Command Injection", "severity": "critical", "cwe": "CWE-78"},
            {"title": "Path Traversal", "severity": "high", "cwe": "CWE-22"},
            {"title": "Insecure Deserialization", "severity": "critical", "cwe": "CWE-502"},
            {"title": "Broken Authentication", "severity": "high", "cwe": "CWE-287"},
            {"title": "Sensitive Data Exposure", "severity": "medium", "cwe": "CWE-200"},
            {"title": "Security Misconfiguration", "severity": "medium", "cwe": "CWE-16"},
        ]):
            vulnerabilities_db.append({
                "id": str(uuid.uuid4())[:8],
                "title": vuln["title"],
                "description": f"Found {vuln['title']} vulnerability in source code",
                "severity": vuln["severity"],
                "status": "open",
                "repository": "demo-repo",
                "file": f"src/{vuln['title'].lower().replace(' ', '_')}.py",
                "cwe_id": vuln["cwe"],
                "cvss_score": 9.0 if vuln["severity"] == "critical" else 7.0 if vuln["severity"] == "high" else 5.0,
                "detected_at": datetime.utcnow().isoformat()
            })
    
    return vulnerabilities_db


@router.get("/vulnerabilities/{vuln_id}")
async def get_vulnerability(vuln_id: str):
    """Get a specific vulnerability"""
    vuln = next((v for v in vulnerabilities_db if v["id"] == vuln_id), None)
    if not vuln:
        raise HTTPException(status_code=404, detail="Vulnerability not found")
    return vuln


@router.put("/vulnerabilities/{vuln_id}")
async def update_vulnerability(vuln_id: str, data: dict):
    """Update a vulnerability"""
    for vuln in vulnerabilities_db:
        if vuln["id"] == vuln_id:
            vuln.update(data)
            return vuln
    raise HTTPException(status_code=404, detail="Vulnerability not found")
