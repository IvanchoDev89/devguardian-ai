import re
from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class SecurityRule:
    name: str
    pattern: re.Pattern
    severity: str
    description: str


class InputValidator:
    SQL_INJECTION_PATTERNS = [
        r"(\b(SELECT|INSERT|UPDATE|DELETE|DROP|UNION|ALTER|CREATE|TRUNCATE)\b)",
        r"(--|;|'|\"|%27|%22|%3B)",
        r"\bOR\b\s+\d+=\d+",
        r"\bOR\b.*=.*",
        r"\bAND\b.*=.*",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",
        r"<iframe[^>]*>",
        r"eval\s*\(",
        r"expression\s*\(",
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        r"[;&|`$]",
        r"\b(cat|ls|dir|echo|wget|curl|nc|bash|sh)\b",
        r"(\|\s*\w+)",
        r"(\$\([^)]+\))",
    ]
    
    PATH_TRAVERSAL_PATTERNS = [
        r"\.\.[/\\]",
        r"/etc/passwd",
        r"/etc/shadow",
        r"C:\\Windows",
    ]
    
    def __init__(self):
        self.sql_rules = [
            SecurityRule(
                name="sql_keywords",
                pattern=re.compile(p, re.IGNORECASE),
                severity="high",
                description="SQL keyword or operator detected"
            )
            for p in self.SQL_INJECTION_PATTERNS
        ]
        
        self.xss_rules = [
            SecurityRule(
                name="xss_pattern",
                pattern=re.compile(p, re.IGNORECASE),
                severity="high",
                description="Potential XSS pattern detected"
            )
            for p in self.XSS_PATTERNS
        ]
        
        self.command_rules = [
            SecurityRule(
                name="command_injection",
                pattern=re.compile(p, re.IGNORECASE),
                severity="critical",
                description="Potential command injection detected"
            )
            for p in self.COMMAND_INJECTION_PATTERNS
        ]
        
        self.path_rules = [
            SecurityRule(
                name="path_traversal",
                pattern=re.compile(p, re.IGNORECASE),
                severity="high",
                description="Potential path traversal detected"
            )
            for p in self.PATH_TRAVERSAL_PATTERNS
        ]
    
    def validate_input(self, input_str: str) -> Dict[str, Any]:
        findings = []
        
        for rule in self.sql_rules:
            if rule.pattern.search(input_str):
                findings.append({
                    "rule": rule.name,
                    "severity": rule.severity,
                    "description": rule.description
                })
        
        for rule in self.xss_rules:
            if rule.pattern.search(input_str):
                findings.append({
                    "rule": rule.name,
                    "severity": rule.severity,
                    "description": rule.description
                })
        
        for rule in self.command_rules:
            if rule.pattern.search(input_str):
                findings.append({
                    "rule": rule.name,
                    "severity": rule.severity,
                    "description": rule.description
                })
        
        for rule in self.path_rules:
            if rule.pattern.search(input_str):
                findings.append({
                    "rule": rule.name,
                    "severity": rule.severity,
                    "description": rule.description
                })
        
        return {
            "is_safe": len(findings) == 0,
            "findings": findings,
            "severity": max([f["severity"] for f in findings], default="none")
        }
    
    def sanitize_input(self, input_str: str) -> str:
        sanitized = input_str
        
        sanitized = re.sub(r"[<>\"']", "", sanitized)
        
        sanitized = re.sub(r"javascript:", "", sanitized, flags=re.IGNORECASE)
        sanitized = re.sub(r"on\w+=", "", sanitized, flags=re.IGNORECASE)
        
        return sanitized


_validator: Optional[InputValidator] = None


def get_validator() -> InputValidator:
    global _validator
    if _validator is None:
        _validator = InputValidator()
    return _validator
