import torch
import torch.nn as nn
import numpy as np
import pandas as pd
from typing import List, Dict, Any, Optional
from transformers import AutoTokenizer, AutoModel
import re
import json
from datetime import datetime

class SecurityVulnerabilityAnalyzer:
    """AI-powered security vulnerability analyzer using PyTorch"""
    
    def __init__(self, model_name: str = "microsoft/codebert-base"):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModel.from_pretrained(model_name).to(self.device)
        self.model.eval()
        
        # Vulnerability patterns
        self.vulnerability_patterns = {
            'sql_injection': [
                r'(SELECT|INSERT|UPDATE|DELETE).*FROM.*WHERE',
                r'UNION.*SELECT',
                r'DROP.*TABLE',
                r'EXEC.*sp_',
                r'\'.*OR.*\'.*=.*\'',
            ],
            'xss': [
                r'<script[^>]*>.*?</script>',
                r'javascript:',
                r'on\w+\s*=\s*["\'][^"\']*["\']',
                r'<iframe[^>]*>.*?</iframe>',
                r'eval\s*\(',
            ],
            'path_traversal': [
                r'\.\./.*',
                r'\.\.\\.*',
                r'%2e%2e%2f',
                r'%2e%2e\\',
                r'/etc/passwd',
                r'/etc/shadow',
            ],
            'command_injection': [
                r';.*rm',
                r';.*cat',
                r';.*ls',
                r'\|.*nc',
                r'`.*`',
                r'\$\([^)]*\)',
            ],
            'insecure_deserialization': [
                r'O:\d+:"',
                r'a:\d+:{',
                r'b:\d+;',
                r'__wake_up',
                r'php://input',
            ],
            'hardcoded_credentials': [
                r'password\s*=\s*["\'][^"\']+["\']',
                r'api_key\s*=\s*["\'][^"\']+["\']',
                r'secret\s*=\s*["\'][^"\']+["\']',
                r'token\s*=\s*["\'][^"\']+["\']',
            ],
            'weak_crypto': [
                r'md5\s*\(',
                r'sha1\s*\(',
                r'base64_encode',
                r'crypt\s*\(',
                r'des_encrypt',
            ]
        }
        
        # Severity weights
        self.severity_weights = {
            'sql_injection': 9.0,
            'xss': 8.0,
            'path_traversal': 7.0,
            'command_injection': 9.5,
            'insecure_deserialization': 8.5,
            'hardcoded_credentials': 6.0,
            'weak_crypto': 5.0,
        }
        
    def analyze_code(self, code: str, file_path: str = "") -> Dict[str, Any]:
        """Analyze code for security vulnerabilities"""
        results = {
            'file_path': file_path,
            'timestamp': datetime.now().isoformat(),
            'vulnerabilities': [],
            'risk_score': 0.0,
            'summary': {
                'total_vulnerabilities': 0,
                'critical_count': 0,
                'high_count': 0,
                'medium_count': 0,
                'low_count': 0,
            }
        }
        
        # Pattern-based detection
        pattern_results = self._detect_patterns(code, file_path)
        
        # AI-based semantic analysis
        semantic_results = self._semantic_analysis(code, file_path)
        
        # Combine results
        all_vulnerabilities = pattern_results + semantic_results
        
        # Calculate risk score
        total_risk = sum(v['severity_score'] for v in all_vulnerabilities)
        results['risk_score'] = min(total_risk / 10.0, 10.0)  # Normalize to 0-10
        
        # Categorize vulnerabilities
        for vuln in all_vulnerabilities:
            results['vulnerabilities'].append(vuln)
            severity = vuln['severity']
            if severity >= 9.0:
                results['summary']['critical_count'] += 1
            elif severity >= 7.0:
                results['summary']['high_count'] += 1
            elif severity >= 4.0:
                results['summary']['medium_count'] += 1
            else:
                results['summary']['low_count'] += 1
        
        results['summary']['total_vulnerabilities'] = len(all_vulnerabilities)
        
        return results
    
    def _detect_patterns(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        """Detect vulnerabilities using regex patterns"""
        vulnerabilities = []
        lines = code.split('\n')
        
        for vuln_type, patterns in self.vulnerability_patterns.items():
            for pattern in patterns:
                for line_num, line in enumerate(lines, 1):
                    matches = re.finditer(pattern, line, re.IGNORECASE)
                    for match in matches:
                        vulnerability = {
                            'type': vuln_type,
                            'severity': self.severity_weights.get(vuln_type, 5.0),
                            'severity_score': self.severity_weights.get(vuln_type, 5.0),
                            'line_number': line_num,
                            'column': match.start() + 1,
                            'code_snippet': line.strip(),
                            'matched_pattern': pattern,
                            'description': self._get_vulnerability_description(vuln_type),
                            'recommendation': self._get_vulnerability_recommendation(vuln_type),
                            'detection_method': 'pattern-based'
                        }
                        vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    def _semantic_analysis(self, code: str, file_path: str) -> List[Dict[str, Any]]:
        """Perform semantic analysis using transformer model"""
        vulnerabilities = []
        
        try:
            # Split code into chunks for analysis
            chunks = self._chunk_code(code, max_length=512)
            
            for chunk_idx, chunk in enumerate(chunks):
                # Tokenize and get embeddings
                inputs = self.tokenizer(
                    chunk,
                    return_tensors="pt",
                    truncation=True,
                    padding=True,
                    max_length=512
                ).to(self.device)
                
                with torch.no_grad():
                    outputs = self.model(**inputs)
                    embeddings = outputs.last_hidden_state
                
                # Analyze embeddings for potential vulnerabilities
                vuln_predictions = self._analyze_embeddings(embeddings, chunk)
                
                for pred in vuln_predictions:
                    vulnerability = {
                        'type': pred['type'],
                        'severity': pred['severity'],
                        'severity_score': pred['severity'],
                        'line_number': pred.get('line_number', 0),
                        'column': 0,
                        'code_snippet': pred.get('code_snippet', chunk[:100] + '...'),
                        'matched_pattern': 'semantic-detection',
                        'description': pred['description'],
                        'recommendation': pred['recommendation'],
                        'detection_method': 'ai-based',
                        'confidence': pred.get('confidence', 0.5)
                    }
                    vulnerabilities.append(vulnerability)
        
        except Exception as e:
            # Fallback to basic analysis if AI fails
            pass
        
        return vulnerabilities
    
    def _chunk_code(self, code: str, max_length: int = 512) -> List[str]:
        """Split code into manageable chunks"""
        lines = code.split('\n')
        chunks = []
        current_chunk = []
        current_length = 0
        
        for line in lines:
            line_length = len(self.tokenizer.encode(line))
            if current_length + line_length > max_length and current_chunk:
                chunks.append('\n'.join(current_chunk))
                current_chunk = [line]
                current_length = line_length
            else:
                current_chunk.append(line)
                current_length += line_length
        
        if current_chunk:
            chunks.append('\n'.join(current_chunk))
        
        return chunks
    
    def _analyze_embeddings(self, embeddings: torch.Tensor, code_chunk: str) -> List[Dict[str, Any]]:
        """Analyze embeddings for security vulnerabilities"""
        vulnerabilities = []
        
        # Simple heuristic-based analysis on embeddings
        # In a real implementation, this would use a trained classifier
        mean_embedding = embeddings.mean(dim=1).squeeze()
        
        # Check for suspicious patterns in the embedding space
        suspicious_keywords = ['password', 'secret', 'key', 'token', 'auth', 'login']
        code_lower = code_chunk.lower()
        
        for keyword in suspicious_keywords:
            if keyword in code_lower:
                # Simple vulnerability detection based on keyword presence
                vulnerability = {
                    'type': 'potential_credential_leak',
                    'severity': 6.0,
                    'description': f'Potential credential exposure detected near "{keyword}"',
                    'recommendation': 'Review and secure any credential handling',
                    'code_snippet': code_chunk[:200] + '...' if len(code_chunk) > 200 else code_chunk,
                    'confidence': 0.7
                }
                vulnerabilities.append(vulnerability)
        
        return vulnerabilities
    
    def _get_vulnerability_description(self, vuln_type: str) -> str:
        """Get description for vulnerability type"""
        descriptions = {
            'sql_injection': 'SQL Injection vulnerability detected. Allows attackers to execute arbitrary SQL queries.',
            'xss': 'Cross-Site Scripting vulnerability detected. Allows injection of malicious scripts.',
            'path_traversal': 'Path Traversal vulnerability detected. Allows access to files outside intended directory.',
            'command_injection': 'Command Injection vulnerability detected. Allows execution of system commands.',
            'insecure_deserialization': 'Insecure Deserialization vulnerability detected. Can lead to remote code execution.',
            'hardcoded_credentials': 'Hardcoded credentials detected. Credentials should not be stored in source code.',
            'weak_crypto': 'Weak cryptographic implementation detected. Uses outdated or insecure algorithms.',
        }
        return descriptions.get(vuln_type, 'Security vulnerability detected.')
    
    def _get_vulnerability_recommendation(self, vuln_type: str) -> str:
        """Get recommendation for vulnerability type"""
        recommendations = {
            'sql_injection': 'Use parameterized queries or prepared statements. Validate and sanitize all user inputs.',
            'xss': 'Implement proper output encoding and Content Security Policy. Validate and sanitize user inputs.',
            'path_traversal': 'Validate file paths and use whitelist of allowed directories. Avoid user-controlled file paths.',
            'command_injection': 'Avoid executing system commands with user input. Use safe alternatives when possible.',
            'insecure_deserialization': 'Use safe serialization formats. Validate and integrity-check serialized data.',
            'hardcoded_credentials': 'Store credentials in environment variables or secure configuration management.',
            'weak_crypto': 'Use modern cryptographic algorithms with proper key management. Avoid deprecated functions.',
        }
        return recommendations.get(vuln_type, 'Review and fix the security issue.')
    
    def generate_report(self, analysis_results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate comprehensive security report"""
        report = {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_files_analyzed': len(analysis_results),
                'total_vulnerabilities': sum(r['summary']['total_vulnerabilities'] for r in analysis_results),
                'critical_vulnerabilities': sum(r['summary']['critical_count'] for r in analysis_results),
                'high_vulnerabilities': sum(r['summary']['high_count'] for r in analysis_results),
                'medium_vulnerabilities': sum(r['summary']['medium_count'] for r in analysis_results),
                'low_vulnerabilities': sum(r['summary']['low_count'] for r in analysis_results),
                'average_risk_score': np.mean([r['risk_score'] for r in analysis_results]) if analysis_results else 0.0,
            },
            'vulnerability_types': {},
            'file_analysis': analysis_results,
            'recommendations': []
        }
        
        # Aggregate vulnerability types
        for result in analysis_results:
            for vuln in result['vulnerabilities']:
                vuln_type = vuln['type']
                if vuln_type not in report['vulnerability_types']:
                    report['vulnerability_types'][vuln_type] = {
                        'count': 0,
                        'max_severity': 0,
                        'files_affected': set()
                    }
                report['vulnerability_types'][vuln_type]['count'] += 1
                report['vulnerability_types'][vuln_type]['max_severity'] = max(
                    report['vulnerability_types'][vuln_type]['max_severity'],
                    vuln['severity']
                )
                report['vulnerability_types'][vuln_type]['files_affected'].add(result['file_path'])
        
        # Convert sets to counts
        for vuln_type in report['vulnerability_types']:
            report['vulnerability_types'][vuln_type]['files_affected'] = len(
                report['vulnerability_types'][vuln_type]['files_affected']
            )
        
        # Generate recommendations based on findings
        if report['summary']['critical_vulnerabilities'] > 0:
            report['recommendations'].append('IMMEDIATE ACTION REQUIRED: Fix all critical vulnerabilities.')
        if report['summary']['high_vulnerabilities'] > 5:
            report['recommendations'].append('High number of high-severity vulnerabilities. Prioritize remediation.')
        if report['summary']['average_risk_score'] > 7.0:
            report['recommendations'].append('Overall risk score is high. Implement comprehensive security review.')
        
        return report
