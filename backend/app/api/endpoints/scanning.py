from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import subprocess
import json
import tempfile
import os
import re
import shutil

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.models import User, Scan, Vulnerability

router = APIRouter(prefix="/api/scans", tags=["Scans"])


class ScanRequest(BaseModel):
    scan_type: str  # code, secrets, dependencies, python, javascript, go, docker, all
    target: str
    options: Optional[dict] = None


@router.post("/run", response_model=dict)
def run_scan(
    scan_data: ScanRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute security scans on the target"""
    
    scan = Scan(
        name=f"{scan_data.scan_type.title()} Scan - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
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
            results = {
                "semgrep": run_semgrep_scan(scan_data.target, scan_data.options or {}),
                "bandit": run_bandit_scan(scan_data.target, scan_data.options or {}),
                "gosec": run_gosec_scan(scan_data.target, scan_data.options or {}),
                "gitleaks": run_gitleaks_scan(scan_data.target, scan_data.options or {}),
                "pip_audit": run_pip_audit(scan_data.target, scan_data.options or {}),
                "npm_audit": run_npm_audit(scan_data.target, scan_data.options or {}),
            }
        elif scan_data.scan_type == "python":
            results = {
                "semgrep": run_semgrep_scan(scan_data.target, scan_data.options or {}),
                "bandit": run_bandit_scan(scan_data.target, scan_data.options or {}),
                "gosec": run_gosec_scan(scan_data.target, scan_data.options or {}),
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


def prepare_target(target: str) -> tuple:
    """Clone repo or use local path, return (path, cleanup_func)"""
    if target.startswith("http") or target.startswith("git@"):
        tmpdir = tempfile.mkdtemp()
        clone_result = subprocess.run(
            ["git", "clone", "--depth", "1", target, tmpdir],
            capture_output=True,
            text=True,
            timeout=60
        )
        if clone_result.returncode != 0:
            shutil.rmtree(tmpdir, ignore_errors=True)
            raise Exception(f"Failed to clone: {clone_result.stderr}")
        return tmpdir, lambda: shutil.rmtree(tmpdir, ignore_errors=True)
    elif os.path.isdir(target):
        return target, lambda: None
    else:
        tmpdir = tempfile.mkdtemp()
        return tmpdir, lambda: shutil.rmtree(tmpdir, ignore_errors=True)


def run_semgrep_scan(target: str, options: dict) -> dict:
    """Run Semgrep analysis"""
    rules = options.get("rules", "p/owasp-top-ten,p/sql-injection,p/xss,p/secrets")
    timeout = options.get("timeout", 120)
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["semgrep", "--config", rules, "--json", "--timeout", str(timeout), target_path],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        cleanup()
        
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


def run_bandit_scan(target: str, options: dict) -> dict:
    """Run Bandit Python security analysis"""
    timeout = options.get("timeout", 120)
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["bandit", "-r", target_path, "-f", "json", "-ll"],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        cleanup()
        
        output = json.loads(result.stdout) if result.stdout else {"results": []}
        
        vulnerabilities = []
        severity_map = {"HIGH": "high", "MEDIUM": "medium", "LOW": "low"}
        
        for finding in output.get("results", []):
            vuln = {
                "tool": "bandit",
                "title": finding.get("test_id", "") + ": " + finding.get("test_name", "Unknown"),
                "description": finding.get("issue_text", ""),
                "severity": severity_map.get(finding.get("issue_severity", "MEDIUM"), "medium"),
                "cwe_id": "CWE-" + str(finding.get("cwe_id", "?")),
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


def run_gosec_scan(target: str, options: dict) -> dict:
    """Run Gosec Go security analysis"""
    timeout = options.get("timeout", 120)
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["gosec", "-fmt", "json", "-no-fail", target_path],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        cleanup()
        
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


def run_gitleaks_scan(target: str, options: dict) -> dict:
    """Run Gitleaks secrets detection + regex fallback"""
    timeout = options.get("timeout", 120)
    gitleaks_path = options.get("gitleaks_path", "/tmp/gitleaks")
    
    vulnerabilities = []
    
    # Try Gitleaks first
    try:
        target_path, cleanup = prepare_target(target)
        
        # Initialize git repo for gitleaks
        subprocess.run(["git", "init"], cwd=target_path, capture_output=True)
        subprocess.run(["git", "add", "."], cwd=target_path, capture_output=True)
        subprocess.run(["git", "commit", "-m", "scan"], cwd=target_path, capture_output=True)
        
        result = subprocess.run(
            [gitleaks_path, "detect", "-s", target_path, "--report-format", "json", "-l", "error"],
            capture_output=True,
            text=True,
            timeout=timeout + 30
        )
        
        cleanup()
        
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
        pass  # Fallback to regex scanning
    
    # Regex fallback for secrets
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
        
        cleanup()
        
    except Exception:
        pass
    
    return {"vulnerabilities": vulnerabilities, "total": len(vulnerabilities)}


def run_pip_audit(target: str, options: dict) -> dict:
    """Run pip-audit for Python dependencies"""
    timeout = options.get("timeout", 120)
    
    try:
        result = subprocess.run(
            ["pip-audit", "--format=json", "--desc=on"],
            capture_output=True,
            text=True,
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


def run_npm_audit(target: str, options: dict) -> dict:
    """Run npm audit for JavaScript dependencies"""
    timeout = options.get("timeout", 120)
    
    try:
        target_path, cleanup = prepare_target(target)
        
        result = subprocess.run(
            ["npm", "audit", "--json"],
            capture_output=True,
            text=True,
            cwd=target_path,
            timeout=timeout + 30
        )
        
        cleanup()
        
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
                    "cwe_id": "CVE-" + vuln.get("VulnerabilityID", ""),
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


def extract_cwe(check_id: str) -> Optional[str]:
    """Extract CWE ID from check_id"""
    cwe_match = re.search(r'CWE-\d+', check_id, re.IGNORECASE)
    return cwe_match.group().upper() if cwe_match else None
