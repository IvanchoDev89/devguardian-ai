"""
Semgrep Scanner - Professional vulnerability detection engine
Integrates Semgrep for accurate, production-grade vulnerability scanning
"""

import os
import json
import subprocess
import tempfile
import shutil
import asyncio
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime
import hashlib


class SemgrepFinding:
    """Represents a single vulnerability finding from Semgrep"""
    
    def __init__(
        self,
        check_id: str,
        path: str,
        start_line: int,
        end_line: int,
        start_col: int,
        end_col: int,
        severity: str,
        message: str,
        metadata: Dict[str, Any],
        extra: Dict[str, Any]
    ):
        self.check_id = check_id
        self.path = path
        self.start_line = start_line
        self.end_line = end_line
        self.start_col = start_col
        self.end_col = end_col
        self.severity = severity
        self.message = message
        self.metadata = metadata
        self.extra = extra
        
        # Map Semgrep severity to our format
        self.severity_map = {
            "ERROR": "critical",
            "WARNING": "high", 
            "INFO": "low"
        }
        
    @property
    def normalized_severity(self) -> str:
        return self.severity_map.get(self.severity.upper(), "medium")
    
    @property
    def cwe_id(self) -> Optional[str]:
        return self.metadata.get("cwe")
    
    @property
    def owasp_category(self) -> Optional[str]:
        return self.metadata.get("owasp")
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.check_id,
            "file": self.path,
            "line": self.start_line,
            "end_line": self.end_line,
            "column": self.start_col,
            "severity": self.normalized_severity,
            "message": self.message,
            "cwe": self.cwe_id,
            "owasp": self.owasp_category,
            "metadata": self.metadata,
            "extra": self.extra
        }


class SemgrepScanner:
    """
    Semgrep-powered vulnerability scanner
    
    Features:
    - Clones repositories temporarily for scanning
    - Uses OWASP, secrets, and language-specific rules
    - Returns structured findings compatible with existing models
    - Supports timeout handling for large repositories
    - Auto-cleanup of temporary files
    """
    
    # Default Semgrep rules to use
    DEFAULT_RULES = [
        "p/owasp-top-ten",
        "p/secrets", 
        "p/sql-injection",
        "p/xss",
        "p/python",
        "p/javascript",
        "p/typescript",
        "p/php",
        "p/go",
        "p/java",
        "p/c"
    ]
    
    # File size limits
    MAX_REPO_SIZE_MB = 100
    MAX_FILE_SIZE_MB = 10
    
    # Timeout settings
    SCAN_TIMEOUT_SECONDS = 300  # 5 minutes
    
    def __init__(
        self,
        rules: Optional[List[str]] = None,
        timeout: int = 300,
        max_file_size_mb: int = 10
    ):
        self.rules = rules or self.DEFAULT_RULES
        self.timeout = timeout
        self.max_file_size_mb = max_file_size_mb
        self._temp_dirs: List[str] = []
        
    def _is_semgrep_installed(self) -> bool:
        """Check if semgrep is installed"""
        try:
            result = subprocess.run(
                ["semgrep", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except (subprocess.TimeoutExpired, FileNotFoundError):
            return False
            
    def _install_semgrep(self) -> bool:
        """Install semgrep via pip"""
        try:
            subprocess.run(
                ["pip", "install", "semgrep"],
                capture_output=True,
                timeout=120,
                check=True
            )
            return self._is_semgrep_installed()
        except Exception:
            return False
            
    def _check_repo_size(self, repo_path: str) -> bool:
        """Check if repository is within size limits"""
        try:
            result = subprocess.run(
                ["du", "-sm", repo_path],
                capture_output=True,
                text=True,
                timeout=30
            )
            size_mb = int(result.stdout.split()[0])
            return size_mb <= self.MAX_REPO_SIZE_MB
        except Exception:
            return False
            
    def _filter_large_files(self, repo_path: str) -> None:
        """Remove or skip files that are too large"""
        max_size_bytes = self.max_file_size_mb * 1024 * 1024
        
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                file_path = os.path.join(root, file)
                try:
                    if os.path.getsize(file_path) > max_size_bytes:
                        os.remove(file_path)
                except OSError:
                    pass
                    
    def _clone_repository(self, repo_url: str, branch: Optional[str] = None) -> str:
        """Clone a repository to a temporary directory"""
        temp_dir = tempfile.mkdtemp(prefix="semgrep_scan_")
        self._temp_dirs.append(temp_dir)
        
        cmd = ["git", "clone", "--depth", "1"]
        if branch:
            cmd.extend(["--branch", branch])
        cmd.extend([repo_url, temp_dir])
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=120
            )
            
            if result.returncode != 0:
                # Try without --depth for large repos
                if "shallow" in result.stderr.lower():
                    cmd = ["git", "clone"]
                    if branch:
                        cmd.extend(["--branch", branch])
                    cmd.extend([repo_url, temp_dir])
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=300
                    )
                    
            if result.returncode != 0:
                raise RuntimeError(f"Git clone failed: {result.stderr}")
                
            return temp_dir
            
        except subprocess.TimeoutExpired:
            self._cleanup()
            raise TimeoutError(f"Repository clone timed out for {repo_url}")
            
    def _run_semgrep(self, repo_path: str) -> List[SemgrepFinding]:
        """Run semgrep scan on repository"""
        if not self._is_semgrep_installed():
            if not self._install_semgrep():
                raise RuntimeError("Failed to install semgrep")
                
        # Build semgrep command
        cmd = [
            "semgrep",
            "--config", ",".join(self.rules),
            "--json",
            "--no-git-ignore",
            "--max-memory", "4096",
            "--timeout", str(self.timeout),
            "--quiet",
            repo_path
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=self.timeout + 30
            )
            
            # Parse JSON output
            if result.stdout:
                return self._parse_semgrep_output(result.stdout)
            return []
            
        except subprocess.TimeoutExpired:
            raise TimeoutError(f"Semgrep scan timed out after {self.timeout}s")
        except json.JSONDecodeError:
            return []
            
    def _parse_semgrep_output(self, output: str) -> List[SemgrepFinding]:
        """Parse Semgrep JSON output into findings"""
        findings = []
        
        try:
            data = json.loads(output)
            results = data.get("results", [])
            
            for result in results:
                check_id = result.get("check_id", "unknown")
                path = result.get("path", "")
                start = result.get("start", {})
                end = result.get("end", {})
                extra = result.get("extra", {})
                metadata = extra.get("metadata", {})
                
                finding = SemgrepFinding(
                    check_id=check_id,
                    path=path,
                    start_line=start.get("line", 0),
                    end_line=end.get("line", 0),
                    start_col=start.get("col", 0),
                    end_col=end.get("col", 0),
                    severity=extra.get("severity", "INFO"),
                    message=extra.get("message", ""),
                    metadata=metadata,
                    extra=extra
                )
                findings.append(finding)
                
        except json.JSONDecodeError:
            pass
            
        return findings
        
    def _group_by_severity(self, findings: List[SemgrepFinding]) -> Dict[str, int]:
        """Group findings by severity"""
        groups = {"critical": 0, "high": 0, "medium": 0, "low": 0, "info": 0}
        for f in findings:
            sev = f.normalized_severity
            if sev in groups:
                groups[sev] += 1
        return groups
        
    def _cleanup(self) -> None:
        """Clean up temporary directories"""
        for temp_dir in self._temp_dirs:
            try:
                if os.path.exists(temp_dir):
                    shutil.rmtree(temp_dir)
            except Exception:
                pass
        self._temp_dirs.clear()
        
    async def scan_repository(
        self,
        repo_url: str,
        branch: Optional[str] = None,
        github_token: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Scan a repository for vulnerabilities
        
        Args:
            repo_url: Git repository URL (HTTPS)
            branch: Optional branch to scan
            github_token: Optional token for private repos
            
        Returns:
            Dict with scan results and findings
        """
        scan_id = hashlib.sha256(
            f"{repo_url}{branch}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        started_at = datetime.now()
        
        try:
            # Clone repository
            if github_token:
                # Insert token for private repos
                repo_url = repo_url.replace(
                    "https://",
                    f"https://{github_token}@"
                )
                
            repo_path = self._clone_repository(repo_url, branch)
            
            # Check size limits
            if not self._check_repo_size(repo_path):
                raise ValueError(
                    f"Repository exceeds {self.MAX_REPO_SIZE_MB}MB limit"
                )
                
            # Filter large files
            self._filter_large_files(repo_path)
            
            # Run semgrep
            findings = await asyncio.to_thread(self._run_semgrep, repo_path)
            
            # Group by severity
            by_severity = self._group_by_severity(findings)
            
            # Calculate risk score
            risk_score = (
                by_severity["critical"] * 10 +
                by_severity["high"] * 7 +
                by_severity["medium"] * 4 +
                by_severity["low"] * 1
            ) / 10
            risk_score = min(risk_score, 10)
            
            return {
                "scan_id": scan_id,
                "repository": repo_url,
                "branch": branch or "main",
                "timestamp": started_at.isoformat(),
                "scan_duration_seconds": (datetime.now() - started_at).total_seconds(),
                "findings": [f.to_dict() for f in findings],
                "total_findings": len(findings),
                "by_severity": by_severity,
                "risk_score": round(risk_score, 2),
                "rules_used": self.rules,
                "status": "completed"
            }
            
        except TimeoutError as e:
            return {
                "scan_id": scan_id,
                "repository": repo_url,
                "status": "timeout",
                "error": str(e),
                "findings": [],
                "total_findings": 0
            }
            
        except Exception as e:
            return {
                "scan_id": scan_id,
                "repository": repo_url,
                "status": "error",
                "error": str(e),
                "findings": [],
                "total_findings": 0
            }
            
        finally:
            self._cleanup()
            
    async def scan_local_directory(self, directory_path: str) -> Dict[str, Any]:
        """Scan a local directory (for uploaded repos)"""
        scan_id = hashlib.sha256(
            f"{directory_path}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        started_at = datetime.now()
        
        try:
            if not os.path.isdir(directory_path):
                raise ValueError(f"Directory not found: {directory_path}")
                
            # Filter large files
            self._filter_large_files(directory_path)
            
            # Run semgrep
            findings = await asyncio.to_thread(self._run_semgrep, directory_path)
            
            # Group by severity
            by_severity = self._group_by_severity(findings)
            
            # Calculate risk score
            risk_score = (
                by_severity["critical"] * 10 +
                by_severity["high"] * 7 +
                by_severity["medium"] * 4 +
                by_severity["low"] * 1
            ) / 10
            risk_score = min(risk_score, 10)
            
            return {
                "scan_id": scan_id,
                "directory": directory_path,
                "timestamp": started_at.isoformat(),
                "scan_duration_seconds": (datetime.now() - started_at).total_seconds(),
                "findings": [f.to_dict() for f in findings],
                "total_findings": len(findings),
                "by_severity": by_severity,
                "risk_score": round(risk_score, 2),
                "rules_used": self.rules,
                "status": "completed"
            }
            
        except Exception as e:
            return {
                "scan_id": scan_id,
                "directory": directory_path,
                "status": "error",
                "error": str(e),
                "findings": [],
                "total_findings": 0
            }
        finally:
            self._cleanup()


class ClaudeAnalyzer:
    """
    Claude API integration for false positive reduction
    and AI-powered fix suggestions
    """
    
    def __init__(self, api_key: str, cache_dir: str = "/tmp/claude_cache"):
        self.api_key = api_key
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        
    def _get_cache_key(self, code_snippet: str, finding_type: str) -> str:
        """Generate cache key for a finding"""
        content = f"{code_snippet}:{finding_type}"
        return hashlib.sha256(content.encode()).hexdigest()[:16]
        
    def _get_cached_result(self, cache_key: str) -> Optional[Dict]:
        """Get cached analysis result"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        if os.path.exists(cache_file):
            try:
                with open(cache_file) as f:
                    return json.load(f)
            except Exception:
                return None
        return None
        
    def _save_cached_result(self, cache_key: str, result: Dict) -> None:
        """Cache analysis result"""
        cache_file = os.path.join(self.cache_dir, f"{cache_key}.json")
        try:
            with open(cache_file, 'w') as f:
                json.dump(result, f)
        except Exception:
            pass
            
    async def analyze_finding(
        self,
        code_snippet: str,
        finding_type: str,
        file_path: str,
        line_number: int
    ) -> Dict[str, Any]:
        """
        Analyze a finding with Claude to determine if it's a true positive
        and generate a fix suggestion
        """
        cache_key = self._get_cache_key(code_snippet, finding_type)
        
        # Check cache first
        cached = self._get_cached_result(cache_key)
        if cached:
            cached["from_cache"] = True
            return cached
            
        # Prepare prompt for Claude
        prompt = f"""Analyze this code finding for a vulnerability:

File: {file_path}
Line: {line_number}
Finding Type: {finding_type}

Code snippet:
```{code_snippet}```

Respond with JSON only (no markdown):
{{
  "is_true_positive": true/false,
  "confidence": 0.0-1.0,
  "explanation": "brief explanation",
  "suggested_fix": "code fix if applicable",
  "severity_adjustment": "same/higher/lower"
}}"""

        try:
            # Call Claude API via OpenAI-compatible endpoint
            import httpx
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    "https://api.anthropic.com/v1/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json"
                    },
                    json={
                        "model": "claude-sonnet-4-20250514",
                        "max_tokens": 1000,
                        "messages": [
                            {"role": "user", "content": prompt}
                        ]
                    },
                    timeout=30.0
                )
                
                if response.status_code == 200:
                    result = response.json()
                    content = result["content"][0]["text"]
                    
                    # Parse JSON from response
                    try:
                        analysis = json.loads(content)
                    except json.JSONDecodeError:
                        # Try to extract JSON from text
                        import re
                        match = re.search(r'\{.*\}', content, re.DOTALL)
                        if match:
                            analysis = json.loads(match.group())
                        else:
                            analysis = {
                                "is_true_positive": True,
                                "confidence": 0.5,
                                "explanation": "Could not parse Claude response",
                                "suggested_fix": None,
                                "severity_adjustment": "same"
                            }
                else:
                    raise Exception(f"Claude API error: {response.status_code}")
                    
        except Exception as e:
            analysis = {
                "is_true_positive": True,
                "confidence": 0.5,
                "explanation": f"Claude analysis failed: {str(e)}",
                "suggested_fix": None,
                "severity_adjustment": "same"
            }
            
        # Cache result
        self._save_cached_result(cache_key, analysis)
        analysis["from_cache"] = False
        
        return analysis


# Factory function to create scanner
def create_semgrep_scanner(
    rules: Optional[List[str]] = None,
    timeout: int = 300
) -> SemgrepScanner:
    """Create and configure a Semgrep scanner"""
    return SemgrepScanner(rules=rules, timeout=timeout)


def create_claude_analyzer(api_key: str) -> ClaudeAnalyzer:
    """Create and configure a Claude analyzer"""
    return ClaudeAnalyzer(api_key=api_key)
