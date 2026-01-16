import torch
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import hashlib
from dataclasses import dataclass
from enum import Enum

class ThreatLevel(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

@dataclass
class ThreatSignature:
    """Threat signature data structure"""
    signature_id: str
    threat_type: str
    pattern: str
    severity: float
    confidence: float
    description: str
    mitigation: str
    created_at: datetime
    updated_at: datetime

class ThreatIntelligenceEngine:
    """AI-powered threat intelligence and analysis engine"""
    
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.threat_signatures = self._load_default_signatures()
        self.threat_history = []
        self.similarity_threshold = 0.8
        
        # Neural network for threat classification
        self.threat_classifier = self._build_threat_classifier()
        self.embedding_dim = 256
        
    def _build_threat_classifier(self) -> torch.nn.Module:
        """Build neural network for threat classification"""
        class ThreatClassifierNet(torch.nn.Module):
            def __init__(self, input_dim: int = 100, hidden_dim: int = 256, output_dim: int = 10):
                super(ThreatClassifierNet, self).__init__()
                self.embedding_dim = 256  # Add this attribute
                self.embedding_layer = torch.nn.Linear(input_dim, self.embedding_dim)
                self.attention = torch.nn.MultiheadAttention(self.embedding_dim, 4)
                self.classifier = torch.nn.Sequential(
                    torch.nn.Linear(self.embedding_dim, hidden_dim),
                    torch.nn.ReLU(),
                    torch.nn.Dropout(0.3),
                    torch.nn.Linear(hidden_dim, hidden_dim // 2),
                    torch.nn.ReLU(),
                    torch.nn.Dropout(0.3),
                    torch.nn.Linear(hidden_dim // 2, output_dim),
                    torch.nn.Softmax(dim=1)
                )
            
            def forward(self, x):
                # Embedding
                embedded = self.embedding_layer(x)
                embedded = embedded.unsqueeze(1)  # Add sequence dimension
                
                # Self-attention
                attended, _ = self.attention(embedded, embedded, embedded)
                attended = attended.squeeze(1)
                
                # Classification
                output = self.classifier(attended)
                return output
        
        return ThreatClassifierNet().to(self.device)
    
    def _load_default_signatures(self) -> Dict[str, ThreatSignature]:
        """Load default threat signatures"""
        signatures = {
            "sql_injection_001": ThreatSignature(
                signature_id="sql_injection_001",
                threat_type="sql_injection",
                pattern=r"(?i)(union|select|insert|update|delete|drop|exec|sp_)\s+",
                severity=9.0,
                confidence=0.95,
                description="SQL injection attack pattern detected",
                mitigation="Use parameterized queries and input validation",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            "xss_001": ThreatSignature(
                signature_id="xss_001",
                threat_type="xss",
                pattern=r"(?i)(<script|javascript:|on\w+\s*=|<iframe|eval\s*\()",
                severity=8.0,
                confidence=0.90,
                description="Cross-site scripting attack pattern",
                mitigation="Implement output encoding and CSP headers",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            "path_traversal_001": ThreatSignature(
                signature_id="path_traversal_001",
                threat_type="path_traversal",
                pattern=r"(?i)(\.\./|\.\.\\|%2e%2e%2f|/etc/passwd)",
                severity=7.0,
                confidence=0.85,
                description="Path traversal attack pattern",
                mitigation="Validate file paths and use chroot jails",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            "command_injection_001": ThreatSignature(
                signature_id="command_injection_001",
                threat_type="command_injection",
                pattern=r"(?i)(;.*rm|;.*cat|;.*ls|\|.*nc|`.*`|\$\([^)]*\))",
                severity=9.5,
                confidence=0.92,
                description="Command injection attack pattern",
                mitigation="Avoid shell commands with user input",
                created_at=datetime.now(),
                updated_at=datetime.now()
            ),
            "crypto_weakness_001": ThreatSignature(
                signature_id="crypto_weakness_001",
                threat_type="weak_crypto",
                pattern=r"(?i)(md5\s*\(|sha1\s*\(|base64_encode|crypt\s*\()",
                severity=5.0,
                confidence=0.80,
                description="Weak cryptographic algorithm detected",
                mitigation="Use modern cryptographic algorithms",
                created_at=datetime.now(),
                updated_at=datetime.now()
            )
        }
        return signatures
    
    def analyze_code_threats(self, code_content: str, file_path: str = "") -> Dict[str, Any]:
        """Analyze code for potential threats using multiple techniques"""
        analysis_result = {
            'file_path': file_path,
            'timestamp': datetime.now().isoformat(),
            'threats_detected': [],
            'risk_score': 0.0,
            'threat_level': ThreatLevel.LOW.value,
            'recommendations': [],
            'analysis_methods': []
        }
        
        # 1. Signature-based detection
        signature_threats = self._signature_based_detection(code_content)
        if signature_threats:
            analysis_result['threats_detected'].extend(signature_threats)
            analysis_result['analysis_methods'].append('signature_based')
        
        # 2. AI-based classification
        ai_threats = self._ai_based_classification(code_content)
        if ai_threats:
            analysis_result['threats_detected'].extend(ai_threats)
            analysis_result['analysis_methods'].append('ai_based')
        
        # 3. Behavioral analysis
        behavioral_threats = self._behavioral_analysis(code_content)
        if behavioral_threats:
            analysis_result['threats_detected'].extend(behavioral_threats)
            analysis_result['analysis_methods'].append('behavioral')
        
        # Calculate overall risk score
        if analysis_result['threats_detected']:
            max_severity = max(threat['severity'] for threat in analysis_result['threats_detected'])
            analysis_result['risk_score'] = min(max_severity, 10.0)
            
            # Determine threat level
            if analysis_result['risk_score'] >= 9.0:
                analysis_result['threat_level'] = ThreatLevel.CRITICAL.value
            elif analysis_result['risk_score'] >= 7.0:
                analysis_result['threat_level'] = ThreatLevel.HIGH.value
            elif analysis_result['risk_score'] >= 4.0:
                analysis_result['threat_level'] = ThreatLevel.MEDIUM.value
            else:
                analysis_result['threat_level'] = ThreatLevel.LOW.value
        
        # Generate recommendations
        analysis_result['recommendations'] = self._generate_recommendations(analysis_result['threats_detected'])
        
        # Store in threat history
        self.threat_history.append(analysis_result)
        
        return analysis_result
    
    def _signature_based_detection(self, code_content: str) -> List[Dict[str, Any]]:
        """Detect threats using signature patterns"""
        threats = []
        
        for sig_id, signature in self.threat_signatures.items():
            import re
            matches = re.finditer(signature.pattern, code_content)
            
            for match in matches:
                threat = {
                    'threat_id': sig_id,
                    'threat_type': signature.threat_type,
                    'severity': signature.severity,
                    'confidence': signature.confidence,
                    'description': signature.description,
                    'mitigation': signature.mitigation,
                    'matched_pattern': match.group(),
                    'line_number': code_content[:match.start()].count('\n') + 1,
                    'column': match.start() - code_content.rfind('\n', 0, match.start()),
                    'detection_method': 'signature_based'
                }
                threats.append(threat)
        
        return threats
    
    def _ai_based_classification(self, code_content: str) -> List[Dict[str, Any]]:
        """AI-based threat classification using neural network"""
        threats = []
        
        try:
            # Extract features for AI analysis
            features = self._extract_threat_features(code_content)
            
            # Convert to tensor
            features_tensor = torch.FloatTensor(features).unsqueeze(0).to(self.device)
            
            # Predict threat types
            with torch.no_grad():
                self.threat_classifier.eval()
                predictions = self.threat_classifier(features_tensor)
                
                # Get top predictions
                top_probs, top_indices = torch.topk(predictions, k=3)
                
                threat_types = ['sql_injection', 'xss', 'path_traversal', 'command_injection', 
                               'crypto_weakness', 'hardcoded_secrets', 'buffer_overflow', 
                               'injection', 'dos', 'reconnaissance']
                
                for i in range(len(top_indices[0])):
                    if top_probs[0][i].item() > 0.5:  # Confidence threshold
                        threat_type = threat_types[top_indices[0][i].item()]
                        threat = {
                            'threat_type': threat_type,
                            'severity': self._map_type_to_severity(threat_type),
                            'confidence': top_probs[0][i].item(),
                            'description': f'AI-detected {threat_type.replace("_", " ")} pattern',
                            'mitigation': self._get_ai_mitigation(threat_type),
                            'detection_method': 'ai_based',
                            'ai_confidence': top_probs[0][i].item()
                        }
                        threats.append(threat)
        
        except Exception as e:
            # Fallback if AI analysis fails
            pass
        
        return threats
    
    def _behavioral_analysis(self, code_content: str) -> List[Dict[str, Any]]:
        """Behavioral analysis for threat detection"""
        threats = []
        
        # Analyze code behavior patterns
        lines = code_content.split('\n')
        
        # Suspicious function calls
        suspicious_functions = [
            'eval', 'exec', 'system', 'shell_exec', 'passthru',
            'file_get_contents', 'fopen', 'include', 'require',
            'unserialize', 'base64_decode', 'openssl_decrypt'
        ]
        
        for line_num, line in enumerate(lines, 1):
            for func in suspicious_functions:
                if func in line.lower():
                    threat = {
                        'threat_type': 'suspicious_function_call',
                        'severity': 6.0,
                        'confidence': 0.7,
                        'description': f'Suspicious function call: {func}',
                        'mitigation': 'Review and validate function usage',
                        'matched_pattern': func,
                        'line_number': line_num,
                        'column': line.lower().find(func),
                        'detection_method': 'behavioral'
                    }
                    threats.append(threat)
        
        # Check for data exfiltration patterns
        exfiltration_patterns = [
            'curl', 'wget', 'file_get_contents', 'fsockopen',
            'mail(', 'base64_encode', 'json_encode'
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern in exfiltration_patterns:
                if pattern in line.lower():
                    threat = {
                        'threat_type': 'potential_data_exfiltration',
                        'severity': 7.0,
                        'confidence': 0.6,
                        'description': f'Potential data exfiltration pattern: {pattern}',
                        'mitigation': 'Review data handling and network calls',
                        'matched_pattern': pattern,
                        'line_number': line_num,
                        'column': line.lower().find(pattern),
                        'detection_method': 'behavioral'
                    }
                    threats.append(threat)
        
        return threats
    
    def _extract_threat_features(self, code_content: str) -> List[float]:
        """Extract features for AI-based threat analysis"""
        features = []
        
        # Basic code metrics
        features.append(len(code_content))  # Code length
        features.append(code_content.count('\n'))  # Number of lines
        features.append(len(set(code_content.split())))  # Unique tokens
        
        # Security-sensitive keywords
        security_keywords = [
            'password', 'secret', 'key', 'token', 'auth', 'login',
            'exec', 'eval', 'system', 'shell', 'cmd', 'sql',
            'file', 'read', 'write', 'upload', 'download'
        ]
        
        for keyword in security_keywords:
            features.append(code_content.lower().count(keyword))
        
        # Special characters and patterns
        features.append(code_content.count('<'))  # HTML tags
        features.append(code_content.count('>'))
        features.append(code_content.count('"'))  # Quotes
        features.append(code_content.count("'"))
        features.append(code_content.count(';'))  # Statements
        features.append(code_content.count('('))  # Function calls
        
        # Network-related patterns
        network_patterns = ['http', 'https', 'ftp', 'ssh', 'telnet']
        for pattern in network_patterns:
            features.append(code_content.lower().count(pattern))
        
        # Encoding patterns
        encoding_patterns = ['base64', 'hex', 'url', 'json']
        for pattern in encoding_patterns:
            features.append(code_content.lower().count(pattern))
        
        # Pad or truncate to fixed size
        while len(features) < 100:
            features.append(0.0)
        features = features[:100]
        
        return features
    
    def _map_type_to_severity(self, threat_type: str) -> float:
        """Map threat type to severity score"""
        severity_map = {
            'sql_injection': 9.0,
            'xss': 8.0,
            'path_traversal': 7.0,
            'command_injection': 9.5,
            'crypto_weakness': 5.0,
            'hardcoded_secrets': 6.0,
            'buffer_overflow': 8.5,
            'injection': 8.0,
            'dos': 6.5,
            'reconnaissance': 4.0
        }
        return severity_map.get(threat_type, 5.0)
    
    def _get_ai_mitigation(self, threat_type: str) -> str:
        """Get AI-generated mitigation for threat type"""
        mitigations = {
            'sql_injection': 'Use parameterized queries and input validation',
            'xss': 'Implement output encoding and Content Security Policy',
            'path_traversal': 'Validate file paths and use whitelist approach',
            'command_injection': 'Avoid system commands with user input',
            'crypto_weakness': 'Use modern cryptographic algorithms',
            'hardcoded_secrets': 'Store secrets in environment variables',
            'buffer_overflow': 'Use bounds checking and safe functions',
            'injection': 'Implement proper input validation and sanitization',
            'dos': 'Implement rate limiting and resource monitoring',
            'reconnaissance': 'Implement access controls and logging'
        }
        return mitigations.get(threat_type, 'Review and implement security best practices')
    
    def _generate_recommendations(self, threats: List[Dict[str, Any]]) -> List[str]:
        """Generate security recommendations based on detected threats"""
        recommendations = []
        
        if not threats:
            recommendations.append("No immediate security threats detected. Continue monitoring.")
            return recommendations
        
        # Count threat types
        threat_counts = {}
        for threat in threats:
            threat_type = threat['threat_type']
            threat_counts[threat_type] = threat_counts.get(threat_type, 0) + 1
        
        # Generate recommendations based on threat patterns
        if 'sql_injection' in threat_counts:
            recommendations.append("CRITICAL: Implement parameterized queries for all database operations.")
        
        if 'xss' in threat_counts:
            recommendations.append("HIGH: Implement output encoding and CSP headers to prevent XSS attacks.")
        
        if 'command_injection' in threat_counts:
            recommendations.append("CRITICAL: Review and secure all system command executions.")
        
        if 'hardcoded_secrets' in threat_counts:
            recommendations.append("MEDIUM: Move all hardcoded credentials to secure environment variables.")
        
        if len(threats) > 10:
            recommendations.append("HIGH: Large number of threats detected. Consider comprehensive security audit.")
        
        # Add general recommendations
        recommendations.append("Implement regular security scanning and monitoring.")
        recommendations.append("Keep all dependencies and frameworks updated to latest secure versions.")
        
        return recommendations
    
    def generate_threat_report(self, analyses: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive threat intelligence report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files_analyzed': len(analyses),
                'total_threats_detected': sum(len(a['threats_detected']) for a in analyses),
                'critical_threats': sum(1 for a in analyses for t in a['threats_detected'] if t['severity'] >= 9.0),
                'high_threats': sum(1 for a in analyses for t in a['threats_detected'] if 7.0 <= t['severity'] < 9.0),
                'medium_threats': sum(1 for a in analyses for t in a['threats_detected'] if 4.0 <= t['severity'] < 7.0),
                'low_threats': sum(1 for a in analyses for t in a['threats_detected'] if t['severity'] < 4.0),
                'average_risk_score': np.mean([a['risk_score'] for a in analyses]) if analyses else 0.0
            },
            'threat_distribution': {},
            'top_threats': [],
            'recommendations': [],
            'detailed_analysis': analyses
        }
        
        # Aggregate threat distribution
        threat_types = {}
        for analysis in analyses:
            for threat in analysis['threats_detected']:
                threat_type = threat['threat_type']
                if threat_type not in threat_types:
                    threat_types[threat_type] = {
                        'count': 0,
                        'max_severity': 0,
                        'files_affected': set()
                    }
                threat_types[threat_type]['count'] += 1
                threat_types[threat_type]['max_severity'] = max(
                    threat_types[threat_type]['max_severity'],
                    threat['severity']
                )
                threat_types[threat_type]['files_affected'].add(analysis['file_path'])
        
        # Convert sets to counts and sort
        for threat_type in threat_types:
            threat_types[threat_type]['files_affected'] = len(threat_types[threat_type]['files_affected'])
        
        report['threat_distribution'] = dict(sorted(
            threat_types.items(),
            key=lambda x: x[1]['count'],
            reverse=True
        ))
        
        # Get top threats
        all_threats = []
        for analysis in analyses:
            for threat in analysis['threats_detected']:
                all_threats.append(threat)
        
        # Sort by severity and confidence
        all_threats.sort(key=lambda x: (x['severity'], x['confidence']), reverse=True)
        report['top_threats'] = all_threats[:10]
        
        # Generate overall recommendations
        if report['summary']['critical_threats'] > 0:
            report['recommendations'].append('IMMEDIATE ACTION REQUIRED: Address all critical threats.')
        if report['summary']['high_threats'] > 5:
            report['recommendations'].append('HIGH PRIORITY: Multiple high-severity threats detected.')
        if report['summary']['average_risk_score'] > 7.0:
            report['recommendations'].append('CONCERN: Overall risk level is high. Comprehensive security review needed.')
        
        return report
