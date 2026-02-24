"""
0-Day Detection Engine - Simplified version without PyTorch
"""

from typing import List, Dict, Any, Optional
import re
from datetime import datetime


class VulnerabilityKnowledgeBase:
    """Knowledge base for vulnerabilities"""
    
    def __init__(self):
        self.cve_database = self._load_cve_database()
        self.cwe_database = self._load_cwe_database()
    
    def _load_cve_database(self) -> Dict:
        return {
            'CVE-2021-44228': {
                'name': 'Log4Shell',
                'cwe': 'CWE-917',
                'severity': 'critical',
                'cvss': 10.0
            },
            'CVE-2022-22965': {
                'name': 'Spring4Shell',
                'cwe': 'CWE-94',
                'severity': 'critical',
                'cvss': 9.8
            }
        }
    
    def _load_cwe_database(self) -> Dict:
        return {
            'CWE-79': {'name': 'XSS', 'category': 'Input Validation'},
            'CWE-89': {'name': 'SQL Injection', 'category': 'Injection'},
            'CWE-78': {'name': 'Command Injection', 'category': 'Injection'},
        }
    
    def lookup_cve(self, cve_id: str) -> Optional[Dict]:
        return self.cve_database.get(cve_id)
    
    def lookup_cwe(self, cwe_id: str) -> Optional[Dict]:
        return self.cwe_database.get(cwe_id)


class ZeroDayDetectionEngine:
    """Pattern-based 0-day detection (simplified)"""
    
    def __init__(self):
        self.known_patterns = self._load_patterns()
    
    def _load_patterns(self) -> Dict:
        return {
            'sql_injection': [
                r'execute\s*\(\s*["\'].*?\$',
                r'query\s*\(\s*["\'].*?\$',
                r'SELECT.*?\$\w+',
                r'INSERT.*?\$\w+',
                r'UPDATE.*?\$\w+',
                r'DELETE.*?\$\w+',
                r'\$_GET\[',
                r'\$_POST\[',
                r'\$_REQUEST\[',
            ],
            'xss': [
                r'innerHTML\s*=',
                r'document\.write\s*\(',
                r'eval\s*\(',
                r'\.html\s*\(',
                r'\.innerText\s*=',
            ],
            'command_injection': [
                r'exec\s*\(',
                r'system\s*\(',
                r'shell_exec\s*\(',
                r'passthru\s*\(',
                r'popen\s*\(',
                r'proc_open\s*\(',
            ],
            'code_injection': [
                r'eval\s*\(',
                r'assert\s*\(',
                r'create_function\s*\(',
                r'call_user_func\s*\(',
                r'call_user_func_array\s*\(',
                r'preg_replace.*?/e',
            ],
            'path_traversal': [
                r'\.\.\/',
                r'\.\.\\\\',
                r'file_get_contents\s*\(\s*\$',
                r'file_put_contents\s*\(\s*\$',
                r'fopen\s*\(\s*\$',
                r'readfile\s*\(\s*\$',
            ],
            'insecure_deserialization': [
                r'unserialize\s*\(',
                r'pickle\.loads\s*\(',
                r'yaml\.load\s*\(',
                r'marshal\.loads\s*\(',
                r'json\.loads\s*\(.*?request',
            ],
            'xxe': [
                r'SimpleXML.*?loadXML',
                r'DOMDocument.*?loadXML',
                r'XMLReader',
            ],
            'ssrf': [
                r'file_get_contents.*?http',
                r'curl_exec.*?\$',
                r'urllib.*?urlopen',
                r'requests\.get\s*\(',
            ],
            'hardcoded_secrets': [
                r'password\s*=\s*["\'][^"\']{8,}["\']',
                r'api_key\s*=\s*["\']sk-[a-zA-Z0-9]{20,}',
                r'SECRET_KEY\s*=\s*["\'][^"\']{16,}["\']',
                r'aws_access_key',
                r'aws_secret_key',
                r'-----BEGIN.*?PRIVATE KEY-----',
            ],
            'weak_crypto': [
                r'md5\s*\(',
                r'sha1\s*\(',
                r'DES\.new\s*\(',
                r'rc4',
            ],
            'ssrf_potential': [
                r'http.*?\$',
                r'url.*?\$',
                r'endpoint.*?\$',
                r'uri.*?\$',
            ]
        }
    
    def _get_severity(self, vuln_type: str) -> str:
        severity_map = {
            'sql_injection': 'critical',
            'command_injection': 'critical',
            'code_injection': 'critical',
            'insecure_deserialization': 'critical',
            'xxe': 'high',
            'ssrf': 'high',
            'xss': 'high',
            'path_traversal': 'high',
            'hardcoded_secrets': 'high',
            'weak_crypto': 'medium',
            'ssrf_potential': 'medium',
        }
        return severity_map.get(vuln_type, 'medium')
    
    def _get_cwe(self, vuln_type: str) -> str:
        cwe_map = {
            'sql_injection': 'CWE-89',
            'xss': 'CWE-79',
            'command_injection': 'CWE-78',
            'code_injection': 'CWE-94',
            'path_traversal': 'CWE-22',
            'insecure_deserialization': 'CWE-502',
            'xxe': 'CWE-611',
            'ssrf': 'CWE-918',
            'hardcoded_secrets': 'CWE-798',
            'weak_crypto': 'CWE-327',
        }
        return cwe_map.get(vuln_type, 'CWE-000')
    
    def detect_known_vulnerabilities(self, code: str) -> List[Dict]:
        findings = []
        seen = set()
        
        for vuln_type, patterns in self.known_patterns.items():
            for pattern in patterns:
                matches = re.finditer(pattern, code, re.IGNORECASE)
                for match in matches:
                    # Deduplicate findings
                    key = f"{vuln_type}:{match.group()[:30]}"
                    if key in seen:
                        continue
                    seen.add(key)
                    
                    severity = self._get_severity(vuln_type)
                    cwe = self._get_cwe(vuln_type)
                    
                    # Calculate confidence based on pattern specificity
                    confidence = 95.0 if len(pattern) > 20 else 85.0
                    
                    findings.append({
                        'type': vuln_type,
                        'severity': severity,
                        'cwe_id': cwe,
                        'confidence': confidence,
                        'is_zero_day': False,
                        'location': match.span(),
                        'match': match.group()[:50],
                        'description': f'Potential {vuln_type.replace("_", " ").title()} vulnerability detected'
                    })
        
        return findings
    
    async def detect_zero_days(self, code: str) -> List[Dict]:
        """Enhanced 0-day detection with anomaly detection"""
        findings = []
        
        # Check for suspicious patterns that might indicate 0-day vulnerabilities
        suspicious_patterns = [
            (r'dynamic\s+\w+\s*\(', 'Dynamic function execution', 'medium', 70.0),
            (r'assert\s*\(\s*\$', 'Dynamic assertion', 'high', 80.0),
            (r'preg_replace.*?\$.*?/', 'Dynamic regex replacement', 'high', 75.0),
            (r'\$\$\w+', 'Variable variables', 'medium', 65.0),
            (r'extract\s*\(\s*\$', 'Variable extraction', 'high', 80.0),
            (r'parse_str\s*\(\s*\$', 'Query string parsing', 'medium', 70.0),
            (r'ldap_\w+\s*\([^)]*\$', 'LDAP injection potential', 'high', 85.0),
            (r'header\s*\([^)]*\$', 'Dynamic header injection', 'medium', 70.0),
            (r'session_regenerate_id\s*\(\s*\)', 'Session fixation risk', 'low', 60.0),
            (r'mt_rand\s*\(', 'Weak random number generation', 'medium', 70.0),
            (r'rand\s*\(', 'Weak random number generation', 'medium', 65.0),
            (r'crypt\s*\(', 'Insecure crypt usage', 'medium', 70.0),
            (r'openssl_random_pseudo_bytes\s*\(\s*0\s*\)', 'Weak random bytes', 'high', 80.0),
        ]
        
        for pattern, description, severity, confidence in suspicious_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                findings.append({
                    'type': f'suspicious_pattern_{len(findings)}',
                    'severity': severity,
                    'confidence': confidence,
                    'is_zero_day': True,
                    'location': match.span(),
                    'match': match.group()[:30],
                    'description': description
                })
        
        # Check for code complexity issues
        if len(code) > 5000:
            findings.append({
                'type': 'large_codebase',
                'severity': 'low',
                'confidence': 50.0,
                'is_zero_day': True,
                'description': f'Large codebase ({len(code)} chars) - manual review recommended'
            })
        
        # Check for missing security controls
        if 'function' in code and 'auth' not in code.lower() and 'login' not in code.lower():
            # Potential missing authentication
            pass  # This is too noisy
        
        return findings
    
    async def analyze_code(self, code: str) -> Dict:
        known = self.detect_known_vulnerabilities(code)
        zero_days = await self.detect_zero_days(code)
        
        return {
            'total_findings': len(known) + len(zero_days),
            'known_vulnerabilities': len(known),
            'potential_zero_days': len(zero_days),
            'findings': known + zero_days,
            'risk_score': min((len(known) + len(zero_days)) * 2, 10),
            'recommendations': ['Review findings manually']
        }
