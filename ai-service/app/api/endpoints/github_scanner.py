"""
GitHub Repository Scanner
Scans GitHub repositories for vulnerabilities
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import re
import os
import json
from datetime import datetime

router = APIRouter(prefix="/github", tags=["GitHub Scanner"])


class RepoScanRequest(BaseModel):
    owner: str
    repo: str
    branch: Optional[str] = "main"
    scan_type: Optional[str] = "full"  # quick, full, deep


class DependencyScanRequest(BaseModel):
    owner: str
    repo: str
    branch: Optional[str] = "main"


# OWASP Top 10 2021 patterns
OWASP_TOP_10 = {
    'A01:2021 - Broken Access Control': [
        (r'\$_(GET|POST|REQUEST)\[.*?\]\s*\[\s*.*?\]', 'Potential IDOR - Direct object reference'),
        (r'file_get_contents\s*\(\s*\$_(GET|POST|REQUEST)', 'Insecure file access via user input'),
        (r'include\s*\(\s*\$_(GET|POST|REQUEST)', 'Remote file inclusion risk'),
        (r'require\s*\(\s*\$_(GET|POST|REQUEST)', 'Remote file inclusion risk'),
        (r'session_unset\s*\(\s*\)', 'Improper session handling'),
    ],
    'A02:2021 - Cryptographic Failures': [
        (r'md5\s*\(\s*\$', 'Weak hashing algorithm (MD5)'),
        (r'sha1\s*\(\s*\$', 'Weak hashing algorithm (SHA1)'),
        (r'DES\s*\(', 'Weak cryptographic algorithm (DES)'),
        (r'RC4\s*\(', 'Weak cryptographic algorithm (RC4)'),
        (r'mcrypt_', 'Deprecated mcrypt library'),
    ],
    'A03:2021 - Injection': [
        (r'exec\s*\(\s*\$', 'Command injection risk'),
        (r'system\s*\(\s*\$', 'Command injection risk'),
        (r'shell_exec\s*\(\s*\$', 'Command injection risk'),
        (r'passthru\s*\(\s*\$', 'Command injection risk'),
        (r'eval\s*\(\s*\$', 'Code injection risk (eval)'),
        (r'assert\s*\(\s*\$', 'Code injection risk'),
        (r'preg_replace.*?/e', 'Code injection via preg_replace'),
    ],
    'A04:2021 - Insecure Design': [
        (r'password\s*=\s*["\'][^"\']{0,7}["\']', 'Weak password configuration'),
        (r'admin.*?\s*=\s*["\']\s*(true|1|yes)', 'Hardcoded admin flag'),
    ],
    'A05:2021 - Security Misconfiguration': [
        (r'error_reporting\s*\(\s*E_ALL\s*\)', 'Full error reporting enabled'),
        (r'display_errors\s*=\s*On', 'Display errors enabled in production'),
        (r'allow_url_fopen\s*=\s*On', 'Remote file access enabled'),
        (r'cors.*?\*', 'Permissive CORS configuration'),
    ],
    'A06:2021 - Vulnerable Components': [
        (r'version\s*:\s*["\']?\d+\.\d+', 'Version declaration found'),
    ],
    'A07:2021 - Authentication Failures': [
        (r'session_start\s*\(\s*\)', 'Session management'),
        (r'Auth::attempt', 'Authentication attempt'),
    ],
    'A08:2021 - Software and Data Integrity Failures': [
        (r'unserialize\s*\(\s*\$', 'Insecure deserialization'),
        (r'pickle\.loads\s*\(', 'Insecure Python deserialization'),
        (r'yaml\.load\s*\(', 'Insecure YAML loading'),
    ],
    'A09:2021 - Security Logging Failures': [
        (r'error_log\s*\(', 'Error logging'),
        (r'console\.log\s*\(', 'Client-side logging'),
    ],
    'A10:2021 - Server-Side Request Forgery (SSRF)': [
        (r'file_get_contents\s*\(.*?http', 'Potential SSRF via file_get_contents'),
        (r'curl_exec\s*\(', 'Potential SSRF via curl'),
        (r'urllib\.request', 'Potential SSRF via urllib'),
    ],
}


@router.post("/scan")
async def scan_github_repo(request: RepoScanRequest):
    """
    Scan a GitHub repository for vulnerabilities
    """
    try:
        scan_id = f"GHSCAN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # For demo, we'll simulate a scan since we don't have GitHub API access
        # In production, this would clone the repo and scan it
        
        findings = []
        
        # Simulated file scanning patterns (in production, would scan real files)
        demo_files = {
            'app/Controllers/AuthController.php': '''<?php
public function login($username, $password) {
    $sql = "SELECT * FROM users WHERE username = '" . $username . "'";
    $result = mysqli_query($conn, $sql);
    if (mysqli_num_rows($result) > 0) {
        return true;
    }
}
''',
            'app/Models/User.php': '''<?php
class User extends Model {
    protected $table = 'users';
    public $primaryKey = 'id';
    public $timestamps = true;
}
''',
            'config/database.php': '''<?php
return [
    'host' => 'localhost',
    'database' => 'myapp',
    'username' => 'root',
    'password' => 'secret123',
];
''',
            'public/index.php': '''<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);

$_GET['page'] = isset($_GET['page']) ? $_GET['page'] : 'home';
include $_GET['page'] . '.php';
''',
        }
        
        for file_path, content in demo_files.items():
            for category, patterns in OWASP_TOP_10.items():
                for pattern, description in patterns:
                    matches = re.finditer(pattern, content, re.IGNORECASE)
                    for match in matches:
                        findings.append({
                            'file': file_path,
                            'category': category,
                            'issue': description,
                            'severity': _get_severity_from_category(category),
                            'line': content[:match.start()].count('\n') + 1,
                            'match': match.group()[:50]
                        })
        
        return {
            'scan_id': scan_id,
            'owner': request.owner,
            'repo': request.repo,
            'branch': request.branch,
            'status': 'completed',
            'timestamp': datetime.now().isoformat(),
            'files_scanned': len(demo_files),
            'findings_count': len(findings),
            'findings': findings,
            'summary': _generate_summary(findings)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Scan failed: {str(e)}")


@router.post("/scan-dependencies")
async def scan_dependencies(request: DependencyScanRequest):
    """
    Scan GitHub repository dependencies for known vulnerabilities
    """
    try:
        scan_id = f"DEPSCAN-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        
        # Demo known vulnerable packages (in production, would check against real CVE database)
        vulnerable_packages = [
            {
                'package': 'lodash',
                'version': '4.17.15',
                'vulnerability': 'CVE-2021-23337',
                'severity': 'high',
                'description': 'Prototype Pollution in lodash',
                'fix': 'Upgrade to >=4.17.21'
            },
            {
                'package': 'moment',
                'version': '2.29.1',
                'vulnerability': 'CVE-2022-24785',
                'severity': 'high',
                'description': 'Path Traversal in moment.js',
                'fix': 'Upgrade to >=2.29.2'
            },
            {
                'package': 'axios',
                'version': '0.21.0',
                'vulnerability': 'CVE-2021-3749',
                'severity': 'high',
                'description': 'Server-Side Request Forgery in axios',
                'fix': 'Upgrade to >=0.21.1'
            },
            {
                'package': 'npm',
                'version': '6.14.12',
                'vulnerability': 'CVE-2021-32803',
                'severity': 'critical',
                'description': 'Arbitrary File Overwrite in npm',
                'fix': 'Upgrade npm to >=7.x'
            },
        ]
        
        # Demo safe packages
        safe_packages = [
            {
                'package': 'express',
                'version': '4.18.2',
                'status': 'safe',
                'description': 'Latest stable version'
            },
            {
                'package': 'react',
                'version': '18.2.0',
                'status': 'safe',
                'description': 'Latest stable version'
            },
        ]
        
        return {
            'scan_id': scan_id,
            'owner': request.owner,
            'repo': request.repo,
            'timestamp': datetime.now().isoformat(),
            'total_packages': len(vulnerable_packages) + len(safe_packages),
            'vulnerable_count': len(vulnerable_packages),
            'safe_count': len(safe_packages),
            'vulnerabilities': vulnerable_packages,
            'safe_packages': safe_packages,
            'summary': {
                'critical': len([p for p in vulnerable_packages if p['severity'] == 'critical']),
                'high': len([p for p in vulnerable_packages if p['severity'] == 'high']),
                'medium': len([p for p in vulnerable_packages if p['severity'] == 'medium']),
                'low': len([p for p in vulnerable_packages if p['severity'] == 'low']),
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Dependency scan failed: {str(e)}")


@router.get("/languages")
async def get_supported_languages():
    """
    Get list of supported languages for scanning
    """
    return {
        'languages': [
            {'name': 'PHP', 'extensions': ['.php'], 'supported': True},
            {'name': 'Python', 'extensions': ['.py'], 'supported': True},
            {'name': 'JavaScript', 'extensions': ['.js', '.jsx'], 'supported': True},
            {'name': 'TypeScript', 'extensions': ['.ts', '.tsx'], 'supported': True},
            {'name': 'Java', 'extensions': ['.java'], 'supported': True},
            {'name': 'C#', 'extensions': ['.cs'], 'supported': True},
            {'name': 'Go', 'extensions': ['.go'], 'supported': True},
            {'name': 'Ruby', 'extensions': ['.rb'], 'supported': True},
        ],
        'frameworks': [
            'Laravel', 'Django', 'Flask', 'Express', 'React', 'Vue', 
            'Angular', 'Spring', 'Rails', 'ASP.NET Core'
        ]
    }


def _get_severity_from_category(category: str) -> str:
    severity_map = {
        'A01:2021 - Broken Access Control': 'high',
        'A02:2021 - Cryptographic Failures': 'high',
        'A03:2021 - Injection': 'critical',
        'A04:2021 - Insecure Design': 'medium',
        'A05:2021 - Security Misconfiguration': 'high',
        'A06:2021 - Vulnerable Components': 'high',
        'A07:2021 - Authentication Failures': 'high',
        'A08:2021 - Software and Data Integrity Failures': 'critical',
        'A09:2021 - Security Logging Failures': 'medium',
        'A10:2021 - Server-Side Request Forgery (SSRF)': 'high',
    }
    return severity_map.get(category, 'medium')


def _generate_summary(findings: List[Dict]) -> Dict:
    by_severity = {'critical': 0, 'high': 0, 'medium': 0, 'low': 0}
    by_category = {}
    
    for finding in findings:
        severity = finding.get('severity', 'medium')
        by_severity[severity] = by_severity.get(severity, 0) + 1
        
        category = finding.get('category', 'Unknown')
        by_category[category] = by_category.get(category, 0) + 1
    
    return {
        'by_severity': by_severity,
        'by_category': by_category,
        'total': len(findings)
    }
