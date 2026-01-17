#!/usr/bin/env python3
"""
Automated Repository Security Analyzer
Comprehensive repository analysis using PyTorch vulnerability scanner
"""

import os
import sys
import json
import time
import asyncio
import subprocess
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import hashlib
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('repository_analyzer.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class RepositoryAnalysis:
    """Repository analysis results"""
    repository_url: str
    repository_name: str
    clone_path: str
    analysis_date: str
    total_files: int
    scanned_files: int
    total_vulnerabilities: int
    severity_breakdown: Dict[str, int]
    type_breakdown: Dict[str, int]
    risk_score: float
    scan_duration: float
    vulnerabilities: List[Dict[str, Any]]
    recommendations: List[str]
    status: str  # 'success', 'failed', 'partial'
    error_message: Optional[str] = None
    commit_hash: Optional[str] = None
    branch: Optional[str] = None

@dataclass
class TestSuite:
    """Automated test suite configuration"""
    name: str
    description: str
    repositories: List[str]
    scan_depth: str
    enable_ml_detection: bool
    enable_pattern_detection: bool
    parallel_processing: bool
    max_workers: int
    output_format: str  # 'json', 'html', 'csv'

class AutomatedRepositoryAnalyzer:
    """Automated repository security analyzer"""
    
    def __init__(self, workspace_dir: str = "./analysis_workspace"):
        self.workspace_dir = Path(workspace_dir)
        self.workspace_dir.mkdir(exist_ok=True)
        
        # Initialize scanner (simplified version for demo)
        self.scanner = self._initialize_scanner()
        
        # Analysis statistics
        self.analysis_stats = {
            'total_repositories': 0,
            'successful_analyses': 0,
            'failed_analyses': 0,
            'total_vulnerabilities': 0,
            'total_scan_time': 0.0,
            'start_time': None,
            'end_time': None
        }
        
        # Supported file extensions
        self.supported_extensions = {
            '.php', '.js', '.jsx', '.ts', '.tsx', '.py', '.rb', '.pl', 
            '.sh', '.bat', '.java', '.cpp', '.c', '.h', '.hpp', '.go', 
            '.rs', '.swift', '.kt', '.scala', '.cs', '.vb', '.php3', 
            '.php4', '.php5', '.phtml', '.jsp', '.asp', '.aspx'
        }
        
    def _initialize_scanner(self):
        """Initialize the vulnerability scanner"""
        try:
            # Try to import the PyTorch scanner
            sys.path.append(os.path.join(os.path.dirname(__file__), 'ai-service'))
            from app.core.services.pytorch_vulnerability_scanner import PyTorchVulnerabilityScanner
            return PyTorchVulnerabilityScanner()
        except ImportError:
            logger.warning("PyTorch scanner not available, using simplified scanner")
            return self._create_simplified_scanner()
    
    def _create_simplified_scanner(self):
        """Create a simplified scanner for demo purposes"""
        from pytorch_scanner_demo import SimplifiedPyTorchScanner
        return SimplifiedPyTorchScanner()
    
    def analyze_repository(self, repository_url: str, branch: str = "main", 
                          scan_depth: str = "standard") -> RepositoryAnalysis:
        """Analyze a single repository for vulnerabilities"""
        
        start_time = time.time()
        repo_name = self._extract_repo_name(repository_url)
        clone_path = self.workspace_dir / repo_name
        
        logger.info(f"Starting analysis of {repository_url}")
        
        try:
            # Clone repository
            commit_hash = self._clone_repository(repository_url, clone_path, branch)
            
            # Scan repository
            vulnerabilities = self._scan_repository(clone_path, scan_depth)
            
            # Generate analysis results
            analysis = self._generate_analysis(
                repository_url, repo_name, str(clone_path), 
                vulnerabilities, time.time() - start_time, commit_hash, branch
            )
            
            # Cleanup
            self._cleanup_repository(clone_path)
            
            logger.info(f"Analysis completed for {repo_name}: {analysis.total_vulnerabilities} vulnerabilities")
            return analysis
            
        except Exception as e:
            logger.error(f"Failed to analyze {repository_url}: {str(e)}")
            
            # Cleanup on failure
            if clone_path.exists():
                self._cleanup_repository(clone_path)
            
            return RepositoryAnalysis(
                repository_url=repository_url,
                repository_name=repo_name,
                clone_path=str(clone_path),
                analysis_date=datetime.now().isoformat(),
                total_files=0,
                scanned_files=0,
                total_vulnerabilities=0,
                severity_breakdown={},
                type_breakdown={},
                risk_score=0.0,
                scan_duration=time.time() - start_time,
                vulnerabilities=[],
                recommendations=[],
                status='failed',
                error_message=str(e),
                branch=branch
            )
    
    def _extract_repo_name(self, repository_url: str) -> str:
        """Extract repository name from URL"""
        if repository_url.endswith('.git'):
            repository_url = repository_url[:-4]
        
        return repository_url.split('/')[-1]
    
    def _clone_repository(self, repository_url: str, clone_path: Path, 
                         branch: str = "main") -> Optional[str]:
        """Clone repository and return commit hash"""
        
        # Remove existing directory if it exists
        if clone_path.exists():
            self._cleanup_repository(clone_path)
        
        # Clone repository
        try:
            result = subprocess.run(
                ["git", "clone", "--depth", "1", "-b", branch, repository_url, str(clone_path)],
                capture_output=True, text=True, timeout=300
            )
            
            if result.returncode != 0:
                raise Exception(f"Git clone failed: {result.stderr}")
            
            # Get commit hash
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=clone_path,
                capture_output=True, text=True
            )
            
            if result.returncode == 0:
                return result.stdout.strip()
            else:
                logger.warning("Could not get commit hash")
                return None
                
        except subprocess.TimeoutExpired:
            raise Exception("Git clone timed out")
        except FileNotFoundError:
            raise Exception("Git not found. Please install git.")
    
    def _scan_repository(self, repo_path: Path, scan_depth: str) -> List[Dict[str, Any]]:
        """Scan repository for vulnerabilities"""
        
        vulnerabilities = []
        scanned_files = 0
        
        # Get all files to scan
        files_to_scan = self._get_files_to_scan(repo_path)
        
        logger.info(f"Scanning {len(files_to_scan)} files in {repo_path}")
        
        # Scan files in parallel
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_file = {
                executor.submit(self._scan_file, file_path): file_path 
                for file_path in files_to_scan
            }
            
            for future in as_completed(future_to_file):
                file_path = future_to_file[future]
                try:
                    file_vulnerabilities = future.result()
                    vulnerabilities.extend(file_vulnerabilities)
                    scanned_files += 1
                    
                    if scanned_files % 10 == 0:
                        logger.info(f"Scanned {scanned_files}/{len(files_to_scan)} files")
                        
                except Exception as e:
                    logger.error(f"Failed to scan {file_path}: {str(e)}")
        
        logger.info(f"Repository scan completed: {len(vulnerabilities)} vulnerabilities found")
        return vulnerabilities
    
    def _get_files_to_scan(self, repo_path: Path) -> List[Path]:
        """Get list of files to scan"""
        files_to_scan = []
        
        # Common directories to exclude
        exclude_dirs = {
            '.git', '.svn', '.hg', '__pycache__', 'node_modules', 
            'vendor', 'bower_components', '.vscode', '.idea',
            'build', 'dist', 'target', 'bin', 'obj', 'out'
        }
        
        # Common file patterns to exclude
        exclude_patterns = {
            '*.min.js', '*.min.css', '*.bundle.js', '*.chunk.js',
            '*.map', '*.lock', '*.log', '*.tmp', '*.cache'
        }
        
        for file_path in repo_path.rglob('*'):
            # Skip directories
            if file_path.is_dir():
                if file_path.name in exclude_dirs:
                    continue
                continue
            
            # Skip excluded patterns
            if any(file_path.match(pattern) for pattern in exclude_patterns):
                continue
            
            # Check file extension
            if file_path.suffix.lower() in self.supported_extensions:
                # Skip very large files (>1MB)
                if file_path.stat().st_size > 1024 * 1024:
                    logger.warning(f"Skipping large file: {file_path}")
                    continue
                
                files_to_scan.append(file_path)
        
        return files_to_scan
    
    def _scan_file(self, file_path: Path) -> List[Dict[str, Any]]:
        """Scan a single file for vulnerabilities"""
        
        try:
            # Read file content
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Skip empty files
            if not content.strip():
                return []
            
            # Scan with scanner
            vulnerabilities = self.scanner.scan_file(str(file_path), content)
            
            # Convert to dictionary format
            return [
                {
                    'file_path': str(file_path.relative_to(file_path.parents[-2])),
                    'vulnerability_type': vuln.vulnerability_type.value,
                    'severity': vuln.severity,
                    'confidence': vuln.confidence,
                    'line_number': vuln.line_number,
                    'code_snippet': vuln.code_snippet,
                    'description': vuln.description,
                    'recommendation': vuln.recommendation,
                    'cwe_id': vuln.cwe_id,
                    'cvss_score': vuln.cvss_score
                }
                for vuln in vulnerabilities
            ]
            
        except Exception as e:
            logger.error(f"Error scanning file {file_path}: {str(e)}")
            return []
    
    def _generate_analysis(self, repository_url: str, repo_name: str, 
                          clone_path: str, vulnerabilities: List[Dict[str, Any]], 
                          scan_duration: float, commit_hash: Optional[str], 
                          branch: str) -> RepositoryAnalysis:
        """Generate repository analysis results"""
        
        # Count statistics
        total_vulnerabilities = len(vulnerabilities)
        severity_breakdown = {}
        type_breakdown = {}
        
        for vuln in vulnerabilities:
            # Count by severity
            severity = vuln['severity']
            severity_breakdown[severity] = severity_breakdown.get(severity, 0) + 1
            
            # Count by type
            vuln_type = vuln['vulnerability_type']
            type_breakdown[vuln_type] = type_breakdown.get(vuln_type, 0) + 1
        
        # Calculate risk score
        risk_score = (
            severity_breakdown.get('critical', 0) * 10 +
            severity_breakdown.get('high', 0) * 7 +
            severity_breakdown.get('medium', 0) * 4 +
            severity_breakdown.get('low', 0) * 1
        )
        
        # Generate recommendations
        recommendations = self._generate_recommendations(vulnerabilities, severity_breakdown)
        
        # Get file counts
        total_files = len(list(Path(clone_path).rglob('*'))) if Path(clone_path).exists() else 0
        scanned_files = len(set(vuln['file_path'] for vuln in vulnerabilities))
        
        return RepositoryAnalysis(
            repository_url=repository_url,
            repository_name=repo_name,
            clone_path=clone_path,
            analysis_date=datetime.now().isoformat(),
            total_files=total_files,
            scanned_files=scanned_files,
            total_vulnerabilities=total_vulnerabilities,
            severity_breakdown=severity_breakdown,
            type_breakdown=type_breakdown,
            risk_score=risk_score,
            scan_duration=scan_duration,
            vulnerabilities=vulnerabilities,
            recommendations=recommendations,
            status='success',
            commit_hash=commit_hash,
            branch=branch
        )
    
    def _generate_recommendations(self, vulnerabilities: List[Dict[str, Any]], 
                                 severity_breakdown: Dict[str, int]) -> List[str]:
        """Generate security recommendations"""
        
        recommendations = []
        
        # Critical vulnerabilities
        if severity_breakdown.get('critical', 0) > 0:
            recommendations.append(
                f"🚨 URGENT: Address {severity_breakdown['critical']} critical vulnerabilities immediately"
            )
        
        # High vulnerabilities
        if severity_breakdown.get('high', 0) > 5:
            recommendations.append(
                f"⚠️ HIGH PRIORITY: {severity_breakdown['high']} high-severity vulnerabilities require immediate attention"
            )
        
        # Type-specific recommendations
        type_counts = {}
        for vuln in vulnerabilities:
            vuln_type = vuln['vulnerability_type']
            type_counts[vuln_type] = type_counts.get(vuln_type, 0) + 1
        
        if type_counts.get('sql_injection', 0) > 3:
            recommendations.append(
                "🗄️ Implement comprehensive input validation and parameterized queries throughout the application"
            )
        
        if type_counts.get('hardcoded_credentials', 0) > 0:
            recommendations.append(
                "🔑 Remove all hardcoded credentials and implement secure credential management"
            )
        
        if type_counts.get('xss', 0) > 5:
            recommendations.append(
                "🌐 Implement comprehensive XSS protection with input sanitization and output encoding"
            )
        
        if type_counts.get('command_injection', 0) > 2:
            recommendations.append(
                "💻 Eliminate command injection vulnerabilities by avoiding system calls with user input"
            )
        
        # General recommendations
        recommendations.extend([
            "🔧 Implement regular security scanning as part of CI/CD pipeline",
            "👥 Conduct security code reviews for all new features",
            "📦 Keep all dependencies and frameworks updated to latest secure versions",
            "🔒 Enable security headers and implement secure coding practices",
            "📊 Monitor and log security events for incident response"
        ])
        
        return recommendations
    
    def _cleanup_repository(self, clone_path: Path):
        """Clean up cloned repository"""
        try:
            if clone_path.exists():
                import shutil
                shutil.rmtree(clone_path)
                logger.debug(f"Cleaned up {clone_path}")
        except Exception as e:
            logger.warning(f"Failed to cleanup {clone_path}: {str(e)}")
    
    def run_test_suite(self, test_suite: TestSuite) -> Dict[str, Any]:
        """Run automated test suite"""
        
        logger.info(f"Starting test suite: {test_suite.name}")
        self.analysis_stats['start_time'] = datetime.now().isoformat()
        
        results = []
        
        for repo_url in test_suite.repositories:
            try:
                analysis = self.analyze_repository(
                    repo_url, 
                    scan_depth=test_suite.scan_depth
                )
                results.append(analysis)
                
                # Update statistics
                self.analysis_stats['total_repositories'] += 1
                if analysis.status == 'success':
                    self.analysis_stats['successful_analyses'] += 1
                    self.analysis_stats['total_vulnerabilities'] += analysis.total_vulnerabilities
                else:
                    self.analysis_stats['failed_analyses'] += 1
                
                self.analysis_stats['total_scan_time'] += analysis.scan_duration
                
            except Exception as e:
                logger.error(f"Failed to analyze {repo_url}: {str(e)}")
                self.analysis_stats['failed_analyses'] += 1
        
        self.analysis_stats['end_time'] = datetime.now().isoformat()
        
        # Generate test suite report
        report = self._generate_test_suite_report(test_suite, results)
        
        # Save results
        self._save_test_results(test_suite, results, report)
        
        return report
    
    def _generate_test_suite_report(self, test_suite: TestSuite, 
                                   results: List[RepositoryAnalysis]) -> Dict[str, Any]:
        """Generate comprehensive test suite report"""
        
        total_vulnerabilities = sum(r.total_vulnerabilities for r in results)
        total_files = sum(r.total_files for r in results)
        total_scan_time = sum(r.scan_duration for r in results)
        
        # Aggregate statistics
        all_severity_breakdown = {}
        all_type_breakdown = {}
        
        for result in results:
            for severity, count in result.severity_breakdown.items():
                all_severity_breakdown[severity] = all_severity_breakdown.get(severity, 0) + count
            
            for vuln_type, count in result.type_breakdown.items():
                all_type_breakdown[vuln_type] = all_type_breakdown.get(vuln_type, 0) + 1
        
        # Calculate overall risk score
        overall_risk_score = sum(r.risk_score for r in results)
        
        # Find highest risk repository
        highest_risk_repo = max(results, key=lambda r: r.risk_score) if results else None
        
        # Find most common vulnerability
        most_common_vuln = max(all_type_breakdown.items(), key=lambda x: x[1])[0] if all_type_breakdown else None
        
        return {
            'test_suite': {
                'name': test_suite.name,
                'description': test_suite.description,
                'configuration': asdict(test_suite)
            },
            'summary': {
                'total_repositories': len(results),
                'successful_analyses': len([r for r in results if r.status == 'success']),
                'failed_analyses': len([r for r in results if r.status == 'failed']),
                'total_files_analyzed': total_files,
                'total_vulnerabilities': total_vulnerabilities,
                'overall_risk_score': overall_risk_score,
                'total_scan_time': total_scan_time,
                'average_scan_time': total_scan_time / len(results) if results else 0,
                'most_common_vulnerability': most_common_vuln,
                'highest_risk_repository': highest_risk_repo.repository_name if highest_risk_repo else None
            },
            'severity_breakdown': all_severity_breakdown,
            'type_breakdown': all_type_breakdown,
            'repository_results': [asdict(result) for result in results],
            'recommendations': self._generate_suite_recommendations(all_severity_breakdown, all_type_breakdown),
            'generated_at': datetime.now().isoformat()
        }
    
    def _generate_suite_recommendations(self, severity_breakdown: Dict[str, int], 
                                       type_breakdown: Dict[str, int]) -> List[str]:
        """Generate recommendations for the entire test suite"""
        
        recommendations = []
        
        # Overall risk assessment
        total_vulns = sum(severity_breakdown.values())
        critical_count = severity_breakdown.get('critical', 0)
        high_count = severity_breakdown.get('high', 0)
        
        if critical_count > 0:
            recommendations.append(
                f"🚨 CRITICAL: {critical_count} critical vulnerabilities found across repositories - immediate action required"
            )
        
        if high_count > 10:
            recommendations.append(
                f"⚠️ HIGH RISK: {high_count} high-severity vulnerabilities require urgent attention"
            )
        
        if total_vulns > 100:
            recommendations.append(
                f"📊 HIGH VOLUME: {total_vulns} total vulnerabilities indicate need for comprehensive security program"
            )
        
        # Type-specific recommendations
        if type_breakdown.get('sql_injection', 0) > 5:
            recommendations.append(
                "🗄️ SQL INJECTION: Implement organization-wide database security standards and parameterized queries"
            )
        
        if type_breakdown.get('hardcoded_credentials', 0) > 3:
            recommendations.append(
                "🔑 CREDENTIALS: Establish organization-wide secret management policies and rotate all exposed credentials"
            )
        
        if type_breakdown.get('xss', 0) > 8:
            recommendations.append(
                "🌐 XSS: Implement comprehensive web application security program with input validation and output encoding"
            )
        
        # Process recommendations
        recommendations.extend([
            "🔄 Implement automated security scanning in CI/CD pipelines",
            "📚 Provide security training for development teams",
            "🔧 Establish secure coding standards and guidelines",
            "📊 Implement security metrics and monitoring dashboards",
            "🛡️ Create incident response procedures for security events",
            "🔍 Conduct regular penetration testing and security assessments"
        ])
        
        return recommendations
    
    def _save_test_results(self, test_suite: TestSuite, 
                          results: List[RepositoryAnalysis], 
                          report: Dict[str, Any]):
        """Save test results to files"""
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("test_results")
        output_dir.mkdir(exist_ok=True)
        
        # Save JSON report
        json_file = output_dir / f"{test_suite.name}_{timestamp}.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        # Save CSV summary
        csv_file = output_dir / f"{test_suite.name}_{timestamp}_summary.csv"
        self._save_csv_summary(results, csv_file)
        
        # Save detailed vulnerabilities
        vuln_file = output_dir / f"{test_suite.name}_{timestamp}_vulnerabilities.csv"
        self._save_vulnerability_csv(results, vuln_file)
        
        logger.info(f"Test results saved to {output_dir}")
    
    def _save_csv_summary(self, results: List[RepositoryAnalysis], csv_file: Path):
        """Save CSV summary of repository analyses"""
        
        import csv
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Repository', 'Status', 'Total Files', 'Scanned Files', 
                'Total Vulnerabilities', 'Critical', 'High', 'Medium', 'Low',
                'Risk Score', 'Scan Duration (s)', 'Branch', 'Commit Hash'
            ])
            
            # Data rows
            for result in results:
                writer.writerow([
                    result.repository_name,
                    result.status,
                    result.total_files,
                    result.scanned_files,
                    result.total_vulnerabilities,
                    result.severity_breakdown.get('critical', 0),
                    result.severity_breakdown.get('high', 0),
                    result.severity_breakdown.get('medium', 0),
                    result.severity_breakdown.get('low', 0),
                    result.risk_score,
                    f"{result.scan_duration:.2f}",
                    result.branch or 'main',
                    result.commit_hash or 'N/A'
                ])
    
    def _save_vulnerability_csv(self, results: List[RepositoryAnalysis], csv_file: Path):
        """Save detailed vulnerabilities to CSV"""
        
        import csv
        
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'Repository', 'File Path', 'Vulnerability Type', 'Severity',
                'Confidence', 'Line Number', 'Code Snippet', 'Description',
                'Recommendation', 'CWE ID', 'CVSS Score'
            ])
            
            # Data rows
            for result in results:
                for vuln in result.vulnerabilities:
                    writer.writerow([
                        result.repository_name,
                        vuln['file_path'],
                        vuln['vulnerability_type'],
                        vuln['severity'],
                        f"{vuln['confidence']:.2f}",
                        vuln['line_number'],
                        vuln['code_snippet'][:100] + "..." if len(vuln['code_snippet']) > 100 else vuln['code_snippet'],
                        vuln['description'],
                        vuln['recommendation'],
                        vuln['cwe_id'] or 'N/A',
                        f"{vuln['cvss_score']:.1f}" if vuln['cvss_score'] else 'N/A'
                    ])

def create_sample_test_suite() -> TestSuite:
    """Create a sample test suite for demonstration"""
    
    return TestSuite(
        name="Security_Scan_Demo",
        description="Automated security vulnerability scanning test suite",
        repositories=[
            "https://github.com/WordPress/WordPress",
            "https://github.com/laravel/laravel",
            "https://github.com/django/django",
            "https://github.com/nodejs/node",
            "https://github.com/python/cpython"
        ],
        scan_depth="standard",
        enable_ml_detection=True,
        enable_pattern_detection=True,
        parallel_processing=True,
        max_workers=4,
        output_format="json"
    )

def main():
    """Main function to run automated repository analysis"""
    
    print("🔍 Automated Repository Security Analyzer")
    print("=" * 60)
    print("📋 This tool automatically analyzes repositories for security vulnerabilities")
    print("   using the PyTorch vulnerability scanner with comprehensive reporting.")
    print()
    
    # Create analyzer
    analyzer = AutomatedRepositoryAnalyzer()
    
    # Create test suite
    test_suite = create_sample_test_suite()
    
    print(f"🚀 Starting test suite: {test_suite.name}")
    print(f"📁 Repositories to analyze: {len(test_suite.repositories)}")
    print(f"🔧 Scan depth: {test_suite.scan_depth}")
    print(f"⚡ Parallel processing: {test_suite.parallel_processing}")
    print()
    
    # Run test suite
    try:
        report = analyzer.run_test_suite(test_suite)
        
        # Display summary
        print("📊 Test Suite Results")
        print("=" * 40)
        print(f"✅ Successful analyses: {report['summary']['successful_analyses']}")
        print(f"❌ Failed analyses: {report['summary']['failed_analyses']}")
        print(f"📁 Total files analyzed: {report['summary']['total_files_analyzed']}")
        print(f"🚨 Total vulnerabilities: {report['summary']['total_vulnerabilities']}")
        print(f"⚠️  Overall risk score: {report['summary']['overall_risk_score']}")
        print(f"⏱️  Total scan time: {report['summary']['total_scan_time']:.2f}s")
        print(f"📈 Average scan time: {report['summary']['average_scan_time']:.2f}s")
        print()
        
        # Display severity breakdown
        print("📈 Severity Breakdown:")
        for severity, count in report['severity_breakdown'].items():
            print(f"  {severity}: {count}")
        print()
        
        # Display type breakdown
        print("🏷️  Type Breakdown:")
        for vuln_type, count in report['type_breakdown'].items():
            print(f"  {vuln_type}: {count}")
        print()
        
        # Display top recommendations
        print("💡 Key Recommendations:")
        for i, rec in enumerate(report['recommendations'][:5], 1):
            print(f"  {i}. {rec}")
        print()
        
        print("📁 Results saved to: test_results/")
        print("🎉 Automated repository analysis completed!")
        
    except KeyboardInterrupt:
        print("\n⚠️  Analysis interrupted by user")
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
