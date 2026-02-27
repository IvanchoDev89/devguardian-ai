"""
Tests for Semgrep Scanner
"""

import pytest
import asyncio
import tempfile
import os
from pathlib import Path

from app.scanners.semgrep_scanner import (
    SemgrepScanner,
    SemgrepFinding,
    ClaudeAnalyzer,
    create_semgrep_scanner
)


class TestSemgrepFinding:
    """Test SemgrepFinding model"""
    
    def test_severity_mapping(self):
        """Test severity normalization"""
        # Test ERROR -> critical
        finding = SemgrepFinding(
            check_id="test.check",
            path="test.py",
            start_line=1,
            end_line=1,
            start_col=1,
            end_col=1,
            severity="ERROR",
            message="Test message",
            metadata={},
            extra={}
        )
        assert finding.normalized_severity == "critical"
        
        # Test WARNING -> high
        finding.severity = "WARNING"
        assert finding.normalized_severity == "high"
        
        # Test INFO -> low
        finding.severity = "INFO"
        assert finding.normalized_severity == "low"
        
    def test_to_dict(self):
        """Test serialization to dict"""
        finding = SemgrepFinding(
            check_id="test.check",
            path="test.py",
            start_line=10,
            end_line=15,
            start_col=5,
            end_col=20,
            severity="ERROR",
            message="SQL injection vulnerability",
            metadata={"cwe": "CWE-89"},
            extra={}
        )
        
        result = finding.to_dict()
        
        assert result["type"] == "test.check"
        assert result["file"] == "test.py"
        assert result["line"] == 10
        assert result["severity"] == "critical"
        assert result["cwe"] == "CWE-89"


class TestSemgrepScanner:
    """Test SemgrepScanner functionality"""
    
    def test_scanner_initialization(self):
        """Test scanner can be created with custom rules"""
        scanner = SemgrepScanner(
            rules=["p/python", "p/secrets"],
            timeout=120
        )
        
        assert scanner.rules == ["p/python", "p/secrets"]
        assert scanner.timeout == 120
        
    def test_default_rules(self):
        """Test default rules are set"""
        scanner = SemgrepScanner()
        
        assert "p/owasp-top-ten" in scanner.rules
        assert "p/secrets" in scanner.rules
        
    def test_size_limits(self):
        """Test size limits are set"""
        scanner = SemgrepScanner(max_file_size_mb=5)
        
        assert scanner.MAX_REPO_SIZE_MB == 100  # Default
        assert scanner.max_file_size_mb == 5
        
    def test_create_factory_function(self):
        """Test factory function creates scanner"""
        scanner = create_semgrep_scanner(timeout=60)
        
        assert isinstance(scanner, SemgrepScanner)
        assert scanner.timeout == 60


class TestClaudeAnalyzer:
    """Test Claude analyzer"""
    
    def test_analyzer_initialization(self):
        """Test analyzer can be created"""
        # Note: This will fail without valid API key, but tests initialization
        analyzer = ClaudeAnalyzer(api_key="test-key", cache_dir="/tmp/test_cache")
        
        assert analyzer.api_key == "test-key"
        assert analyzer.cache_dir == "/tmp/test_cache"
        
    def test_cache_key_generation(self):
        """Test cache key is deterministic"""
        analyzer = ClaudeAnalyzer(api_key="test")
        
        key1 = analyzer._get_cache_key("code snippet", "sql_injection")
        key2 = analyzer._get_cache_key("code snippet", "sql_injection")
        
        assert key1 == key2  # Same input = same key


class TestScannerIntegration:
    """Integration tests (require semgrep installed)"""
    
    @pytest.fixture
    def temp_dir(self):
        """Create temp directory for testing"""
        with tempfile.TemporaryDirectory() as tmpdir:
            yield tmpdir
            
    def test_scan_empty_directory(self, temp_dir):
        """Test scanning empty directory"""
        scanner = SemgrepScanner(timeout=30)
        
        # This should complete without error
        result = asyncio.run(scanner.scan_local_directory(temp_dir))
        
        assert result["status"] == "completed"
        assert result["total_findings"] == 0
        
    def test_temp_cleanup(self, temp_dir):
        """Test temp directories are cleaned up"""
        scanner = SemgrepScanner()
        
        # Run scan
        asyncio.run(scanner.scan_local_directory(temp_dir))
        
        # Check cleanup happened
        assert len(scanner._temp_dirs) == 0


# Run tests with: pytest app/scanners/test_semgrep_scanner.py -v
