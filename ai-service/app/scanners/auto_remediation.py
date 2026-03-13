"""
Auto-Remediation Service
Automatically fix common security vulnerabilities
"""

import re
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass


@dataclass
class Fix:
    vulnerability_type: str
    original_code: str
    fixed_code: str
    explanation: str
    confidence: float  # 0-1


class AutoRemediator:
    """
    Automatically fix common security vulnerabilities
    """
    
    # Remediation rules
    RULES = {
        # SQL Injection
        "sql_injection": {
            "pattern": r'["\']?(?:SELECT|INSERT|UPDATE|DELETE|DROP|CREATE|ALTER).*?["\']?\s*\+\s*',
            "fix": lambda match: "Use parameterized queries instead",
            "template": "cursor.execute('{}', ({},))"
        },
        
        # Command Injection
        "command_injection": {
            "pattern": r'(?:os\.system|os\.popen|subprocess\.call|subprocess\.run)\s*\(\s*(?!["\'])',
            "fix": "Use subprocess with shell=False and argument list",
            "template": "subprocess.run({}, shell=False, args=[{}])"
        },
        
        # Hardcoded Password
        "hardcoded_password": {
            "pattern": r'password\s*[:=]\s*["\'][^"\']{8,}["\']',
            "fix": "Use environment variables or secrets manager",
            "template": "password = os.environ.get('PASSWORD')"
        },
        
        # Hardcoded API Key
        "hardcoded_api_key": {
            "pattern": r'(?:api_key|apikey|apiSecret)\s*[:=]\s*["\'][A-Za-z0-9]{20,}["\']',
            "fix": "Use environment variables",
            "template": "api_key = os.environ.get('API_KEY')"
        },
        
        # Eval Usage
        "eval_usage": {
            "pattern": r'\beval\s*\(',
            "fix": "Avoid eval(), use ast.literal_eval for literals or refactor",
            "template": "# Replace eval() with safe alternative"
        },
        
        # Pickle Usage
        "pickle_usage": {
            "pattern": r'pickle\.(?:load|loads)\s*\(',
            "fix": "Use weights_only=True or switch to safer format like ONNX",
            "template": "torch.load({}, weights_only=True)"
        },
        
        # SQL with string formatting
        "sql_string_format": {
            "pattern": r'(?:cursor|db|connection)\.(?:execute|query)\s*\(\s*f?["\']',
            "fix": "Use parameterized queries",
            "template": "cursor.execute('SELECT * FROM users WHERE id = %s', (user_id,))"
        },
        
        # Weak Cryptography
        "weak_crypto": {
            "pattern": r'(?:md5|sha1)\s*\(',
            "fix": "Use bcrypt or argon2 for passwords, SHA-256 for checksums",
            "template": "hashlib.sha256(data).hexdigest()"
        },
        
        # Insecure Random
        "insecure_random": {
            "pattern": r'random\.(?:random|randint)\s*\(',
            "fix": "Use secrets module for cryptographic randomness",
            "template": "secrets.token_hex(32)"
        },
        
        # Path Traversal
        "path_traversal": {
            "pattern": r'(?:open|file|Path)\s*\([^)]*(?:\.\.|/etc/passwd)',
            "fix": "Validate and sanitize file paths, use os.path.realpath()",
            "template": "# Validate path is within allowed directory"
        },
        
        # XSS - InnerHTML
        "xss_innerHTML": {
            "pattern": r'innerHTML\s*=\s*',
            "fix": "Use textContent or sanitize with DOMPurify",
            "template": "element.textContent = userInput  # Safe alternative"
        },
        
        # YAML Unsafe Load
        "yaml_unsafe": {
            "pattern": r'yaml\.(?:load)\s*\(',
            "fix": "Use yaml.safe_load()",
            "template": "yaml.safe_load({})"
        },
        
        # JWT None Algorithm
        "jwt_none": {
            "pattern": r'algorithm\s*[:=]\s*["\']?none["\']?',
            "fix": "Always verify JWT signatures with proper algorithm",
            "template": "jwt.decode(token, key, algorithms=['HS256'])"
        },
        
        # Hardcoded Secret
        "hardcoded_secret": {
            "pattern": r'(?:secret|token|auth)[_-]?key\s*[:=]\s*["\'][^"\']+["\']',
            "fix": "Use environment variables",
            "template": "secrets = os.environ.get('{}')"
        }
    }
    
    def __init__(self):
        self.fixes: List[Fix] = []
        
    def analyze(self, code: str, language: str = "python") -> List[Dict]:
        """
        Analyze code and generate fixes
        """
        fixes = []
        
        for vuln_type, rule in self.RULES.items():
            pattern = rule.get("pattern", "")
            
            for match in re.finditer(pattern, code, re.IGNORECASE | re.MULTILINE):
                original = match.group(0)
                
                # Get line number
                line_num = code[:match.start()].count('\n') + 1
                
                fix_info = rule.get("fix", "No automatic fix available")
                template = rule.get("template", "")
                
                # Generate explanation
                explanation = self._generate_explanation(vuln_type, original)
                
                # Calculate confidence
                confidence = self._calculate_confidence(vuln_type, original)
                
                fixes.append({
                    "vulnerability_type": vuln_type,
                    "severity": self._get_severity(vuln_type),
                    "line_number": line_num,
                    "original_code": original.strip()[:100],
                    "explanation": explanation,
                    "fix_suggestion": template,
                    "confidence": confidence,
                    "can_auto_fix": bool(template) and confidence > 0.7
                })
        
        return fixes
    
    def _generate_explanation(self, vuln_type: str, code: str) -> str:
        """Generate human-readable explanation"""
        explanations = {
            "sql_injection": "This code is vulnerable to SQL injection. User input is directly concatenated into SQL queries, allowing attackers to manipulate the query.",
            "command_injection": "This code executes system commands unsafely. An attacker could inject malicious commands through user input.",
            "hardcoded_password": "Hardcoded passwords are a security risk. They can be discovered through code review or repository leaks.",
            "hardcoded_api_key": "API keys should not be hardcoded. They should be stored in environment variables or a secrets manager.",
            "eval_usage": "eval() can execute arbitrary code. It's dangerous with any untrusted input and should be avoided.",
            "pickle_usage": "Unsafe pickle deserialization can lead to arbitrary code execution. Always use weights_only=True or safer formats.",
            "weak_crypto": "MD5 and SHA1 are cryptographically broken. Use SHA-256 or better for hashing, bcrypt/argon2 for passwords.",
            "path_traversal": "This code may be vulnerable to path traversal attacks. Validate that paths stay within allowed directories.",
            "xss_innerHTML": "Using innerHTML with user input can lead to XSS attacks. Use textContent or sanitize input.",
            "yaml_unsafe": "yaml.load() is unsafe. Use yaml.safe_load() to prevent arbitrary code execution."
        }
        return explanations.get(vuln_type, "Security vulnerability detected.")
    
    def _get_severity(self, vuln_type: str) -> str:
        """Get severity level"""
        critical = ["sql_injection", "command_injection", "pickle_usage", "yaml_unsafe"]
        high = ["hardcoded_password", "hardcoded_api_key", "jwt_none", "path_traversal"]
        medium = ["eval_usage", "weak_crypto", "xss_innerHTML", "hardcoded_secret"]
        
        if vuln_type in critical:
            return "critical"
        elif vuln_type in high:
            return "high"
        elif vuln_type in medium:
            return "medium"
        return "low"
    
    def _calculate_confidence(self, vuln_type: str, code: str) -> float:
        """Calculate confidence score"""
        base_confidence = {
            "sql_injection": 0.9,
            "command_injection": 0.85,
            "hardcoded_password": 0.95,
            "hardcoded_api_key": 0.95,
            "pickle_usage": 0.9,
            "eval_usage": 0.85,
            "weak_crypto": 0.8,
            "path_traversal": 0.7,
            "xss_innerHTML": 0.8,
            "yaml_unsafe": 0.95
        }
        return base_confidence.get(vuln_type, 0.7)
    
    def generate_fix(self, code: str, vuln_type: str, language: str = "python") -> Optional[Dict]:
        """
        Generate actual fixed code
        """
        rule = self.RULES.get(vuln_type)
        if not rule:
            return None
            
        template = rule.get("template", "")
        
        # This is a simplified version - in production you'd use AST parsing
        return {
            "original": code[:100],
            "fixed": "# Fix requires manual review\n" + template,
            "requires_test": True,
            "notes": "Auto-generated fix. Review and test before deploying."
        }


def create_auto_remediator() -> AutoRemediator:
    return AutoRemediator()
