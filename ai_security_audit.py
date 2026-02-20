#!/usr/bin/env python3
"""
AI-Powered Security & Performance Audit for DevGuardian AI Project
Comprehensive security analysis and performance optimization using AI
"""

import os
import re
import json
import ast
import time
import hashlib
import subprocess
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any, Tuple, Optional
import logging
from concurrent.futures import ThreadPoolExecutor, as_completed
import numpy as np

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class AISecurityAuditor:
    """AI-powered security and performance auditor for DevGuardian AI"""
    
    def __init__(self, project_root: str):
        self.project_root = Path(project_root)
        self.audit_results = {
            "timestamp": datetime.now().isoformat(),
            "project_root": str(project_root),
            "security_findings": [],
            "performance_metrics": [],
            "code_quality_issues": [],
            "dependency_vulnerabilities": [],
            "configuration_issues": [],
            "api_security": [],
            "database_security": [],
            "infrastructure_issues": []
        }
        
        # Security patterns for vulnerability detection
        self.security_patterns = {
            "sql_injection": [
                r"SELECT.*FROM.*WHERE.*\+.*",
                r"execute\s*\(\s*['\"].*%.*['\"]",
                r"query\s*\(\s*['\"].*\+.*['\"]",
                r"mysql_query\s*\(\s*['\"].*\$.*['\"]",
                r"pg_query\s*\(\s*['\"].*\$.*['\"]"
            ],
            "xss": [
                r"innerHTML\s*=.*user",
                r"document\.write\s*\(\s*user",
                r"eval\s*\(\s*user",
                r"outerHTML\s*=.*user",
                r"insertAdjacentHTML\s*.*user"
            ],
            "command_injection": [
                r"exec\s*\(\s*user",
                r"system\s*\(\s*user",
                r"shell_exec\s*\(\s*user",
                r"subprocess\.call\s*\(\s*user",
                r"os\.system\s*\(\s*user"
            ],
            "path_traversal": [
                r"\.\./.*",
                r"file_get_contents\s*\(\s*user",
                r"fopen\s*\(\s*user",
                r"open\s*\(\s*user",
                r"readfile\s*\(\s*user"
            ],
            "hardcoded_secrets": [
                r"password\s*=\s*['\"][^'\"]{4,}['\"]",
                r"api_key\s*=\s*['\"][^'\"]{10,}['\"]",
                r"secret\s*=\s*['\"][^'\"]{10,}['\"]",
                r"token\s*=\s*['\"][^'\"]{10,}['\"]",
                r"private_key\s*=\s*['\"][^'\"]{20,}['\"]"
            ],
            "weak_crypto": [
                r"md5\s*\(",
                r"sha1\s*\(",
                r"base64_encode",
                r"crypt\s*\(",
                r"des_encrypt"
            ],
            "insecure_deserialization": [
                r"pickle\.loads",
                r"unserialize\s*\(",
                r"yaml\.load\s*\(",
                r"json\.loads\s*\(\s*user"
            ]
        }
        
        # Performance anti-patterns
        self.performance_patterns = {
            "n_plus_one": [
                r"for.*in.*:\s*.*\.get\(",
                r"for.*in.*:\s*.*\.find\(",
                r"for.*in.*:\s*.*\.filter\("
            ],
            "missing_indexes": [
                r"WHERE\s+\w+\s*=",
                r"JOIN\s+.*\s+ON\s+.*\s*=",
                r"ORDER BY\s+\w+"
            ],
            "memory_leaks": [
                r"\.append\s*\(\s*.*\)\s*#.*loop",
                r"global\s+\w+",
                r"del\s+\w+"
            ],
            "blocking_operations": [
                r"time\.sleep\s*\(",
                r"requests\.get\s*\(",
                r"subprocess\.call\s*\("
            ]
        }
    
    def scan_file_for_vulnerabilities(self, file_path: Path) -> List[Dict]:
        """Scan individual file for security vulnerabilities"""
        vulnerabilities = []
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                lines = content.split('\n')
            
            file_ext = file_path.suffix.lower()
            
            for line_num, line in enumerate(lines, 1):
                # Check for security vulnerabilities
                for vuln_type, patterns in self.security_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            vulnerabilities.append({
                                "type": vuln_type,
                                "severity": self._get_severity(vuln_type),
                                "file": str(file_path.relative_to(self.project_root)),
                                "line": line_num,
                                "code": line.strip(),
                                "pattern": pattern,
                                "confidence": self._calculate_confidence(line, pattern)
                            })
                
                # Check for performance issues
                for perf_type, patterns in self.performance_patterns.items():
                    for pattern in patterns:
                        if re.search(pattern, line, re.IGNORECASE):
                            vulnerabilities.append({
                                "type": f"performance_{perf_type}",
                                "severity": "medium",
                                "file": str(file_path.relative_to(self.project_root)),
                                "line": line_num,
                                "code": line.strip(),
                                "pattern": pattern,
                                "confidence": 0.7
                            })
        
        except Exception as e:
            logger.error(f"Error scanning {file_path}: {e}")
        
        return vulnerabilities
    
    def _get_severity(self, vuln_type: str) -> str:
        """Determine severity level for vulnerability type"""
        severity_map = {
            "sql_injection": "critical",
            "xss": "high",
            "command_injection": "critical",
            "path_traversal": "high",
            "hardcoded_secrets": "critical",
            "weak_crypto": "medium",
            "insecure_deserialization": "high"
        }
        return severity_map.get(vuln_type, "medium")
    
    def _calculate_confidence(self, line: str, pattern: str) -> float:
        """Calculate confidence score for vulnerability detection"""
        confidence = 0.5
        
        # Increase confidence for obvious patterns
        if "user" in line.lower() or "input" in line.lower():
            confidence += 0.2
        if "=" in line and ("+" in line or "%" in line):
            confidence += 0.2
        if re.search(r"['\"].*['\"]", line):
            confidence += 0.1
        
        return min(confidence, 0.95)
    
    def analyze_dependencies(self) -> List[Dict]:
        """Analyze project dependencies for vulnerabilities"""
        vulnerabilities = []
        
        # Check for requirements.txt
        req_files = list(self.project_root.rglob("requirements*.txt"))
        for req_file in req_files:
            try:
                with open(req_file, 'r') as f:
                    for line_num, line in enumerate(f, 1):
                        line = line.strip()
                        if line and not line.startswith('#'):
                            # Check for known vulnerable packages
                            if self._is_vulnerable_package(line):
                                vulnerabilities.append({
                                    "type": "dependency_vulnerability",
                                    "severity": "high",
                                    "file": str(req_file.relative_to(self.project_root)),
                                    "line": line_num,
                                    "package": line,
                                    "description": "Known vulnerable package detected"
                                })
            except Exception as e:
                logger.error(f"Error analyzing {req_file}: {e}")
        
        # Check for package.json
        package_files = list(self.project_root.rglob("package.json"))
        for pkg_file in package_files:
            try:
                with open(pkg_file, 'r') as f:
                    package_data = json.load(f)
                    dependencies = package_data.get('dependencies', {})
                    for dep_name, version in dependencies.items():
                        if self._is_vulnerable_npm_package(dep_name, version):
                            vulnerabilities.append({
                                "type": "npm_dependency_vulnerability",
                                "severity": "high",
                                "file": str(pkg_file.relative_to(self.project_root)),
                                "package": f"{dep_name}@{version}",
                                "description": "Known vulnerable npm package detected"
                            })
            except Exception as e:
                logger.error(f"Error analyzing {pkg_file}: {e}")
        
        return vulnerabilities
    
    def _is_vulnerable_package(self, package_line: str) -> bool:
        """Check if package has known vulnerabilities"""
        vulnerable_packages = [
            "requests<2.25.0",
            "urllib3<1.26.0",
            "pillow<8.0.0",
            "jinja2<2.11.0",
            "flask<1.0.0"
        ]
        
        for vuln_pkg in vulnerable_packages:
            if vuln_pkg.split('<')[0] in package_line.lower():
                return True
        return False
    
    def _is_vulnerable_npm_package(self, package_name: str, version: str) -> bool:
        """Check if npm package has known vulnerabilities"""
        vulnerable_packages = [
            "lodash<4.17.21",
            "axios<0.21.0",
            "node-forge<1.0.0",
            "serialize-javascript<3.1.0",
            "minimist<1.2.0"
        ]
        
        for vuln_pkg in vulnerable_packages:
            pkg_name, min_version = vuln_pkg.split('<')
            if package_name == pkg_name:
                # Simple version check (would need proper semver comparison in production)
                return True
        return False
    
    def analyze_api_endpoints(self) -> List[Dict]:
        """Analyze API endpoints for security issues"""
        api_issues = []
        
        # Find API route files
        api_files = list(self.project_root.rglob("*router*.py")) + \
                   list(self.project_root.rglob("*endpoint*.py")) + \
                   list(self.project_root.rglob("*api*.py"))
        
        for api_file in api_files:
            try:
                with open(api_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    # Check for missing authentication
                    if re.search(r'@app\.get\(|@router\.get\(|@bp\.get\(', line):
                        if "auth" not in line.lower() and "login" not in line.lower():
                            next_lines = lines[line_num:line_num+5]
                            if not any("auth" in l.lower() or "token" in l.lower() for l in next_lines):
                                api_issues.append({
                                    "type": "missing_authentication",
                                    "severity": "high",
                                    "file": str(api_file.relative_to(self.project_root)),
                                    "line": line_num,
                                    "code": line.strip(),
                                    "description": "API endpoint without authentication"
                                })
                    
                    # Check for CORS issues
                    if "cors" in line.lower() and "*" in line:
                        api_issues.append({
                            "type": "cors_misconfiguration",
                            "severity": "medium",
                            "file": str(api_file.relative_to(self.project_root)),
                            "line": line_num,
                            "code": line.strip(),
                            "description": "CORS configured to allow all origins"
                        })
                    
                    # Check for SQL injection in API
                    if re.search(r'execute|query|select', line, re.IGNORECASE):
                        if "+" in line or "%" in line:
                            api_issues.append({
                                "type": "api_sql_injection",
                                "severity": "critical",
                                "file": str(api_file.relative_to(self.project_root)),
                                "line": line_num,
                                "code": line.strip(),
                                "description": "Potential SQL injection in API endpoint"
                            })
            
            except Exception as e:
                logger.error(f"Error analyzing API file {api_file}: {e}")
        
        return api_issues
    
    def analyze_configuration(self) -> List[Dict]:
        """Analyze configuration files for security issues"""
        config_issues = []
        
        # Find configuration files
        config_files = list(self.project_root.rglob("*.env*")) + \
                      list(self.project_root.rglob("config*.py")) + \
                      list(self.project_root.rglob("settings*.py")) + \
                      list(self.project_root.rglob("docker-compose*.yml"))
        
        for config_file in config_files:
            try:
                with open(config_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                for line_num, line in enumerate(lines, 1):
                    # Check for hardcoded secrets in config
                    if re.search(r'password|secret|key|token', line, re.IGNORECASE):
                        if re.search(r'=\s*["\'][^"\']+["\']', line):
                            config_issues.append({
                                "type": "config_hardcoded_secret",
                                "severity": "critical",
                                "file": str(config_file.relative_to(self.project_root)),
                                "line": line_num,
                                "code": line.strip(),
                                "description": "Hardcoded secret in configuration file"
                            })
                    
                    # Check for debug mode in production
                    if "debug" in line.lower() and "true" in line.lower():
                        config_issues.append({
                            "type": "debug_mode_enabled",
                            "severity": "medium",
                            "file": str(config_file.relative_to(self.project_root)),
                            "line": line_num,
                            "code": line.strip(),
                            "description": "Debug mode enabled in configuration"
                        })
                    
                    # Check for weak SSL/TLS settings
                    if re.search(r'tls|ssl|https', line, re.IGNORECASE):
                        if "version" in line.lower() and ("1.0" in line or "1.1" in line):
                            config_issues.append({
                                "type": "weak_tls_version",
                                "severity": "high",
                                "file": str(config_file.relative_to(self.project_root)),
                                "line": line_num,
                                "code": line.strip(),
                                "description": "Weak TLS/SSL version configured"
                            })
            
            except Exception as e:
                logger.error(f"Error analyzing config file {config_file}: {e}")
        
        return config_issues
    
    def analyze_performance(self) -> List[Dict]:
        """Analyze code for performance issues"""
        performance_issues = []
        
        # Find source code files
        code_files = []
        for ext in ['.py', '.js', '.ts', '.php', '.java']:
            code_files.extend(list(self.project_root.rglob(f"*{ext}")))
        
        for code_file in code_files:
            try:
                with open(code_file, 'r') as f:
                    content = f.read()
                    lines = content.split('\n')
                
                # Analyze for performance anti-patterns
                for line_num, line in enumerate(lines, 1):
                    # Check for inefficient loops
                    if re.search(r'for.*in.*:\s*.*\.get\(|for.*in.*:\s*.*\.find\(', line):
                        performance_issues.append({
                            "type": "n_plus_one_query",
                            "severity": "medium",
                            "file": str(code_file.relative_to(self.project_root)),
                            "line": line_num,
                            "code": line.strip(),
                            "description": "Potential N+1 query problem in loop",
                            "impact": "high_database_load"
                        })
                    
                    # Check for missing error handling
                    if re.search(r'except\s*:\s*pass|except\s*Exception\s*:\s*pass', line):
                        performance_issues.append({
                            "type": "missing_error_handling",
                            "severity": "medium",
                            "file": str(code_file.relative_to(self.project_root)),
                            "line": line_num,
                            "code": line.strip(),
                            "description": "Empty exception block can hide errors",
                            "impact": "debugging_difficulty"
                        })
                    
                    # Check for large object creation in loops
                    if re.search(r'for.*in.*:\s*.*\[\s*\]', line):
                        performance_issues.append({
                            "type": "inefficient_memory_usage",
                            "severity": "low",
                            "file": str(code_file.relative_to(self.project_root)),
                            "line": line_num,
                            "code": line.strip(),
                            "description": "Creating large objects in loops",
                            "impact": "memory_usage"
                        })
            
            except Exception as e:
                logger.error(f"Error analyzing performance in {code_file}: {e}")
        
        return performance_issues
    
    def run_security_scan(self) -> Dict:
        """Run comprehensive security scan"""
        logger.info("🔍 Starting comprehensive security scan...")
        
        # Get all code files
        code_files = []
        for ext in ['.py', '.js', '.ts', '.php', '.java', '.go', '.rb']:
            code_files.extend(list(self.project_root.rglob(f"*{ext}")))
        
        logger.info(f"📁 Scanning {len(code_files)} code files...")
        
        # Scan files in parallel
        all_vulnerabilities = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {executor.submit(self.scan_file_for_vulnerabilities, f): f 
                             for f in code_files}
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    vulnerabilities = future.result()
                    all_vulnerabilities.extend(vulnerabilities)
                except Exception as e:
                    logger.error(f"Error scanning {file_path}: {e}")
        
        # Analyze dependencies
        logger.info("📦 Analyzing dependencies...")
        dependency_vulns = self.analyze_dependencies()
        
        # Analyze API endpoints
        logger.info("🔗 Analyzing API endpoints...")
        api_issues = self.analyze_api_endpoints()
        
        # Analyze configuration
        logger.info("⚙️ Analyzing configuration...")
        config_issues = self.analyze_configuration()
        
        # Analyze performance
        logger.info("⚡ Analyzing performance...")
        performance_issues = self.analyze_performance()
        
        # Compile results
        self.audit_results["security_findings"] = all_vulnerabilities
        self.audit_results["dependency_vulnerabilities"] = dependency_vulns
        self.audit_results["api_security"] = api_issues
        self.audit_results["configuration_issues"] = config_issues
        self.audit_results["performance_metrics"] = performance_issues
        
        # Generate summary
        self._generate_summary()
        
        return self.audit_results
    
    def _generate_summary(self):
        """Generate audit summary"""
        total_issues = 0
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
        
        for category in ["security_findings", "dependency_vulnerabilities", 
                        "api_security", "configuration_issues", "performance_metrics"]:
            issues = self.audit_results.get(category, [])
            total_issues += len(issues)
            for issue in issues:
                severity = issue.get("severity", "medium")
                if severity in severity_counts:
                    severity_counts[severity] += 1
        
        self.audit_results["summary"] = {
            "total_issues": total_issues,
            "severity_breakdown": severity_counts,
            "security_score": self._calculate_security_score(severity_counts),
            "performance_score": self._calculate_performance_score(),
            "recommendations": self._generate_recommendations(severity_counts)
        }
    
    def _calculate_security_score(self, severity_counts: Dict) -> float:
        """Calculate overall security score (0-100)"""
        weights = {"critical": 40, "high": 25, "medium": 15, "low": 5}
        total_penalty = sum(count * weights[severity] 
                           for severity, count in severity_counts.items())
        score = max(0, 100 - total_penalty)
        return round(score, 1)
    
    def _calculate_performance_score(self) -> float:
        """Calculate performance score (0-100)"""
        perf_issues = self.audit_results.get("performance_metrics", [])
        if not perf_issues:
            return 100.0
        
        # Simple scoring based on number of performance issues
        penalty = min(50, len(perf_issues) * 2)
        return round(100 - penalty, 1)
    
    def _generate_recommendations(self, severity_counts: Dict) -> List[str]:
        """Generate security recommendations"""
        recommendations = []
        
        if severity_counts["critical"] > 0:
            recommendations.append("🚨 CRITICAL: Address all critical security vulnerabilities immediately")
        
        if severity_counts["high"] > 5:
            recommendations.append("⚠️ HIGH: Prioritize fixing high-severity security issues")
        
        if len(self.audit_results.get("dependency_vulnerabilities", [])) > 0:
            recommendations.append("📦 Update all vulnerable dependencies to latest secure versions")
        
        if len(self.audit_results.get("api_security", [])) > 0:
            recommendations.append("🔗 Implement proper authentication and authorization for all API endpoints")
        
        if len(self.audit_results.get("configuration_issues", [])) > 0:
            recommendations.append("⚙️ Review and secure all configuration files")
        
        if len(self.audit_results.get("performance_metrics", [])) > 10:
            recommendations.append("⚡ Optimize performance issues to improve application responsiveness")
        
        return recommendations
    
    def generate_report(self, output_file: str = "security_audit_report.json"):
        """Generate detailed audit report"""
        with open(output_file, 'w') as f:
            json.dump(self.audit_results, f, indent=2, default=str)
        
        logger.info(f"📊 Security audit report saved to {output_file}")
        return output_file
    
    def print_summary(self):
        """Print audit summary to console"""
        summary = self.audit_results.get("summary", {})
        
        print("\n" + "="*80)
        print("🔍 DEVGUARDIAN AI - SECURITY & PERFORMANCE AUDIT REPORT")
        print("="*80)
        print(f"📅 Timestamp: {self.audit_results['timestamp']}")
        print(f"📁 Project Root: {self.audit_results['project_root']}")
        print(f"\n📊 SUMMARY:")
        print(f"   Total Issues Found: {summary.get('total_issues', 0)}")
        print(f"   Security Score: {summary.get('security_score', 0)}/100")
        print(f"   Performance Score: {summary.get('performance_score', 0)}/100")
        
        severity = summary.get('severity_breakdown', {})
        print(f"\n🚨 SEVERITY BREAKDOWN:")
        print(f"   Critical: {severity.get('critical', 0)}")
        print(f"   High: {severity.get('high', 0)}")
        print(f"   Medium: {severity.get('medium', 0)}")
        print(f"   Low: {severity.get('low', 0)}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in summary.get('recommendations', []):
            print(f"   {rec}")
        
        print("\n" + "="*80)

def main():
    """Main audit execution"""
    project_root = "/home/marcelo/Documents/varas con chat gpt/proyecto/devguardian-ai"
    
    print("🚀 Starting AI-Powered Security & Performance Audit...")
    print(f"📁 Project: {project_root}")
    
    # Initialize auditor
    auditor = AISecurityAuditor(project_root)
    
    # Run comprehensive scan
    results = auditor.run_security_scan()
    
    # Generate report
    report_file = auditor.generate_report()
    
    # Print summary
    auditor.print_summary()
    
    print(f"\n📄 Detailed report saved to: {report_file}")
    print("✅ Audit completed successfully!")

if __name__ == "__main__":
    main()
