"""
Custom Security Rules Engine
Allow users to define their own security rules
"""

import re
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from datetime import datetime
import json


@dataclass
class SecurityRule:
    id: str
    name: str
    description: str
    pattern: str
    severity: str  # critical, high, medium, low
    enabled: bool = True
    language: str = "any"  # python, javascript, etc.
    category: str = "custom"
    remediation: str = ""
    created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class CustomRulesEngine:
    """Custom security rules engine"""
    
    # Default rules
    DEFAULT_RULES = [
        SecurityRule(
            id="custom_001",
            name="Debug Mode Enabled",
            description="Check for debug mode enabled in production",
            pattern=r"DEBUG\s*=\s*True",
            severity="high",
            remediation="Set DEBUG=False in production"
        ),
        SecurityRule(
            id="custom_002", 
            name="Console Log Exposed",
            description="Check for console.log in JavaScript",
            pattern=r"console\.log\(",
            severity="low",
            language="javascript",
            remediation="Remove console.log statements or use proper logging"
        ),
        SecurityRule(
            id="custom_003",
            name="TODO Comments",
            description="Check for TODO/FIXME comments",
            pattern=r"(TODO|FIXME|HACK|XXX):",
            severity="low",
            remediation="Address TODO comments before production"
        ),
        SecurityRule(
            id="custom_004",
            name="Print Statement",
            description="Check for print statements in Python",
            pattern=r"\bprint\(",
            severity="low",
            language="python",
            remediation="Use proper logging instead of print"
        ),
        SecurityRule(
            id="custom_005",
            name="Disabled SSL Verification",
            description="Check for disabled SSL verification",
            pattern=r"verify\s*=\s*False|ssl_verify\s*=\s*False",
            severity="critical",
            remediation="Enable SSL verification in production"
        ),
    ]
    
    def __init__(self):
        self.rules: Dict[str, SecurityRule] = {r.id: r for r in self.DEFAULT_RULES}
        self.user_rules: Dict[str, List[SecurityRule]] = {}
        
    def add_rule(self, user_id: str, rule: SecurityRule) -> bool:
        """Add a custom rule for a user"""
        if user_id not in self.user_rules:
            self.user_rules[user_id] = []
            
        # Check for duplicate pattern
        for existing in self.user_rules[user_id]:
            if existing.pattern == rule.pattern:
                return False
                
        self.rules[rule.id] = rule
        self.user_rules[user_id].append(rule)
        return True
    
    def remove_rule(self, user_id: str, rule_id: str) -> bool:
        """Remove a custom rule"""
        if rule_id not in self.rules:
            return False
            
        # Can only remove user rules, not defaults
        if not rule_id.startswith("custom_"):
            return False
            
        rule = self.rules.get(rule_id)
        if rule and user_id in self.user_rules:
            self.user_rules[user_id] = [r for r in self.user_rules[user_id] if r.id != rule_id]
            
        del self.rules[rule_id]
        return True
    
    def get_rules(self, user_id: str = None) -> List[Dict]:
        """Get all rules"""
        rules = list(self.rules.values())
        
        if user_id:
            # Filter to show only user's rules + enabled defaults
            user_rule_ids = [r.id for r in self.user_rules.get(user_id, [])]
            rules = [r for r in rules if r.enabled and (r.id in user_rule_ids or not r.id.startswith("custom_"))]
        
        return [
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "pattern": r.pattern,
                "severity": r.severity,
                "enabled": r.enabled,
                "language": r.language,
                "category": r.category,
                "remediation": r.remediation,
                "created_at": r.created_at
            }
            for r in rules
        ]
    
    def scan_with_rules(self, code: str, language: str = "any", user_id: str = None) -> List[Dict]:
        """Scan code with custom rules"""
        findings = []
        
        rules = [r for r in self.rules.values() if r.enabled]
        
        if user_id:
            # Include user's custom rules
            user_rules = self.user_rules.get(user_id, [])
            rules.extend([r for r in user_rules if r.enabled])
        
        for rule in rules:
            # Skip if language doesn't match
            if language != "any" and rule.language != "any" and rule.language != language:
                continue
                
            try:
                for match in re.finditer(rule.pattern, code, re.IGNORECASE | re.MULTILINE):
                    line_num = code[:match.start()].count('\n') + 1
                    findings.append({
                        "rule_id": rule.id,
                        "rule_name": rule.name,
                        "severity": rule.severity,
                        "line_number": line_num,
                        "match": match.group()[:100],
                        "description": rule.description,
                        "remediation": rule.remediation
                    })
            except re.error:
                continue
        
        return findings
    
    def validate_pattern(self, pattern: str) -> Dict:
        """Validate a regex pattern"""
        try:
            re.compile(pattern)
            return {"valid": True}
        except re.error as e:
            return {"valid": False, "error": str(e)}


def create_rules_engine() -> CustomRulesEngine:
    return CustomRulesEngine()
