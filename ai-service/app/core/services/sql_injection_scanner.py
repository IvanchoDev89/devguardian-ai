"""
Real SQL Injection Scanner - Analyzes code files for SQL injection vulnerabilities
"""

import re
import os
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum


class Severity(Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class SQLInjectionFinding:
    file_path: str
    line_number: int
    code_snippet: str
    vulnerability_type: str
    severity: Severity
    cwe_id: str
    description: str
    confidence: float
    remediation: str
    sink: str
    source: str


class SQLInjectionScanner:
    """Real SQL injection vulnerability scanner"""
    
    def __init__(self):
        self.findings: List[SQLInjectionFinding] = []
        
        # SQL injection sinks - where user input meets SQL
        self.sql_sinks = [
            r'\.query\s*\(',
            r'\.execute\s*\(',
            r'\.raw\s*\(',
            r'db\.raw\s*\(',
            r'SELECT\s+',
            r'INSERT\s+',
            r'UPDATE\s+',
            r'DELETE\s+',
            r'execute\s*\(',
            r'exec\s*\(',
            r'mysql_query\s*\(',
            r'mysqli_query\s*\(',
            r'pg_query\s*\(',
            r'mongodb\.find\s*\(',
            r'collection\.find\s*\(',
            r'\$wpdb->query\s*\(',
            r'Cursor\.execute\s*\(',
        ]
        
        # User input sources - where user data comes from
        self.user_inputs = [
            r'\$_(GET|POST|REQUEST|COOKIE|FILES)\s*\[',
            r'req\.body\.',
            r'req\.query\.',
            r'req\.params\.',
            r'request\.',
            r'params\[',
            r'body\[',
            r'query\[',
            r'Input::',
            r'request\(\)->',
            r'Request::',
        ]
        
        # Unsafe string interpolation patterns
        self.unsafe_patterns = [
            (r'["\'].*?%\s*s.*?["\'].*?\.format\s*\(', 'String formatting'),
            (r'["\'].*?\{.*?\}.*?["\'].*?\.format\s*\(', 'String formatting'),
            (r'\+\s*["\'][^"\']*\+', 'String concatenation'),
            (r'f["\'][^"\']*\{.*?\}', 'F-string injection'),
            (r'\$\w+\s*\.\s*\$', 'Variable interpolation'),
        ]
        
        # Taint flow: source -> sink analysis
        self.vulnerability_rules = [
            {
                'pattern': r'(\$\w+(?:\[[^\]]+\])?)\s*\.\s*query\s*\(\s*["\'].*?\1',
                'type': 'Direct variable in query',
                'severity': Severity.CRITICAL,
                'cwe': 'CWE-89',
                'remediation': 'Use parameterized queries or prepared statements'
            },
            {
                'pattern': r'execute\s*\(\s*["\'].*?\$\w+',
                'type': 'String concatenation in execute',
                'severity': Severity.CRITICAL,
                'cwe': 'CWE-89',
                'remediation': 'Use execute with parameter binding: execute(query, [params])'
            },
            {
                'pattern': r'query\s*\(\s*["\'].*?\$\{?\w+\}?',
                'type': 'String interpolation in query',
                'severity': Severity.CRITICAL,
                'cwe': 'CWE-89',
                'remediation': 'Use query builder with parameter binding'
            },
            {
                'pattern': r'SELECT\s+.*?FROM.*?WHERE.*?["\'].*?\$\w+',
                'type': 'Direct variable in WHERE clause',
                'severity': Severity.HIGH,
                'cwe': 'CWE-89',
                'remediation': 'Use parameterized WHERE clauses'
            },
            {
                'pattern': r'f["\'][^"\']*\{[^"\']+\}[^"\']*["\'].*?\.format|query|execute',
                'type': 'F-string in SQL',
                'severity': Severity.CRITICAL,
                'cwe': 'CWE-89',
                'remediation': 'Use parameterized queries instead of f-strings'
            },
            {
                'pattern': r'\.format\s*\(\s*\{[^}]*\}.*?\)\s*\.query|\.execute',
                'type': '.format() in SQL method',
                'severity': Severity.CRITICAL,
                'cwe': 'CWE-89',
                'remediation': 'Use query parameter binding'
            },
        ]

    def scan_file(self, file_path: str) -> List[SQLInjectionFinding]:
        """Scan a single file for SQL injection vulnerabilities"""
        findings = []
        
        if not os.path.exists(file_path):
            return findings
            
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
        except Exception:
            return findings
        
        code = ''.join(lines)
        
        # Check each line for vulnerabilities
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if self._is_comment(line):
                continue
                
            for rule in self.vulnerability_rules:
                matches = re.finditer(rule['pattern'], line, re.IGNORECASE)
                for match in matches:
                    finding = SQLInjectionFinding(
                        file_path=file_path,
                        line_number=line_num,
                        code_snippet=line.strip(),
                        vulnerability_type=rule['type'],
                        severity=rule['severity'],
                        cwe_id=rule['cwe'],
                        description=self._generate_description(rule['type'], match.group()),
                        confidence=self._calculate_confidence(line),
                        remediation=rule['remediation'],
                        sink=self._identify_sink(line),
                        source=self._identify_source(line)
                    )
                    findings.append(finding)
        
        # Check for unsafe string operations
        findings.extend(self._scan_unsafe_strings(code, lines, file_path))
        
        return findings

    def scan_directory(self, directory: str, extensions: List[str] = None) -> List[SQLInjectionFinding]:
        """Scan all files in a directory"""
        if extensions is None:
            extensions = ['.php', '.js', '.ts', '.py', '.java', '.rb', '.go', '.cs']
            
        findings = []
        
        for root, dirs, files in os.walk(directory):
            # Skip common non-code directories
            dirs[:] = [d for d in dirs if d not in ['node_modules', 'vendor', '.git', 'dist', 'build']]
            
            for file in files:
                if any(file.endswith(ext) for ext in extensions):
                    file_path = os.path.join(root, file)
                    findings.extend(self.scan_file(file_path))
        
        return findings

    def scan_code_string(self, code: str, language: str = 'unknown') -> List[SQLInjectionFinding]:
        """Scan a code string directly"""
        findings = []
        
        for rule in self.vulnerability_rules:
            matches = re.finditer(rule['pattern'], code, re.IGNORECASE | re.MULTILINE)
            for match in matches:
                # Find line number
                line_num = code[:match.start()].count('\n') + 1
                
                finding = SQLInjectionFinding(
                    file_path='inline',
                    line_number=line_num,
                    code_snippet=self._get_line(code, line_num),
                    vulnerability_type=rule['type'],
                    severity=rule['severity'],
                    cwe_id=rule['cwe'],
                    description=self._generate_description(rule['type'], match.group()),
                    confidence=self._calculate_confidence(match.group()),
                    remediation=rule['remediation'],
                    sink=self._identify_sink(match.group()),
                    source=self._identify_source(match.group())
                )
                findings.append(finding)
        
        return findings

    def _scan_unsafe_strings(self, code: str, lines: List[str], file_path: str) -> List[SQLInjectionFinding]:
        """Scan for unsafe string operations that could lead to SQL injection"""
        findings = []
        
        unsafe_patterns = [
            (r'["\'].*?%\s*[sd].*?["\'].*?%\s*\(', 'printf-style string formatting'),
            (r'\+\s*["\'][^"\']+\s*\+\s*\$\w+', 'string concatenation with variable'),
            (r'f["\'][^"\']*\{[^"\']+\}', 'f-string with braces'),
        ]
        
        for line_num, line in enumerate(lines, 1):
            for pattern, desc in unsafe_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # Check if this line also has SQL
                    has_sql = any(re.search(sink, line, re.IGNORECASE) for sink in self.sql_sinks)
                    
                    if has_sql:
                        finding = SQLInjectionFinding(
                            file_path=file_path,
                            line_number=line_num,
                            code_snippet=line.strip(),
                            vulnerability_type='Potential SQL injection via string',
                            severity=Severity.HIGH,
                            cwe_id='CWE-89',
                            description=f'Unsafe string operation: {desc}',
                            confidence=70.0,
                            remediation='Use parameterized queries',
                            sink=self._identify_sink(line),
                            source='unknown'
                        )
                        findings.append(finding)
        
        return findings

    def _is_comment(self, line: str) -> bool:
        """Check if line is a comment"""
        return bool(re.match(r'^\s*(//|#|/\*|\*|--)', line))

    def _identify_sink(self, line: str) -> str:
        """Identify the SQL sink in the line"""
        for sink in self.sql_sinks:
            if re.search(sink, line, re.IGNORECASE):
                return sink
        return 'unknown'

    def _identify_source(self, line: str) -> str:
        """Identify the user input source in the line"""
        for source in self.user_inputs:
            if re.search(source, line, re.IGNORECASE):
                return source
        return 'unknown'

    def _calculate_confidence(self, line: str) -> float:
        """Calculate confidence score based on context"""
        confidence = 50.0
        
        # Higher confidence if both source and sink present
        if self._identify_source(line) != 'unknown':
            confidence += 20
        if self._identify_sink(line) != 'unknown':
            confidence += 20
            
        # Higher confidence for direct variable usage
        if '$' in line and ('query' in line.lower() or 'execute' in line.lower()):
            confidence += 10
            
        return min(confidence, 100.0)

    def _generate_description(self, vuln_type: str, match: str) -> str:
        """Generate a human-readable description"""
        return f"{vuln_type}: Found pattern '{match[:50]}...' that may allow SQL injection"

    def _get_line(self, code: str, line_num: int) -> str:
        """Get specific line from code"""
        lines = code.split('\n')
        if 0 < line_num <= len(lines):
            return lines[line_num - 1].strip()
        return ''

    def generate_report(self, findings: List[SQLInjectionFinding]) -> Dict[str, Any]:
        """Generate a scan report"""
        if not findings:
            return {
                'summary': 'No SQL injection vulnerabilities found',
                'total_findings': 0,
                'by_severity': {},
                'findings': []
            }
        
        by_severity = {
            'critical': len([f for f in findings if f.severity == Severity.CRITICAL]),
            'high': len([f for f in findings if f.severity == Severity.HIGH]),
            'medium': len([f for f in findings if f.severity == Severity.MEDIUM]),
            'low': len([f for f in findings if f.severity == Severity.LOW]),
        }
        
        return {
            'summary': f"Found {len(findings)} potential SQL injection vulnerabilities",
            'total_findings': len(findings),
            'by_severity': by_severity,
            'findings': [
                {
                    'file': f.file_path,
                    'line': f.line_number,
                    'type': f.vulnerability_type,
                    'severity': f.severity.value,
                    'cwe_id': f.cwe_id,
                    'confidence': f.confidence,
                    'code': f.code_snippet,
                    'remediation': f.remediation
                }
                for f in findings
            ]
        }


if __name__ == '__main__':
    # Example usage
    scanner = SQLInjectionScanner()
    
    # Test code
    test_code = '''
    $sql = "SELECT * FROM users WHERE id = " . $_GET['id'];
    db.query($sql);
    
    $name = $_POST['name'];
    $result = db.execute("INSERT INTO users (name) VALUES ('" . $name . "')");
    '''
    
    findings = scanner.scan_code_string(test_code)
    report = scanner.generate_report(findings)
    print(report)
