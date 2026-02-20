"""
Simplified Security Analyzer - Works without PyTorch
"""

from typing import List, Dict, Any, Optional
import re
from enum import Enum


class VulnerabilityType(Enum):
    SQL_INJECTION = "sql_injection"
    XSS = "xss"
    PATH_TRAVERSAL = "path_traversal"
    COMMAND_INJECTION = "command_injection"
    INSECURE_DESERIALIZATION = "insecure_deserialization"
    WEAK_CRYPTOGRAPHY = "weak_cryptography"
    INFORMATION_DISCLOSURE = "information_disclosure"
    BROKEN_AUTHENTICATION = "broken_authentication"


class SeverityLevel(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


class SecurityVulnerabilityAnalyzer:
    """Pattern-based security vulnerability analyzer"""
    
    def __init__(self):
        self.vulnerability_patterns = {
            'sql_injection': [
                (r'SELECT.*\$\w+', SeverityLevel.HIGH, "CWE-89"),
                (r'UNION.*SELECT', SeverityLevel.HIGH, "CWE-89"),
                (r"'\s*OR\s*'.*'.*'", SeverityLevel.HIGH, "CWE-89"),
                (r'execute\s*\(\s*["\'].*\$', SeverityLevel.CRITICAL, "CWE-89"),
                (r'query\s*\(\s*["\'].*\$\w+', SeverityLevel.HIGH, "CWE-89"),
            ],
            'xss': [
                (r'innerHTML\s*=', SeverityLevel.HIGH, "CWE-79"),
                (r'document\.write\s*\(', SeverityLevel.MEDIUM, "CWE-79"),
                (r'eval\s*\(', SeverityLevel.CRITICAL, "CWE-79"),
                (r'<script>', SeverityLevel.CRITICAL, "CWE-79"),
            ],
            'command_injection': [
                (r'exec\s*\(', SeverityLevel.CRITICAL, "CWE-78"),
                (r'system\s*\(', SeverityLevel.CRITICAL, "CWE-78"),
                (r'shell_exec\s*\(', SeverityLevel.CRITICAL, "CWE-78"),
                (r'`.*\$\w+.*`', SeverityLevel.CRITICAL, "CWE-78"),
            ],
            'path_traversal': [
                (r'\.\./', SeverityLevel.HIGH, "CWE-22"),
                (r'\.\.\/', SeverityLevel.HIGH, "CWE-22"),
                (r'file_get_contents\s*\(\s*\$\w+', SeverityLevel.MEDIUM, "CWE-22"),
                (r'include\s*\(\s*\$\w+', SeverityLevel.MEDIUM, "CWE-22"),
            ],
            'insecure_deserialization': [
                (r'unserialize\s*\(', SeverityLevel.CRITICAL, "CWE-502"),
                (r'pickle\.loads\s*\(', SeverityLevel.CRITICAL, "CWE-502"),
                (r'yaml\.load\s*\(', SeverityLevel.CRITICAL, "CWE-502"),
            ],
            'hardcoded_credentials': [
                (r'password\s*=\s*["\'][^"\']{8,}["\']', SeverityLevel.HIGH, "CWE-798"),
                (r'api_key\s*=\s*["\']sk-[a-zA-Z0-9]{20,}', SeverityLevel.HIGH, "CWE-798"),
                (r'SECRET_KEY\s*=\s*["\'][^"\']{16,}["\']', SeverityLevel.HIGH, "CWE-798"),
            ],
            'weak_crypto': [
                (r'md5\s*\(', SeverityLevel.MEDIUM, "CWE-327"),
                (r'sha1\s*\(', SeverityLevel.MEDIUM, "CWE-327"),
                (r'DES\.new\s*\(', SeverityLevel.HIGH, "CWE-327"),
            ],
        }
    
    def analyze_code(self, code: str) -> List[Dict[str, Any]]:
        """Analyze code for vulnerabilities"""
        findings = []
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern, severity, cwe in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE)
                for match in matches:
                    findings.append({
                        'type': vuln_type,
                        'severity': severity.value,
                        'cwe_id': cwe,
                        'location': match.span(),
                        'match': match.group(),
                        'confidence': 85.0
                    })
        
        return findings
    
    def get_severity_score(self, severity: str) -> float:
        scores = {
            'critical': 9.0,
            'high': 7.0,
            'medium': 5.0,
            'low': 3.0,
            'info': 1.0
        }
        return scores.get(severity.lower(), 5.0)
