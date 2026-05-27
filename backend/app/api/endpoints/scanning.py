from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
import subprocess
import json
import tempfile
import os
import re
import shutil
import logging

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Scan, Vulnerability

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/scans", tags=["Scans"])


class ScanRequest(BaseModel):
    scan_type: str
    target: str
    options: Optional[dict] = None


def validate_target(target: str) -> bool:
    """Validate target to prevent command injection"""
    if not target or len(target) > 500:
        return False
    dangerous_chars = [';', '|', '`', '$', '&&', '||', '\n', '\r', '>', '<']
    for char in dangerous_chars:
        if char in target:
            return False
    return True


def validate_tool_path(path: str, allowed_paths: list[str]) -> str:
    import os.path
    normalized = os.path.normpath(path)
    for allowed in allowed_paths:
        if normalized.startswith(allowed):
            return normalized
    logger.warning(f"Tool path '{path}' not in allowed paths {allowed_paths}, falling back to '{allowed_paths[0]}'")
    return allowed_paths[0] if allowed_paths else "/usr/bin"


@router.post("/run", response_model=dict)
def run_scan(
    scan_data: ScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute security scans on the target"""
    
    if not validate_target(scan_data.target):
        raise HTTPException(status_code=400, detail="Invalid target. Target must be a valid URL, git repo, or local path.")
    
    if scan_data.options:
        scan_data.options["gitleaks_path"] = validate_tool_path(
            scan_data.options.get("gitleaks_path", "/usr/local/bin/gitleaks"),
            ["/usr/local/bin", "/usr/bin", "/tmp/tools"]
        )
        scan_data.options["trivy_path"] = validate_tool_path(
            scan_data.options.get("trivy_path", "/usr/bin/trivy"),
            ["/usr/bin", "/usr/local/bin"]
        )
    
    scan = Scan(
        name=f"{scan_data.scan_type.title()} Scan - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
        scan_type=scan_data.scan_type,
        target=scan_data.target,
        status="running",
        owner_id=current_user.id
    )
    db.add(scan)
    db.commit()
    db.refresh(scan)
    
    all_vulnerabilities = []
    
    try:
        if scan_data.scan_type == "all":
            target_path, target_cleanup = prepare_target(scan_data.target)
            try:
                results = {
                    "semgrep": run_semgrep_scan(target_path, scan_data.options or {}),
                    "bandit": run_bandit_scan(target_path, scan_data.options or {}),
                    "gosec": run_gosec_scan(target_path, scan_data.options or {}),
                    "gitleaks": run_gitleaks_scan(target_path, scan_data.options or {}),
                    "pip_audit": run_pip_audit(target_path, scan_data.options or {}),
                    "npm_audit": run_npm_audit(target_path, scan_data.options or {}),
                }
            finally:
                target_cleanup()
        elif scan_data.scan_type == "python":
            results = {
                "semgrep": run_semgrep_scan(scan_data.target, scan_data.options or {}),
                "bandit": run_bandit_scan(scan_data.target, scan_data.options or {}),
            }
        elif scan_data.scan_type == "secrets":
            results = {"gitleaks": run_gitleaks_scan(scan_data.target, scan_data.options or {})}
        elif scan_data.scan_type == "dependencies":
            results = {
                "pip_audit": run_pip_audit(scan_data.target, scan_data.options or {}),
                "npm_audit": run_npm_audit(scan_data.target, scan_data.options or {}),
            }
        elif scan_data.scan_type == "docker":
            results = {"trivy": run_trivy_scan(scan_data.target, scan_data.options or {})}
        elif scan_data.scan_type == "javascript":
            results = {
                "semgrep": run_semgrep_scan(scan_data.target, scan_data.options or {}),
                "npm_audit": run_npm_audit(scan_data.target, scan_data.options or {}),
            }
        elif scan_data.scan_type == "go":
            results = {
                "gosec": run_gosec_scan(scan_data.target, scan_data.options or {}),
                "semgrep": run_semgrep_scan(scan_data.target, scan_data.options or {}),
            }
        else:
            results = {"error": f"Unknown scan type: {scan_data.scan_type}"}
        
        for tool_name, tool_results in results.items():
            if isinstance(tool_results, dict) and "vulnerabilities" in tool_results:
                all_vulnerabilities.extend(tool_results["vulnerabilities"])
        
        scan.results = json.dumps(results)
        if isinstance(results, dict) and results.get("error"):
            scan.status = "failed"
        else:
            scan.status = "completed"
            scan.completed_at = datetime.utcnow()
        
        for vuln_data in all_vulnerabilities:
            vuln = Vulnerability(
                title=vuln_data.get("title", "Unknown"),
                description=vuln_data.get("description", ""),
                severity=vuln_data.get("severity", "medium"),
                cwe_id=vuln_data.get("cwe_id"),
                file_path=vuln_data.get("file_path"),
                line_number=vuln_data.get("line_number"),
                code_snippet=vuln_data.get("code_snippet"),
                fix_suggestion=vuln_data.get("fix_suggestion"),
                owner_id=current_user.id,
                scan_id=scan.id
            )
            db.add(vuln)
        
        db.commit()
        
        return {
            "scan_id": scan.id,
            "status": "completed",
            "vulnerabilities_found": len(all_vulnerabilities),
            "results": results,
            "vulnerabilities": all_vulnerabilities[:20]
        }
        
    except Exception as e:
        scan.status = "failed"
        scan.results = json.dumps({"error": str(e)})
        db.commit()
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


ALLOWED_GIT_HOSTS = [
    "github.com",
    "gitlab.com",
    "bitbucket.org",
    "gist.github.com",
]

BLOCKED_IP_RANGES = [
    "169.254.169.254",  # AWS metadata
    "metadata.google.internal",  # GCP metadata
    "metadata.google",
    "10.0.0.0/8",
    "172.16.0.0/12",
    "192.168.0.0/16",
    "127.0.0.0/8",
    "localhost",
    "0.0.0.0",
]


def is_ip_blocked(host: str) -> bool:
    """Check if host is a blocked IP or internal IP"""
    import ipaddress
    for blocked in BLOCKED_IP_RANGES:
        try:
            if "/" in blocked:
                network = ipaddress.ip_network(blocked, strict=False)
                try:
                    ip = ipaddress.ip_address(host)
                    if ip in network:
                        return True
                except ValueError:
                    pass
            elif host == blocked or host.startswith(blocked):
                return True
        except ValueError:
            continue
    return False


def validate_git_url(url: str) -> bool:
    """Validate git URL to prevent SSRF and command injection"""
    from urllib.parse import urlparse
    
    if url.startswith("git@"):
        parts = url.split(":")
        if len(parts) < 2:
            return False
        host = parts[0].replace("git@", "")
        if host not in ALLOWED_GIT_HOSTS:
            return False
        return True
    
    try:
        parsed = urlparse(url)
        host = parsed.hostname
        
        if not host:
            return False
        
        if host in ["localhost", "127.0.0.1", "0.0.0.0"]:
            return False
        
        if is_ip_blocked(host):
            logger.warning(f"Blocked SSRF attempt to: {host}")
            return False
        
        if host not in ALLOWED_GIT_HOSTS:
            return False
        
        return True
    except Exception as e:
        logger.error(f"URL validation error: {e}")
        return False


def prepare_target(target: str) -> tuple:
    """Clone repo or use local path, return (path, cleanup_func)"""
    if target.startswith("http") or target.startswith("git@"):
        if not validate_git_url(target):
            raise Exception("Invalid or disallowed git URL. Only GitHub, GitLab, and Bitbucket are allowed.")
        
        tmpdir = tempfile.mkdtemp()
        try:
            clone_result = subprocess.run(
                ["git", "clone", "--depth", "1", target, tmpdir],
                capture_output=True,
                text=True,
                timeout=60,
                env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
            )
            if clone_result.returncode != 0:
                shutil.rmtree(tmpdir, ignore_errors=True)
                raise Exception(f"Failed to clone: {clone_result.stderr}")
            return tmpdir, lambda: shutil.rmtree(tmpdir, ignore_errors=True)
        except Exception as e:
            shutil.rmtree(tmpdir, ignore_errors=True)
            raise Exception(f"Clone failed: {str(e)}")
    elif os.path.isdir(target):
        safe_path = os.path.realpath(target)
        if not safe_path.startswith("/home") and not safe_path.startswith("/tmp"):
            raise Exception("Local paths must be in /home or /tmp directories")
        return target, lambda: None
    else:
        raise Exception("Invalid target. Must be a git URL or local directory.")


ALLOWED_SEMGREP_RULES = {
    "p/owasp-top-ten", "p/sql-injection", "p/xss", "p/secrets",
    "p/command-injection", "p/security-audit", "p/rust",
    "p/python", "p/javascript", "p/java", "p/go",
}

def run_semgrep_scan(target: str, options: dict) -> dict:
    """Run Semgrep analysis"""
    rules_raw = options.get("rules", "p/owasp-top-ten,p/sql-injection,p/xss,p/secrets")
    rules_list = [r.strip() for r in rules_raw.split(",")]
    allowed = [r for r in rules_list if r in ALLOWED_SEMGREP_RULES]
    if not allowed:
        allowed = ["p/owasp-top-ten"]
        logger.warning(f"No allowed semgrep rules in '{rules_raw}', using defaults")
    rules = ",".join(allowed)
    timeout = options.get("timeout", 120)
    cleanup = lambda: None
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["semgrep", "--config", rules, "--json", "--timeout", str(timeout), target_path],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        if result.returncode not in [0, 1]:
            return {"error": f"Semgrep error: {result.stderr}", "vulnerabilities": []}
        
        findings = json.loads(result.stdout) if result.stdout else {"results": []}
        
        vulnerabilities = []
        severity_map = {"ERROR": "high", "WARNING": "medium", "INFO": "low"}
        
        for finding in findings.get("results", []):
            vuln = {
                "tool": "semgrep",
                "title": finding.get("check_id", "Unknown"),
                "description": finding.get("message", ""),
                "severity": severity_map.get(finding.get("severity", "WARNING"), "medium"),
                "cwe_id": extract_cwe(finding.get("check_id", "")),
                "file_path": finding.get("path", ""),
                "line_number": finding.get("start", {}).get("line"),
                "code_snippet": finding.get("extra", {}).get("lines", "")[:200],
                "fix_suggestion": f"Review {finding.get('path', 'code')} at line {finding.get('start', {}).get('line')}"
            }
            vulnerabilities.append(vuln)
        
        return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}
        
    except subprocess.TimeoutExpired:
        return {"error": "Semgrep timed out", "vulnerabilities": []}
    except FileNotFoundError:
        return {"error": "Semgrep not installed", "vulnerabilities": []}
    except Exception as e:
        return {"error": str(e), "vulnerabilities": []}
    finally:
        cleanup()


def run_bandit_scan(target: str, options: dict) -> dict:
    """Run Bandit Python security analysis"""
    timeout = options.get("timeout", 120)
    cleanup = lambda: None
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["bandit", "-r", target_path, "-f", "json", "-ll"],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        output = json.loads(result.stdout) if result.stdout else {"results": []}
        
        vulnerabilities = []
        severity_map = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
        
        for finding in output.get("results", []):
            vuln = {
                "tool": "bandit",
                "title": finding.get("test_id", "") + ": " + finding.get("test_name", "Unknown"),
                "description": finding.get("issue_text", ""),
                "severity": severity_map.get(finding.get("issue_severity", "MEDIUM"), "medium"),
                "cwe_id": ("CWE-" + str(finding["cwe_id"])) if finding.get("cwe_id") else None,
                "file_path": finding.get("filename", ""),
                "line_number": finding.get("line_number"),
                "code_snippet": finding.get("code", "")[:200],
                "fix_suggestion": finding.get("issue_text", "").split(". For example:")[0] if "." in finding.get("issue_text", "") else "Review and fix the security issue"
            }
            vulnerabilities.append(vuln)
        
        return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}
        
    except subprocess.TimeoutExpired:
        return {"error": "Bandit timed out", "vulnerabilities": []}
    except FileNotFoundError:
        return {"error": "Bandit not installed", "vulnerabilities": []}
    except Exception as e:
        return {"error": str(e), "vulnerabilities": []}
    finally:
        cleanup()


def run_gosec_scan(target: str, options: dict) -> dict:
    """Run Gosec Go security analysis"""
    timeout = options.get("timeout", 120)
    cleanup = lambda: None
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["gosec", "-fmt", "json", "-no-fail", target_path],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        if not result.stdout:
            return {"vulnerabilities": [], "total": 0}
        
        output = json.loads(result.stdout)
        
        vulnerabilities = []
        severity_map = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
        
        for issue in output.get("Issues", []):
            vuln = {
                "tool": "gosec",
                "title": issue.get("rule_id", "Unknown"),
                "description": issue.get("details", ""),
                "severity": severity_map.get(issue.get("severity", "MEDIUM"), "medium"),
                "cwe_id": issue.get("cwe", ""),
                "file_path": issue.get("file", ""),
                "line_number": issue.get("line"),
                "code_snippet": issue.get("code", "")[:200],
                "fix_suggestion": "Review Go code for " + issue.get("rule_id", "security issue")
            }
            vulnerabilities.append(vuln)
        
        return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}
        
    except subprocess.TimeoutExpired:
        return {"error": "Gosec timed out", "vulnerabilities": []}
    except FileNotFoundError:
        return {"error": "Gosec not installed", "vulnerabilities": []}
    except Exception as e:
        return {"error": str(e), "vulnerabilities": []}
    finally:
        cleanup()


def run_gitleaks_scan(target: str, options: dict) -> dict:
    """Run Gitleaks secrets detection + regex fallback"""
    timeout = options.get("timeout", 120)
    gitleaks_path = options.get("gitleaks_path", "/tmp/gitleaks")
    cleanup = lambda: None
    
    vulnerabilities = []
    
    # Try Gitleaks first
    try:
        target_path, cleanup = prepare_target(target)
        
        is_temp_dir = target_path.startswith('/tmp/')
        if is_temp_dir:
            git_config = {"GIT_TERMINAL_PROMPT": "0"}
            subprocess.run(["git", "init"], cwd=target_path, capture_output=True, env={**os.environ, **git_config})
            subprocess.run(["git", "config", "user.email", "scan@devguardian.ai"], cwd=target_path, capture_output=True)
            subprocess.run(["git", "config", "user.name", "DevGuardian Scan"], cwd=target_path, capture_output=True)
            subprocess.run(["git", "add", "."], cwd=target_path, capture_output=True)
            subprocess.run(["git", "commit", "-m", "scan"], cwd=target_path, capture_output=True)
        
        result = subprocess.run(
            [gitleaks_path, "detect", "-s", target_path, "--report-format", "json", "-l", "error"],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        if result.stdout:
            for line in result.stdout.strip().split('\n'):
                if not line.strip():
                    continue
                try:
                    finding = json.loads(line)
                    vuln = {
                        "tool": "gitleaks",
                        "title": "Secret Detected: " + finding.get("RuleID", "Unknown"),
                        "description": f"Hardcoded secret found in {finding.get('File', 'unknown')}",
                        "severity": "critical",
                        "cwe_id": "CWE-798",
                        "file_path": finding.get("File", ""),
                        "line_number": finding.get("StartLine"),
                        "code_snippet": finding.get("Match", "")[:100],
                        "fix_suggestion": "Remove hardcoded secrets. Use environment variables instead."
                    }
                    vulnerabilities.append(vuln)
                except json.JSONDecodeError:
                    continue
                    
    except Exception as e:
        logger.warning(f"Gitleaks scan failed, falling back to regex: {e}")
    finally:
        cleanup()
    
    # Regex fallback for secrets
    cleanup = lambda: None
    try:
        target_path, cleanup = prepare_target(target)
        
        secret_patterns = [
            (r'["\']?(api[_-]?key|secret[_-]?key|access[_-]?key)["\']?\s*[=:]\s*["\'][a-zA-Z0-9]{20,}["\']', "Hardcoded API Key"),
            (r'["\']?password["\']?\s*[=:]\s*["\'][^"\']{8,}["\']', "Hardcoded Password"),
            (r'-----BEGIN\s+(RSA|EC|OPENSSH)?\s*PRIVATE\s+KEY-----', "Private Key Found"),
            (r'(?i)(aws[_-]?access[_-]?key|aws[_-]?secret)', "AWS Credentials"),
            (r'ghp_[a-zA-Z0-9]{36}', "GitHub Token"),
            (r'sk_live_[a-zA-Z0-9]{24,}', "Stripe Live Key"),
            (r'xox[baprs]-[a-zA-Z0-9]{10,}', "Slack Token"),
            (r'AIza[0-9A-Za-z_-]{35}', "Google API Key"),
        ]
        
        for root, dirs, files in os.walk(target_path):
            dirs[:] = [d for d in dirs if d not in ['.git', 'node_modules', '__pycache__', '.venv']]
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.json', '.yaml', '.yml', '.env', '.txt', '.sh')):
                    filepath = os.path.join(root, file)
                    try:
                        with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                            for i, line in enumerate(f, 1):
                                for pattern, title in secret_patterns:
                                    if re.search(pattern, line):
                                        vuln = {
                                            "tool": "regex-scan",
                                            "title": title,
                                            "description": f"Potential hardcoded secret in {file}",
                                            "severity": "critical",
                                            "cwe_id": "CWE-798",
                                            "file_path": filepath,
                                            "line_number": i,
                                            "code_snippet": line.strip()[:100],
                                            "fix_suggestion": "Use environment variables instead of hardcoded secrets"
                                        }
                                        vulnerabilities.append(vuln)
                    except Exception:
                        pass
        
    except Exception as e:
        logger.warning(f"Regex fallback scan failed: {e}")
    finally:
        cleanup()
    
    return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}


def run_pip_audit(target: str, options: dict) -> dict:
    """Run pip-audit for Python dependencies"""
    timeout = options.get("timeout", 120)
    cleanup = lambda: None
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["pip-audit", "--format=json", "--desc=on", "-r", f"{target_path}/requirements.txt"],
            capture_output=True,
            text=True,
            cwd=target_path,
            timeout=timeout + 30
        )
        
        if result.returncode not in [0, 1]:
            return {"error": result.stderr or "pip-audit failed", "vulnerabilities": []}
        
        output = json.loads(result.stdout) if result.stdout else []
        
        vulnerabilities = []
        
        for dep in output:
            for vuln in dep.get("vulns", []):
                vuln_data = {
                    "tool": "pip-audit",
                    "title": f"Vulnerable: {dep.get('name', 'unknown')}=={dep.get('version', '?')}",
                    "description": vuln.get("id", "") + ": " + vuln.get("description", ""),
                    "severity": "high",
                    "cwe_id": "CWE-1395",
                    "file_path": "requirements.txt or pyproject.toml",
                    "fix_suggestion": f"Update {dep.get('name', 'package')}: pip install --upgrade {dep.get('name', 'package')}"
                }
                vulnerabilities.append(vuln_data)
        
        return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}
        
    except subprocess.TimeoutExpired:
        return {"error": "pip-audit timed out", "vulnerabilities": []}
    except FileNotFoundError:
        return {"error": "pip-audit not installed", "vulnerabilities": []}
    except Exception as e:
        return {"error": str(e), "vulnerabilities": []}
    finally:
        cleanup()


def run_npm_audit(target: str, options: dict) -> dict:
    """Run npm audit for JavaScript dependencies"""
    timeout = options.get("timeout", 120)
    cleanup = lambda: None
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["npm", "audit", "--json"],
            capture_output=True,
            text=True,
            cwd=target_path,
            timeout=timeout + 30
        )
        
        if not result.stdout:
            return {"vulnerabilities": [], "total": 0}
        
        output = json.loads(result.stdout)
        
        vulnerabilities = []
        
        for vuln_id, vuln_data in output.get("vulnerabilities", {}).items():
            vuln = {
                "tool": "npm-audit",
                "title": f"npm: {vuln_id}",
                "description": vuln_data.get("title", ""),
                "severity": vuln_data.get("severity", "moderate"),
                "cwe_id": "CWE-1395",
                "file_path": "package.json",
                "fix_suggestion": f"npm audit fix or update {vuln_id}"
            }
            vulnerabilities.append(vuln)
        
        return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}
        
    except subprocess.TimeoutExpired:
        return {"error": "npm audit timed out", "vulnerabilities": []}
    except FileNotFoundError:
        return {"error": "npm not installed", "vulnerabilities": []}
    except Exception as e:
        return {"error": str(e), "vulnerabilities": []}
    finally:
        cleanup()


def run_trivy_scan(target: str, options: dict) -> dict:
    """Run Trivy container/Docker scanning"""
    timeout = options.get("timeout", 180)
    trivy_path = options.get("trivy_path", "/tmp/trivy")
    
    try:
        result = subprocess.run(
            [trivy_path, "image", "--format", "json", "--severity", "HIGH,CRITICAL,MEDIUM", target],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        if not result.stdout:
            return {"vulnerabilities": [], "total": 0}
        
        output = json.loads(result.stdout)
        
        vulnerabilities = []
        
        for result_item in output.get("Results", []):
            for vuln in result_item.get("Vulnerabilities", []) or []:
                vuln_data = {
                    "tool": "trivy",
                    "title": f"{vuln.get('PkgName', 'package')} {vuln.get('InstalledVersion', '')}",
                    "description": vuln.get("Description", ""),
                    "severity": vuln.get("Severity", "MEDIUM").lower(),
                    "cwe_id": (vuln.get("CweIDs") or [None])[0] if vuln.get("CweIDs") else None,
                    "file_path": f"Image: {target}",
                    "fix_suggestion": f"Upgrade to {vuln.get('FixedVersion', 'latest version')}"
                }
                vulnerabilities.append(vuln_data)
        
        return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}
        
    except subprocess.TimeoutExpired:
        return {"error": "Trivy timed out", "vulnerabilities": []}
    except FileNotFoundError:
        return {"error": "Trivy not found at " + trivy_path, "vulnerabilities": []}
    except Exception as e:
        return {"error": str(e), "vulnerabilities": []}


def _detect_vulnerabilities_from_code(code: str, filename: str) -> list:
    """Pattern-based vulnerability detection as fallback"""
    vulnerabilities = []
    
    # Common vulnerability patterns
    patterns = [
        {
            "pattern": r"eval\s*\(",
            "title": "Dangerous use of eval()",
            "description": "Using eval() with user input can lead to code injection",
            "severity": "high",
            "cwe_id": "CWE-95"
        },
        {
            "pattern": r"execute\s*\(",
            "title": "SQL query execution",
            "description": "Direct SQL execution can lead to injection attacks",
            "severity": "high",
            "cwe_id": "CWE-89"
        },
        {
            "pattern": r"subprocess\s*\.\s*call",
            "title": "Shell command injection risk",
            "description": "Using subprocess with shell=True can be dangerous",
            "severity": "high",
            "cwe_id": "CWE-78"
        },
        {
            "pattern": r"os\.system\s*\(",
            "title": "OS command execution",
            "description": "Direct OS command execution is risky",
            "severity": "high",
            "cwe_id": "CWE-78"
        },
        {
            "pattern": r"pickle\.loads?\s*\(",
            "title": "Insecure deserialization",
            "description": " unpickling untrusted data can lead to code execution",
            "severity": "critical",
            "cwe_id": "CWE-502"
        },
        {
            "pattern": r"yaml\.load\s*\(",
            "title": "Insecure YAML parsing",
            "description": "yaml.load without Loader is unsafe",
            "severity": "high",
            "cwe_id": "CWE-502"
        },
        {
            "pattern": r"hardcoded.*password|password\s*=\s*['\"]",
            "title": "Hardcoded password detected",
            "description": "Hardcoded passwords are a security risk",
            "severity": "high",
            "cwe_id": "CWE-259"
        },
        {
            "pattern": r"secret.*=.*['\"]",
            "title": "Hardcoded secret detected",
            "description": "Hardcoded API keys or secrets should not be in code",
            "severity": "high",
            "cwe_id": "CWE-798"
        },
        {
            "pattern": r"request\.params\[|request\.args\[",
            "title": "User input in request",
            "description": "Direct use of user input without validation",
            "severity": "medium",
            "cwe_id": "CWE-20"
        },
        {
            "pattern": r"innerHTML\s*=",
            "title": "Potential XSS vulnerability",
            "description": "Directly setting innerHTML can lead to XSS",
            "severity": "high",
            "cwe_id": "CWE-79"
        },
    ]
    
    for i, p in enumerate(patterns):
        matches = list(re.finditer(p["pattern"], code, re.IGNORECASE))
        for match in matches:
            line_num = code[:match.start()].count('\n') + 1
            
            # Get surrounding context
            lines = code.split('\n')
            start_line = max(0, line_num - 2)
            end_line = min(len(lines), line_num + 2)
            snippet = '\n'.join(lines[start_line:end_line])[:200]
            
            vulnerabilities.append({
                "tool": "pattern",
                "title": p["title"],
                "description": p["description"],
                "severity": p["severity"],
                "cwe_id": p["cwe_id"],
                "file_path": filename,
                "line_number": line_num,
                "code_snippet": snippet,
                "fix_suggestion": f"Review line {line_num}: {p['description']}"
            })
    
    return vulnerabilities


def extract_cwe(check_id: str) -> Optional[str]:
    """Extract CWE ID from check_id"""
    cwe_match = re.search(r'CWE-\d+', check_id, re.IGNORECASE)
    return cwe_match.group().upper() if cwe_match else None


class CodeScanRequest(BaseModel):
    code: str
    language: str = "python"
    filename: Optional[str] = None


@router.post("/scan-code", response_model=dict)
def scan_code(
    scan_data: CodeScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Scan code directly without cloning a repository"""
    
    language = scan_data.language.lower()
    filename = scan_data.filename or f"input.{language}"
    
    # Create temp file with the code
    with tempfile.NamedTemporaryFile(mode='w', suffix=f"_{filename}", delete=False) as f:
        f.write(scan_data.code)
        temp_path = f.name
    
    try:
        vulnerabilities = []
        
        # Scan based on language
        if language in ["python", "py"]:
            # Run Bandit
            try:
                result = subprocess.run(
                    ["bandit", "-r", temp_path, "-f", "json", "-ll"],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.stdout:
                    output = json.loads(result.stdout)
                    for finding in output.get("results", []):
                        vuln = {
                            "tool": "bandit",
                            "title": f"{finding.get('test_id', 'unknown')}: {finding.get('test_name', 'Unknown')}",
                            "description": finding.get("issue_text", ""),
                            "severity": {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}.get(finding.get("issue_severity", "MEDIUM"), "medium"),
                            "cwe_id": f"CWE-{finding.get('cwe_id', 'Unknown')}" if finding.get('cwe_id') else None,
                            "file_path": filename,
                            "line_number": finding.get("line_number"),
                            "code_snippet": finding.get("code", "")[:200],
                            "fix_suggestion": f"Fix: {finding.get('issue_text', 'Review and fix this issue')[:100]}"
                        }
                        vulnerabilities.append(vuln)
            except FileNotFoundError:
                pass
            except Exception as e:
                logger.warning(f"Bandit scan failed: {e}")
            
            # Run semgrep if available
            try:
                result = subprocess.run(
                    ["semgrep", "--config", "auto", "--json", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode in [0, 1] and result.stdout:
                    findings = json.loads(result.stdout)
                    for finding in findings.get("results", []):
                        vuln = {
                            "tool": "semgrep",
                            "title": finding.get("check_id", "Unknown"),
                            "description": finding.get("message", ""),
                            "severity": {"ERROR": "high", "WARNING": "medium", "INFO": "low"}.get(finding.get("severity", "WARNING"), "medium"),
                            "cwe_id": extract_cwe(finding.get("check_id", "")),
                            "file_path": filename,
                            "line_number": finding.get("start", {}).get("line"),
                            "code_snippet": finding.get("extra", {}).get("lines", "")[:200],
                            "fix_suggestion": f"Review {filename} at line {finding.get('start', {}).get('line')}"
                        }
                        vulnerabilities.append(vuln)
            except FileNotFoundError:
                pass
            except Exception as e:
                logger.warning(f"Semgrep scan failed: {e}")
        
        elif language in ["javascript", "js", "typescript", "ts"]:
            try:
                result = subprocess.run(
                    ["semgrep", "--config", "auto", "--json", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode in [0, 1] and result.stdout:
                    findings = json.loads(result.stdout)
                    for finding in findings.get("results", []):
                        vuln = {
                            "tool": "semgrep",
                            "title": finding.get("check_id", "Unknown"),
                            "description": finding.get("message", ""),
                            "severity": {"ERROR": "high", "WARNING": "medium", "INFO": "low"}.get(finding.get("severity", "WARNING"), "medium"),
                            "cwe_id": extract_cwe(finding.get("check_id", "")),
                            "file_path": filename,
                            "line_number": finding.get("start", {}).get("line"),
                            "code_snippet": finding.get("extra", {}).get("lines", "")[:200],
                            "fix_suggestion": f"Review {filename} at line {finding.get('start', {}).get('line')}"
                        }
                        vulnerabilities.append(vuln)
            except Exception as e:
                logger.warning(f"JS scan failed: {e}")
        
        else:
            # Generic scan with semgrep for other languages
            try:
                result = subprocess.run(
                    ["semgrep", "--config", "auto", "--json", temp_path],
                    capture_output=True,
                    text=True,
                    timeout=60
                )
                if result.returncode in [0, 1] and result.stdout:
                    findings = json.loads(result.stdout)
                    for finding in findings.get("results", []):
                        vuln = {
                            "tool": "semgrep",
                            "title": finding.get("check_id", "Unknown"),
                            "description": finding.get("message", ""),
                            "severity": {"ERROR": "high", "WARNING": "medium", "INFO": "low"}.get(finding.get("severity", "WARNING"), "medium"),
                            "cwe_id": extract_cwe(finding.get("check_id", "")),
                            "file_path": filename,
                            "line_number": finding.get("start", {}).get("line"),
                            "code_snippet": finding.get("extra", {}).get("lines", "")[:200],
                            "fix_suggestion": f"Review {filename} at line {finding.get('start', {}).get('line')}"
                        }
                        vulnerabilities.append(vuln)
            except Exception as e:
                logger.warning(f"Generic scan failed: {e}")
        
        # Add pattern-based vulnerability detection as fallback
        patterns = _detect_vulnerabilities_from_code(scan_data.code, filename)
        vulnerabilities.extend(patterns)
        
        # Save to database
        if vulnerabilities:
            scan = Scan(
                name=f"Code Scan - {language.upper()} - {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}",
                scan_type=f"code_{language}",
                target=f"direct_input:{filename}",
                status="completed",
                owner_id=current_user.id,
                completed_at=datetime.utcnow()
            )
            db.add(scan)
            db.commit()
            db.refresh(scan)
            
            for vuln_data in vulnerabilities:
                vuln = Vulnerability(
                    title=vuln_data.get("title", "Unknown"),
                    description=vuln_data.get("description", ""),
                    severity=vuln_data.get("severity", "medium"),
                    cwe_id=vuln_data.get("cwe_id"),
                    file_path=vuln_data.get("file_path"),
                    line_number=vuln_data.get("line_number"),
                    code_snippet=vuln_data.get("code_snippet"),
                    fix_suggestion=vuln_data.get("fix_suggestion"),
                    owner_id=current_user.id,
                    scan_id=scan.id
                )
                db.add(vuln)
            db.commit()
        
        return {
            "scan_id": scan.id if vulnerabilities else None,
            "status": "completed",
            "vulnerabilities_found": len(vulnerabilities),
            "language": language,
            "vulnerabilities": vulnerabilities
        }
        
    finally:
        try:
            os.unlink(temp_path)
        except Exception:
            pass
