"""
Secret Scanner - Detect exposed API keys, tokens, and credentials
"""

import re
import hashlib
import hmac
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime


@dataclass
class SecretFinding:
    type: str
    severity: str
    line_number: int
    line_content: str
    match: str
    description: str
    remediation: str


class SecretScanner:
    """Scanner for detecting exposed secrets in code"""
    
    # Secret patterns with regex
    PATTERNS = {
        # AWS
        "aws_access_key": {
            "pattern": r"(?:A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}",
            "severity": "critical",
            "description": "AWS Access Key ID",
            "remediation": "Rotate the access key immediately. Use IAM roles instead of long-lived credentials."
        },
        "aws_secret_key": {
            "pattern": r"(?i)(?:aws(?:_secret)?_access(?:_key)?(?:_id)?|aws_secret_key|aws_secret_access_key)\s*[:=]\s*['\"]?[A-Za-z0-9/+=]{40}['\"]?",
            "severity": "critical",
            "description": "AWS Secret Access Key",
            "remediation": "Rotate the secret key. Use AWS Secrets Manager for credential storage."
        },
        
        # GitHub
        "github_token": {
            "pattern": r"ghp_[A-Za-z0-9]{36}",
            "severity": "critical",
            "description": "GitHub Personal Access Token",
            "remediation": "Revoke the token immediately in GitHub settings. Use GitHub Apps or OAuth instead."
        },
        "github_oauth": {
            "pattern": r"gho_[A-Za-z0-9]{36}",
            "severity": "critical",
            "description": "GitHub OAuth Access Token",
            "remediation": "Revoke the OAuth token in GitHub developer settings."
        },
        
        # GitLab
        "gitlab_token": {
            "pattern": r"glpat-[A-Za-z0-9\-]{20}",
            "severity": "critical",
            "description": "GitLab Personal Access Token",
            "remediation": "Revoke the token in GitLab User Settings > Access Tokens."
        },
        
        # OpenAI
        "openai_api_key": {
            "pattern": r"sk-[A-Za-z0-9]{32,}",
            "severity": "critical",
            "description": "OpenAI API Key",
            "remediation": "Revoke the API key in OpenAI platform. Use environment variables, never commit keys."
        },
        
        # Anthropic/Claude
        "anthropic_api_key": {
            "pattern": r"sk-ant-[A-Za-z0-9\-]{20,}",
            "severity": "critical",
            "description": "Anthropic API Key",
            "remediation": "Revoke the API key in Anthropic console."
        },
        
        # Stripe
        "stripe_api_key": {
            "pattern": r"(?:sk|pk)_(?:test|live)_[A-Za-z0-9]{24,}",
            "severity": "critical",
            "description": "Stripe API Key",
            "remediation": "Rotate in Stripe dashboard. Use test keys only in non-production."
        },
        
        # JWT
        "jwt_token": {
            "pattern": r"eyJ[A-Za-z0-9-_]+\.eyJ[A-Za-z0-9-_]+\.[A-Za-z0-9-_]+",
            "severity": "high",
            "description": "JWT Token",
            "remediation": "Ensure JWTs are not hardcoded. Use secure token storage."
        },
        
        # Generic API Keys
        "generic_api_key": {
            "pattern": r"(?:api[_-]?key|apikey|api[_-]?secret)\s*[:=]\s*['\"][A-Za-z0-9]{20,}['\"]",
            "severity": "high",
            "description": "Potential API Key",
            "remediation": "Move to environment variables or secrets manager."
        },
        
        # Passwords
        "hardcoded_password": {
            "pattern": r"(?:password|passwd|pwd)\s*[:=]\s*['\"][^'\"]{8,}['\"]",
            "severity": "high",
            "description": "Hardcoded Password",
            "remediation": "Use environment variables or secure password storage."
        },
        
        # Private Keys
        "private_key": {
            "pattern": r"-----BEGIN (?:RSA |EC |DSA |OPENSSH )?PRIVATE KEY-----",
            "severity": "critical",
            "description": "Private Key",
            "remediation": "Remove the private key. Use a secrets manager or key vault."
        },
        
        # Database URLs
        "database_url": {
            "pattern": r"(?:mysql|postgres|postgresql|mongodb|redis)://[^\s]+:[^\s]+@[^\s]+",
            "severity": "critical",
            "description": "Database Connection String with Credentials",
            "remediation": "Use environment variables for DB credentials. Never embed in code."
        },
        
        # Slack Tokens
        "slack_token": {
            "pattern": r"xox[baprs]-[0-9]{10,13}-[0-9]{10,13}[a-zA-Z0-9-]*",
            "severity": "critical",
            "description": "Slack Token",
            "remediation": "Revoke in Slack API settings. Use scoped tokens with minimal permissions."
        },
        
        # Telegram Bot Token
        "telegram_token": {
            "pattern": r"[0-9]{8,10}:[A-Za-z0-9_-]{35}",
            "severity": "high",
            "description": "Telegram Bot Token",
            "remediation": "Revoke via @BotFather and create new token."
        },
        
        # SendGrid
        "sendgrid_api_key": {
            "pattern": r"SG\.[A-Za-z0-9_-]{22}\.[A-Za-z0-9_-]{43}",
            "severity": "critical",
            "description": "SendGrid API Key",
            "remediation": "Revoke in SendGrid dashboard. Use environment variables."
        },
        
        # Twilio
        "twilio_api_key": {
            "pattern": r"SK[a-f0-9]{32}",
            "severity": "high",
            "description": "Twilio API Key",
            "remediation": "Revoke in Twilio Console. Use Auth Tokens instead."
        },
        
        # Firebase
        "firebase_key": {
            "pattern": r"AIza[0-9A-Za-z_-]{35}",
            "severity": "high",
            "description": "Firebase API Key",
            "remediation": "Restrict key in Google Cloud Console. Set HTTP referrer restrictions."
        },
        
        # Azure
        "azure_token": {
            "pattern": r"[A-Za-z0-9+/]{86}==",
            "severity": "high",
            "description": "Azure Access Token",
            "remediation": "Tokens should be short-lived. Use Managed Identities instead."
        },
        
        # Generic Secrets
        "generic_secret": {
            "pattern": r"(?:secret|token|auth)[_-]?(?:key|token)?\s*[:=]\s*['\"][A-Za-z0-9]{32,}['\"]",
            "severity": "medium",
            "description": "Potential Secret",
            "remediation": "Use a secrets manager like AWS Secrets Manager or HashiCorp Vault."
        }
    }
    
    # Files to exclude
    EXCLUDE_PATTERNS = [
        r"\.git/",
        r"node_modules/",
        r"vendor/",
        r"venv/",
        r"\.venv/",
        r"__pycache__/",
        r"\.env$",
        r"\.env\.example",
        r"\.env\.local$",
        r"package-lock\.json",
        r"yarn\.lock",
        r"requirements\.txt$",
        r"Pipfile\.lock",
        r"\.md$",
        r"test[_-]?",
        r"mock[_-]?",
        r"fake[_-]?",
        r"dummy[_-]?"
    ]
    
    def __init__(self):
        self.findings: List[SecretFinding] = []
        
    def scan_content(self, content: str, filename: str = "unknown") -> List[SecretFinding]:
        """Scan file content for secrets"""
        findings = []
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Skip comments and test files
            if self._should_skip_line(line, filename):
                continue
                
            for secret_type, config in self.PATTERNS.items():
                pattern = config["pattern"]
                match = re.search(pattern, line)
                
                if match:
                    finding = SecretFinding(
                        type=secret_type,
                        severity=config["severity"],
                        line_number=line_num,
                        line_content=line.strip()[:100],
                        match=match.group()[:50],
                        description=config["description"],
                        remediation=config["remediation"]
                    )
                    findings.append(finding)
                    
        return findings
    
    def scan_file(self, filepath: str) -> List[SecretFinding]:
        """Scan a single file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            return self.scan_content(content, filepath)
        except Exception:
            return []
    
    def scan_directory(self, directory: str) -> Dict[str, List[SecretFinding]]:
        """Scan entire directory"""
        results = {}
        
        for root, dirs, files in os.walk(directory):
            # Skip excluded directories
            dirs[:] = [d for d in dirs if not any(
                re.search(pattern, os.path.join(root, d)) 
                for pattern in self.EXCLUDE_PATTERNS
            )]
            
            for file in files:
                filepath = os.path.join(root, file)
                
                # Skip binary files and excluded patterns
                if any(re.search(pattern, filepath) for pattern in self.EXCLUDE_PATTERNS):
                    continue
                    
                findings = self.scan_file(filepath)
                if findings:
                    results[filepath] = findings
                    
        return results
    
    def _should_skip_line(self, line: str, filename: str) -> bool:
        """Check if line should be skipped (comments)"""
        line = line.strip()
        
        # Skip empty lines
        if not line:
            return True
            
        # Skip comments
        comment_starts = ['#', '//', '/*', '*/', '<!--', '--']
        if any(line.startswith(c) for c in comment_starts):
            return True
            
        return False
    
    def generate_report(self, findings: Dict[str, List[SecretFinding]]) -> Dict[str, Any]:
        """Generate a summary report"""
        total = sum(len(v) for v in findings.values())
        
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0
        }
        
        type_counts = {}
        
        for filepath, file_findings in findings.items():
            for finding in file_findings:
                severity_counts[finding.severity] = severity_counts.get(finding.severity, 0) + 1
                type_counts[finding.type] = type_counts.get(finding.type, 0) + 1
        
        return {
            "total_secrets_found": total,
            "files_with_secrets": len(findings),
            "severity_breakdown": severity_counts,
            "secret_types": type_counts,
            "findings": findings,
            "timestamp": datetime.utcnow().isoformat(),
            "recommendation": "Immediately rotate all exposed credentials and remove from code"
        }


import os

# Factory function
def create_secret_scanner() -> SecretScanner:
    return SecretScanner()


# CLI for testing
if __name__ == "__main__":
    import sys
    
    scanner = create_secret_scanner()
    
    if len(sys.argv) > 1:
        path = sys.argv[1]
        if os.path.isfile(path):
            findings = scanner.scan_file(path)
            print(f"Found {len(findings)} potential secrets in {path}")
            for f in findings:
                print(f"  [{f.severity.upper()}] {f.type} at line {f.line_number}")
        else:
            results = scanner.scan_directory(path)
            report = scanner.generate_report(results)
            print(f"Secrets Report:")
            print(f"  Total: {report['total_secrets_found']}")
            print(f"  Files: {report['files_with_secrets']}")
            print(f"  Critical: {report['severity_breakdown']['critical']}")
            print(f"  High: {report['severity_breakdown']['high']}")
    else:
        print("Usage: python secret_scanner.py <file_or_directory>")
