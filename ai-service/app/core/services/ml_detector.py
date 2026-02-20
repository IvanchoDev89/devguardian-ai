"""
Simplified ML Detector - Works without PyTorch
"""

from typing import List, Dict, Any
import re
from collections import defaultdict


class SecurityMLDetector:
    """Rule-based security threat detector"""
    
    def __init__(self):
        self.threat_patterns = self._load_threat_patterns()
        self.risk_scores = {
            'critical': 10,
            'high': 7,
            'medium': 4,
            'low': 1
        }
        self.model_trained = True
        self.analyze_code_batch = self.detect_threats
    
    def _load_threat_patterns(self) -> Dict:
        return {
            'sql_injection': {
                'severity': 'critical',
                'patterns': [
                    r'execute\s*\(\s*["\'].*?\$',
                    r'query\s*\(\s*["\'].*?\$',
                    r'SELECT.*?FROM.*?WHERE.*?\$',
                    r'UNION\s+SELECT',
                ]
            },
            'xss': {
                'severity': 'high',
                'patterns': [
                    r'innerHTML\s*=',
                    r'document\.write\s*\(',
                    r'eval\s*\(',
                ]
            },
            'command_injection': {
                'severity': 'critical',
                'patterns': [
                    r'exec\s*\(',
                    r'system\s*\(',
                    r'shell_exec\s*\(',
                ]
            },
            'path_traversal': {
                'severity': 'high',
                'patterns': [
                    r'\.\.\/',
                    r'\.\.\\',
                ]
            },
            'hardcoded_secrets': {
                'severity': 'critical',
                'patterns': [
                    r'password\s*=\s*["\'][^"\']{8,}["\']',
                    r'api[_-]?key\s*=\s*["\'][a-zA-Z0-9]{20,}["\']',
                    r'secret[_-]?key\s*=\s*["\'][^"\']{16,}["\']',
                ]
            },
        }
    
    def detect_threats(self, code: str) -> List[Dict[str, Any]]:
        threats = []
        lines = code.split('\n')
        
        for threat_type, data in self.threat_patterns.items():
            for pattern in data['patterns']:
                for line_num, line in enumerate(lines, 1):
                    if re.search(pattern, line, re.IGNORECASE):
                        threats.append({
                            'type': threat_type,
                            'severity': data['severity'],
                            'line': line_num,
                            'code': line.strip(),
                            'confidence': 85.0
                        })
        
        return threats
    
    def calculate_risk_score(self, threats: List[Dict]) -> float:
        total = sum(self.risk_scores.get(t['severity'], 1) for t in threats)
        return min(total / 10, 10.0)
