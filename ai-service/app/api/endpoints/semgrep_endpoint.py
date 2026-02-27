"""
Semgrep-powered repository scanning endpoint
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os
import uuid

from app.scanners.semgrep_scanner import (
    SemgrepScanner,
    ClaudeAnalyzer,
    create_semgrep_scanner,
    create_claude_analyzer
)

router = APIRouter(prefix="/api/semgrep", tags=["semgrep"])

# Initialize scanner
semgrep_scanner = None
claude_analyzer = None


def get_scanner() -> SemgrepScanner:
    """Get or create Semgrep scanner instance"""
    global semgrep_scanner
    if semgrep_scanner is None:
        timeout = int(os.getenv("SEMGREP_TIMEOUT", "300"))
        rules = os.getenv("SEMGREP_RULES", "").split(",") if os.getenv("SEMGREP_RULES") else None
        semgrep_scanner = create_semgrep_scanner(rules=rules, timeout=timeout)
    return semgrep_scanner


def get_claude_analyzer() -> Optional[ClaudeAnalyzer]:
    """Get or create Claude analyzer instance"""
    global claude_analyzer
    if claude_analyzer is None:
        api_key = os.getenv("CLAUDE_API_KEY")
        if api_key:
            claude_analyzer = create_claude_analyzer(api_key)
    return claude_analyzer


class RepositoryScanRequest(BaseModel):
    """Request to scan a repository"""
    repository_url: str
    branch: Optional[str] = None
    github_token: Optional[str] = None
    use_ai_analysis: bool = True
    rules: Optional[List[str]] = None


class LocalScanRequest(BaseModel):
    """Request to scan a local directory"""
    directory_path: str
    use_ai_analysis: bool = True


class ScanProgress(BaseModel):
    """Scan progress response"""
    scan_id: str
    status: str
    progress: float = 0.0
    message: str = ""


# Store for background scan results
scan_results: Dict[str, Dict[str, Any]] = {}


@router.post("/scan/repository")
async def scan_repository(request: RepositoryScanRequest, background_tasks: BackgroundTasks):
    """
    Scan a Git repository for vulnerabilities using Semgrep
    
    Features:
    - Clones repository temporarily
    - Runs Semgrep with OWASP, secrets, and language-specific rules
    - Optionally uses Claude AI to reduce false positives
    - Returns structured findings
    """
    scan_id = str(uuid.uuid4())[:16]
    
    # Validate repository URL
    if not request.repository_url:
        raise HTTPException(status_code=400, detail="repository_url is required")
        
    if not request.repository_url.startswith(("http://", "https://", "git@")):
        raise HTTPException(
            status_code=400, 
            detail="Invalid repository URL. Must start with http://, https://, or git@"
        )
    
    # Create scanner with custom rules if provided
    scanner = get_scanner()
    if request.rules:
        scanner.rules = request.rules
    
    # Initialize result storage
    scan_results[scan_id] = {
        "status": "starting",
        "progress": 0.0,
        "message": "Initializing scan..."
    }
    
    # Run scan in background
    background_tasks.add_task(
        run_repository_scan,
        scan_id,
        request.repository_url,
        request.branch,
        request.github_token,
        request.use_ai_analysis
    )
    
    return {
        "scan_id": scan_id,
        "status": "started",
        "message": "Scan started in background",
        "status_url": f"/api/semgrep/scan/{scan_id}/status"
    }


async def run_repository_scan(
    scan_id: str,
    repo_url: str,
    branch: Optional[str],
    github_token: Optional[str],
    use_ai_analysis: bool
) -> None:
    """Background task to run repository scan"""
    scanner = get_scanner()
    analyzer = get_claude_analyzer()
    
    try:
        scan_results[scan_id]["progress"] = 0.1
        scan_results[scan_id]["message"] = "Cloning repository..."
        
        # Run Semgrep scan
        result = await scanner.scan_repository(
            repo_url=repo_url,
            branch=branch,
            github_token=github_token
        )
        
        if result.get("status") == "error":
            scan_results[scan_id] = result
            return
            
        scan_results[scan_id]["progress"] = 0.7
        scan_results[scan_id]["message"] = "Analyzing findings with AI..."
        
        # Apply Claude AI analysis if enabled
        if use_ai_analysis and analyzer and result.get("findings"):
            findings = result["findings"]
            
            # Analyze top findings (limit to avoid token exhaustion)
            for i, finding in enumerate(findings[:20]):  # Max 20 AI analyses
                try:
                    # Get code snippet from file
                    code_snippet = _extract_code_snippet(
                        finding.get("file", ""),
                        finding.get("line", 0)
                    )
                    
                    if code_snippet:
                        analysis = await analyzer.analyze_finding(
                            code_snippet=code_snippet,
                            finding_type=finding.get("type", "unknown"),
                            file_path=finding.get("file", ""),
                            line_number=finding.get("line", 0)
                        )
                        
                        # Apply analysis results
                        if not analysis.get("is_true_positive", True):
                            finding["false_positive"] = True
                            finding["ai_confidence"] = analysis.get("confidence", 0.5)
                        else:
                            finding["ai_confidence"] = analysis.get("confidence", 0.5)
                            
                        finding["ai_suggested_fix"] = analysis.get("suggested_fix")
                        finding["ai_explanation"] = analysis.get("explanation")
                        
                except Exception:
                    pass
                    
                # Update progress
                scan_results[scan_id]["progress"] = 0.7 + (i * 0.02)
        
        scan_results[scan_id]["progress"] = 1.0
        scan_results[scan_id]["message"] = "Scan completed"
        scan_results[scan_id].update(result)
        
    except Exception as e:
        scan_results[scan_id] = {
            "scan_id": scan_id,
            "status": "error",
            "error": str(e),
            "findings": [],
            "total_findings": 0
        }


def _extract_code_snippet(file_path: str, line_number: int, context_lines: int = 5) -> Optional[str]:
    """Extract code snippet from a file for AI analysis"""
    if not file_path or not os.path.exists(file_path):
        return None
        
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
            
        start = max(0, line_number - context_lines - 1)
        end = min(len(lines), line_number + context_lines)
        
        return ''.join(lines[start:end])
        
    except Exception:
        return None


@router.get("/scan/{scan_id}/status")
async def get_scan_status(scan_id: str):
    """Get the status of a background scan"""
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    return scan_results[scan_id]


@router.get("/scan/{scan_id}/results")
async def get_scan_results(scan_id: str):
    """Get full scan results"""
    if scan_id not in scan_results:
        raise HTTPException(status_code=404, detail="Scan not found")
        
    result = scan_results[scan_id]
    
    # Return 202 if still running
    if result.get("status") in ("starting", "running"):
        return JSONResponse(
            status_code=202,
            content={
                "scan_id": scan_id,
                "status": result.get("status", "running"),
                "progress": result.get("progress", 0),
                "message": result.get("message", "Scan in progress...")
            }
        )
        
    return result


@router.post("/scan/local")
async def scan_local_directory(request: LocalScanRequest):
    """
    Scan a local directory for vulnerabilities
    """
    scanner = get_scanner()
    
    if not os.path.exists(request.directory_path):
        raise HTTPException(status_code=400, detail="Directory not found")
        
    result = await scanner.scan_local_directory(request.directory_path)
    
    return result


@router.get("/rules")
async def list_available_rules():
    """List available Semgrep rules"""
    return {
        "rules": SemgrepScanner.DEFAULT_RULES,
        "description": "OWASP Top 10, Secrets, SQL Injection, XSS, and language-specific rules"
    }


@router.get("/health")
async def semgrep_health():
    """Check Semgrep availability"""
    scanner = get_scanner()
    analyzer = get_claude_analyzer()
    
    return {
        "semgrep_available": scanner._is_semgrep_installed(),
        "claude_available": analyzer is not None,
        "timeout_seconds": scanner.timeout,
        "max_repo_size_mb": scanner.MAX_REPO_SIZE_MB
    }
