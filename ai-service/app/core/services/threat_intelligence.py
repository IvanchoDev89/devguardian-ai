"""
Threat Intelligence Engine - Simplified version
"""

from typing import List, Dict, Any, Optional
from datetime import datetime
from enum import Enum


class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ThreatIntelligenceEngine:
    """Threat intelligence and vulnerability database"""
    
    def __init__(self):
        self.known_threats = self._load_threat_database()
        self.cve_database = self._load_cve_database()
    
    def _load_threat_database(self) -> Dict[str, Any]:
        return {
            'CVE-2021-44228': {
                'name': 'Log4Shell',
                'severity': 'critical',
                'cvss': 10.0,
                'description': 'Remote code execution in Apache Log4j',
                'affected': ['Log4j < 2.15.0']
            },
            'CVE-2022-22965': {
                'name': 'Spring4Shell',
                'severity': 'critical',
                'cvss': 9.8,
                'description': 'RCE in Spring Framework',
                'affected': ['Spring Framework < 5.3.18']
            },
            'CVE-2023-44487': {
                'name': 'HTTP/2 Rapid Reset',
                'severity': 'high',
                'cvss': 7.5,
                'description': 'DDoS vulnerability in HTTP/2',
                'affected': ['Multiple HTTP/2 servers']
            }
        }
    
    def _load_cve_database(self) -> Dict:
        return self.known_threats
    
    def lookup_cve(self, cve_id: str) -> Optional[Dict]:
        return self.known_threats.get(cve_id)
    
    def get_threat_level(self, severity: str) -> ThreatLevel:
        levels = {
            'critical': ThreatLevel.CRITICAL,
            'high': ThreatLevel.HIGH,
            'medium': ThreatLevel.MEDIUM,
            'low': ThreatLevel.LOW
        }
        return levels.get(severity.lower(), ThreatLevel.LOW)
