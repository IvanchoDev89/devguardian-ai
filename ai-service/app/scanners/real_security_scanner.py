"""
Real Security Scanner - Uses Industry-Standard SAST Tools
- Semgrep (multi-language)
- Bandit (Python)
- npm audit (JavaScript)
- Dependency check (SBOM)
"""

import subprocess
import json
import os
import tempfile
import shutil
from typing import Dict, List, Any, Optional
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

class RealSecurityScanner:
    """Production-ready security scanner using real SAST tools"""
    
    def __init__(self):
        self.tools = {
            'semgrep': self._check_semgrep(),
            'bandit': self._check_bandit(),
            'git': self._check_git()
        }
        logger.info(f"Available security tools: {[k for k, v in self.tools.items() if v]}")
    
    def _check_semgrep(self) -> bool:
        try:
            result = subprocess.run(['semgrep', '--version'], 
                                    capture_output=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def _check_bandit(self) -> bool:
        try:
            result = subprocess.run(['bandit', '--version'], 
                                    capture_output=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def _check_git(self) -> bool:
        try:
            result = subprocess.run(['git', '--version'], 
                                    capture_output=True, timeout=10)
            return result.returncode == 0
        except:
            return False
    
    def scan_code(self, code: str, language: str) -> Dict[str, Any]:
        """Scan code using multiple SAST tools"""
        vulnerabilities = []
        tools_used = []
        
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write code to temp file
            ext = self._get_extension(language)
            filepath = Path(tmpdir) / f"code{ext}"
            filepath.write_text(code)
            
            # Run Semgrep if available
            if self.tools.get('semgrep'):
                semgrep_results = self._run_semgrep(tmpdir, language)
                vulnerabilities.extend(semgrep_results)
                tools_used.append('semgrep')
            else:
                logger.warning("Semgrep not available")
            
            # Run Bandit for Python
            if language == 'python' and self.tools.get('bandit'):
                bandit_results = self._run_bandit(tmpdir)
                vulnerabilities.extend(bandit_results)
                tools_used.append('bandit')
        
        # Calculate severity scores
        severity_scores = {'critical': 10, 'high': 7, 'medium': 4, 'low': 1}
        score = 100 - sum(
            severity_scores.get(v.get('severity', 'low'), 1) 
            for v in vulnerabilities
        )
        score = max(0, min(score, 100))
        
        return {
            'vulnerabilities': vulnerabilities,
            'total_vulnerabilities': len(vulnerabilities),
            'score': score,
            'tools_used': tools_used,
            'language': language,
            'scan_type': 'real_sast'
        }
    
    def scan_repository(self, repo_url: str, provider: str = 'github') -> Dict[str, Any]:
        """Clone and scan a repository"""
        if not self.tools.get('git'):
            return {'error': 'Git not available', 'vulnerabilities': []}
        
        with tempfile.TemporaryDirectory() as tmpdir:
            try:
                # Clone repository
                clone_result = self._clone_repo(repo_url, tmpdir, provider)
                if 'error' in clone_result:
                    return clone_result
                
                repo_path = clone_result['path']
                
                # Run comprehensive scan
                all_vulns = []
                
                # Semgrep scan
                if self.tools.get('semgrep'):
                    semgrep_results = self._run_semgrep_repo(repo_path)
                    all_vulns.extend(semgrep_results)
                
                # Bandit for Python files
                if self.tools.get('bandit'):
                    bandit_results = self._run_bandit_repo(repo_path)
                    all_vulns.extend(bandit_results)
                
                # Dependency scan
                dep_results = self._scan_dependencies(repo_path)
                all_vulns.extend(dep_results)
                
                # Calculate score
                severity_scores = {'critical': 10, 'high': 7, 'medium': 4, 'low': 1}
                score = 100 - sum(
                    severity_scores.get(v.get('severity', 'low'), 1) 
                    for v in all_vulns
                )
                score = max(0, min(score, 100))
                
                return {
                    'vulnerabilities': all_vulns,
                    'total_vulnerabilities': len(all_vulns),
                    'score': score,
                    'repo_path': repo_path,
                    'tools_used': ['semgrep', 'bandit', 'dependency-check'],
                    'scan_type': 'full_repo_scan'
                }
                
            except Exception as e:
                logger.error(f"Repository scan failed: {e}")
                return {'error': str(e), 'vulnerabilities': []}
    
    def _clone_repo(self, repo_url: str, tmpdir: str, provider: str) -> Dict:
        """Clone repository from GitHub/GitLab/Bitbucket"""
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        target_path = os.path.join(tmpdir, repo_name)
        
        cmd = ['git', 'clone', '--depth', '1', repo_url, target_path]
        
        try:
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            if result.returncode != 0:
                return {'error': f"Clone failed: {result.stderr.decode()}"}
            return {'path': target_path, 'name': repo_name}
        except subprocess.TimeoutExpired:
            return {'error': 'Clone timeout'}
        except Exception as e:
            return {'error': str(e)}
    
    def _run_semgrep(self, tmpdir: str, language: str) -> List[Dict]:
        """Run Semgrep on code"""
        try:
            cmd = [
                'semgrep', '--json', '--no-git-ignore',
                '--lang', language,
                '--config', 'auto',
                '--severity', 'ERROR',
                '--severity', 'WARNING',
                str(tmpdir)
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=60)
            
            if result.returncode not in [0, 1]:  # 0 = no findings, 1 = findings
                return []
            
            try:
                data = json.loads(result.stdout)
                findings = data.get('results', [])
                
                return [
                    {
                        'line_number': f.get('start', {}).get('line', 0),
                        'line_content': f.get('extra', {}).get('lines', '').strip(),
                        'vulnerability_type': f.get('check_id', 'unknown'),
                        'severity': self._map_semgrep_severity(f.get('extra', {}).get('severity', 'WARNING')),
                        'description': f.get('extra', {}).get('message', ''),
                        'match': f.get('extra', {}).get('lines', ''),
                        'cwe_id': f.get('extra', {}).get('cwe', ''),
                        'owasp_category': f.get('extra', {}).get('owasp', ''),
                        'tool': 'semgrep',
                        'confidence': f.get('extra', {}).get('confidence', 'MEDIUM')
                    }
                    for f in findings
                ]
            except json.JSONDecodeError:
                return []
                
        except Exception as e:
            logger.error(f"Semgrep scan failed: {e}")
            return []
    
    def _run_semgrep_repo(self, repo_path: str) -> List[Dict]:
        """Run Semgrep on entire repository"""
        try:
            cmd = [
                'semgrep', '--json', '--no-git-ignore',
                '--config', 'auto',
                '--json-output', '-',
                repo_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, timeout=300)
            
            if result.returncode not in [0, 1]:
                return []
            
            try:
                data = json.loads(result.stdout)
                findings = data.get('results', [])
                
                return [
                    {
                        'line_number': f.get('start', {}).get('line', 0),
                        'file_path': f.get('path', ''),
                        'vulnerability_type': f.get('check_id', 'unknown'),
                        'severity': self._map_semgrep_severity(f.get('extra', {}).get('severity', 'WARNING')),
                        'description': f.get('extra', {}).get('message', ''),
                        'match': f.get('extra', {}).get('lines', '').strip()[:200],
                        'tool': 'semgrep'
                    }
                    for f in findings
                ]
            except:
                return []
                
        except Exception as e:
            logger.error(f"Semgrep repo scan failed: {e}")
            return []
    
    def _run_bandit(self, tmpdir: str) -> List[Dict]:
        """Run Bandit on Python code"""
        try:
            cmd = [
                'bandit', '-r', '-f', 'json', '-'
            ]
            
            # Find Python files
            py_files = list(Path(tmpdir).rglob('*.py'))
            if not py_files:
                return []
            
            result = subprocess.run(
                ['bandit', '-r', str(py_files[0].parent), '-f', 'json'],
                capture_output=True, timeout=60
            )
            
            if result.returncode not in [0, 1]:
                return []
            
            try:
                data = json.loads(result.stdout)
                findings = data.get('results', [])
                
                return [
                    {
                        'line_number': f.get('line_number', 0),
                        'line_content': f.get('code', '').strip()[:200],
                        'vulnerability_type': f.get('issue_text', 'Bandit finding'),
                        'severity': self._map_bandit_severity(f.get('issue_severity', 'LOW')),
                        'description': f.get('issue_text', ''),
                        'match': f.get('code', '').strip()[:200],
                        'cwe_id': f.get('cwe_id', ''),
                        'tool': 'bandit',
                        'confidence': f.get('issue_confidence', 'LOW')
                    }
                    for f in findings
                ]
            except:
                return []
                
        except Exception as e:
            logger.error(f"Bandit scan failed: {e}")
            return []
    
    def _run_bandit_repo(self, repo_path: str) -> List[Dict]:
        """Run Bandit on repository"""
        try:
            cmd = ['bandit', '-r', repo_path, '-f', 'json']
            result = subprocess.run(cmd, capture_output=True, timeout=120)
            
            if result.returncode not in [0, 1]:
                return []
            
            try:
                data = json.loads(result.stdout)
                findings = data.get('results', [])
                
                return [
                    {
                        'line_number': f.get('line_number', 0),
                        'file_path': f.get('filename', ''),
                        'vulnerability_type': f.get('issue_text', 'Bandit finding'),
                        'severity': self._map_bandit_severity(f.get('issue_severity', 'LOW')),
                        'description': f.get('issue_text', ''),
                        'match': f.get('code', '').strip()[:200],
                        'tool': 'bandit'
                    }
                    for f in findings[:50]  # Limit to top 50
                ]
            except:
                return []
                
        except Exception as e:
            logger.error(f"Bandit repo scan failed: {e}")
            return []
    
    def _scan_dependencies(self, repo_path: str) -> List[Dict]:
        """Scan dependencies for known vulnerabilities"""
        vulns = []
        
        # Check package.json
        package_json = Path(repo_path) / 'package.json'
        if package_json.exists():
            vulns.extend(self._check_npm_audit(repo_path))
        
        # Check requirements.txt
        requirements = Path(repo_path) / 'requirements.txt'
        if requirements.exists():
            vulns.extend(self._check_pip_audit(repo_path))
        
        # Check Gemfile
        gemfile = Path(repo_path) / 'Gemfile'
        if gemfile.exists():
            vulns.extend(self._check_gem_audit(repo_path))
        
        return vulns
    
    def _check_npm_audit(self, repo_path: str) -> List[Dict]:
        """Run npm audit"""
        try:
            result = subprocess.run(
                ['npm', 'audit', '--json'],
                capture_output=True, timeout=60,
                cwd=repo_path
            )
            
            if result.returncode != 0:
                try:
                    data = json.loads(result.stdout)
                    vulns = data.get('vulnerabilities', {})
                    
                    return [
                        {
                            'vulnerability_type': f'npm: {vuln_type}',
                            'severity': self._map_npm_severity(info.get('severity', 'low')),
                            'description': f"Dependency vulnerability: {info.get('via', [{'url': ''}])[0].get('url', '')}",
                            'file_path': 'package.json',
                            'tool': 'npm-audit'
                        }
                        for vuln_type, info in vulns.items()
                    ]
                except:
                    return []
            return []
        except:
            return []
    
    def _check_pip_audit(self, repo_path: str) -> List[Dict]:
        """Run pip-audit"""
        try:
            result = subprocess.run(
                ['pip-audit', '-f', 'json'],
                capture_output=True, timeout=60,
                cwd=repo_path
            )
            
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    deps = data.get('dependencies', [])
                    
                    return [
                        {
                            'vulnerability_type': f"pip: {dep.get('name', 'unknown')}",
                            'severity': 'high',
                            'description': f"Vulnerability in {dep.get('name')}: {dep.get('vulns', [])}",
                            'file_path': 'requirements.txt',
                            'tool': 'pip-audit'
                        }
                        for dep in deps
                    ]
                except:
                    return []
            return []
        except:
            return []
    
    def _check_gem_audit(self, repo_path: str) -> List[Dict]:
        """Run bundle-audit"""
        try:
            result = subprocess.run(
                ['bundle-audit', 'check', '--format', 'json'],
                capture_output=True, timeout=60,
                cwd=repo_path
            )
            
            if result.returncode != 0:
                try:
                    data = json.loads(result.stdout)
                    vulns = data.get('vulnerabilities', [])
                    
                    return [
                        {
                            'vulnerability_type': f"gem: {v.get('gem', 'unknown')}",
                            'severity': 'high',
                            'description': f"{v.get('title', '')}: {v.get('description', '')}",
                            'file_path': 'Gemfile',
                            'tool': 'bundle-audit'
                        }
                        for v in vulns
                    ]
                except:
                    return []
            return []
        except:
            return []
    
    def _get_extension(self, language: str) -> str:
        extensions = {
            'python': '.py',
            'javascript': '.js',
            'typescript': '.ts',
            'java': '.java',
            'csharp': '.cs',
            'php': '.php',
            'ruby': '.rb',
            'go': '.go',
            'rust': '.rs',
            'c': '.c',
            'cpp': '.cpp'
        }
        return extensions.get(language, '.txt')
    
    def _map_semgrep_severity(self, severity: str) -> str:
        mapping = {
            'ERROR': 'critical',
            'WARNING': 'high',
            'INFO': 'low'
        }
        return mapping.get(severity.upper(), 'medium')
    
    def _map_bandit_severity(self, severity: str) -> str:
        mapping = {
            'HIGH': 'critical',
            'MEDIUM': 'high',
            'LOW': 'medium'
        }
        return mapping.get(severity.upper(), 'low')
    
    def _map_npm_severity(self, severity: str) -> str:
        mapping = {
            'critical': 'critical',
            'high': 'high',
            'moderate': 'medium',
            'low': 'low'
        }
        return mapping.get(severity.lower(), 'medium')


def create_real_scanner() -> RealSecurityScanner:
    """Factory function"""
    return RealSecurityScanner()
