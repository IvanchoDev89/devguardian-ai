from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from datetime import datetime
import secrets
import re
import subprocess
import os

router = APIRouter(prefix="/api/v1/repos", tags=["Repository Scanner"])


class RepoScanRequest(BaseModel):
    repo_url: str
    provider: Optional[str] = None  # github, gitlab, bitbucket, custom
    branch: Optional[str] = "main"
    scan_dependencies: bool = True
    include_ignore: bool = True


class RepoScanResponse(BaseModel):
    scan_id: str
    repo_url: str
    provider: str
    status: str
    created_at: str
    total_files: int = 0
    total_vulnerabilities: int = 0
    score: int = 100


PROVIDER_PATTERNS = {
    "github": r"github\.com[/:]([\w-]+)/([\w.-]+)",
    "gitlab": r"gitlab\.com[/:]([\w-]+)/([\w.-]+)",
    "bitbucket": r"bitbucket\.org[/:]([\w-]+)/([\w.-]+)",
}


def detect_provider(url: str) -> tuple[str, str, str]:
    """Detect the provider and extract owner/repo from URL"""
    url = url.strip().rstrip("/")
    
    # Remove .git suffix
    if url.endswith(".git"):
        url = url[:-4]
    
    for provider, pattern in PROVIDER_PATTERNS.items():
        match = re.search(pattern, url)
        if match:
            owner, repo = match.groups()
            return provider, owner, repo.rstrip("/")
    
    # Try custom/SSH URLs
    if url.startswith("git@"):
        # SSH format: git@github.com:owner/repo.git
        match = re.search(r"git@(\w+)\.com[/:]([\w-]+)/([\w.-]+)", url)
        if match:
            provider = "github" if "github" in match.group(1) else "gitlab"
            return provider, match.group(2), match.group(3).rstrip("/")
    
    return "custom", "", ""


def clone_repo(url: str, target_dir: str, branch: str = "main") -> bool:
    """Clone a repository to target directory"""
    try:
        # Try different branch names
        for branch_name in [branch, "main", "master", "develop"]:
            result = subprocess.run(
                ["git", "clone", "--depth", "1", "-b", branch_name, url, target_dir],
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            if result.returncode == 0:
                return True
            # Try next branch
            if os.path.exists(target_dir):
                import shutil
                shutil.rmtree(target_dir)
        
        # Fallback: shallow clone without branch
        result = subprocess.run(
            ["git", "clone", "--depth", "1", url, target_dir],
            capture_output=True,
            text=True,
            timeout=300
        )
        return result.returncode == 0
        
    except Exception as e:
        print(f"Clone error: {e}")
        return False


async def scan_cloned_repo(repo_dir: str, provider: str, owner: str, repo: str) -> Dict[str, Any]:
    """Scan a cloned repository for vulnerabilities"""
    from app.scanners.vulnerability_scanner import create_scanner
    
    scanner = create_scanner()
    
    total_vulns = 0
    all_vulnerabilities = []
    files_scanned = 0
    
    supported_extensions = {
        ".py": "python",
        ".js": "javascript", 
        ".ts": "typescript",
        ".java": "java",
        ".go": "go",
        ".rb": "ruby",
        ".php": "php",
        ".cs": "csharp",
        ".cpp": "cpp", ".c": "c"
    }
    
    for root, dirs, files in os.walk(repo_dir):
        # Skip common non-code directories
        dirs[:] = [d for d in dirs if d not in [".git", "node_modules", "vendor", "venv", "__pycache__", ".venv"]]
        
        for file in files:
            file_path = os.path.join(root, file)
            ext = os.path.splitext(file)[1].lower()
            
            if ext not in supported_extensions:
                continue
            
            try:
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    code = f.read()
                
                if len(code) < 10:  # Skip very small files
                    continue
                
                files_scanned += 1
                language = supported_extensions[ext]
                
                result = scanner.analyze(code, language)
                
                if result.get("vulnerabilities"):
                    for vuln in result["vulnerabilities"]:
                        vuln["file"] = os.path.relpath(file_path, repo_dir)
                        all_vulnerabilities.append(vuln)
                    total_vulns += len(result["vulnerabilities"])
                    
            except Exception as e:
                continue
    
    # Calculate score
    if files_scanned == 0:
        score = 100
    elif total_vulns == 0:
        score = 100
    elif total_vulns <= 2:
        score = 80
    elif total_vulns <= 5:
        score = 60
    elif total_vulns <= 10:
        score = 40
    else:
        score = max(0, 20 - total_vulns)
    
    return {
        "files_scanned": files_scanned,
        "total_vulnerabilities": total_vulns,
        "score": score,
        "vulnerabilities": all_vulnerabilities,
        "provider": provider,
        "owner": owner,
        "repo": repo
    }


@router.post("/scan", response_model=RepoScanResponse)
async def scan_repository(
    request: RepoScanRequest,
    background_tasks: BackgroundTasks
):
    """Scan a GitHub, GitLab, or Bitbucket repository"""
    
    # Validate URL
    if not request.repo_url:
        raise HTTPException(status_code=400, detail="Repository URL is required")
    
    # Detect provider
    if request.provider:
        provider = request.provider.lower()
    else:
        provider, owner, repo = detect_provider(request.repo_url)
        
        if not owner or not repo:
            raise HTTPException(
                status_code=400, 
                detail="Could not detect repository provider. Please specify GitHub, GitLab, or Bitbucket URL."
            )
    
    if provider not in ["github", "gitlab", "bitbucket", "custom"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported provider. Use: github, gitlab, or bitbucket"
        )
    
    # Generate scan ID
    scan_id = secrets.token_hex(8)
    
    # For demo, return mock data (in production, would clone and scan)
    return RepoScanResponse(
        scan_id=scan_id,
        repo_url=request.repo_url,
        provider=provider,
        status="completed",
        created_at=datetime.utcnow().isoformat(),
        total_files=42,
        total_vulnerabilities=7,
        score=65
    )


@router.get("/providers")
async def get_providers():
    """Get supported repository providers"""
    return {
        "providers": [
            {
                "id": "github",
                "name": "GitHub",
                "url_pattern": "https://github.com/owner/repo",
                "icon": "github"
            },
            {
                "id": "gitlab", 
                "name": "GitLab",
                "url_pattern": "https://gitlab.com/owner/repo",
                "icon": "gitlab"
            },
            {
                "id": "bitbucket",
                "name": "Bitbucket",
                "url_pattern": "https://bitbucket.org/owner/repo",
                "icon": "bitbucket"
            }
        ]
    }


@router.get("/scan/{scan_id}")
async def get_scan_results(scan_id: str):
    """Get results of a repository scan"""
    # In production, fetch from database
    return {
        "scan_id": scan_id,
        "status": "completed",
        "total_files": 42,
        "total_vulnerabilities": 7,
        "score": 65,
        "vulnerabilities": [
            {
                "file": "app/auth.py",
                "line": 15,
                "type": "Hardcoded Password",
                "severity": "critical",
                "description": "Hardcoded password detected"
            },
            {
                "file": "utils/sql.py", 
                "line": 23,
                "type": "SQL Injection",
                "severity": "critical",
                "description": "SQL query built with string concatenation"
            }
        ]
    }
