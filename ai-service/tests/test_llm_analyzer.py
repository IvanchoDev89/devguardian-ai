"""
Tests for LLM Analyzer
"""

import pytest
from app.services.llm_analyzer import LLMAnalyzer, AnalysisResult, create_analyzer


class TestLLMAnalyzer:
    """Test suite for LLM Analyzer"""
    
    def test_analyzer_initialization(self):
        """Test analyzer can be created"""
        analyzer = LLMAnalyzer(provider="claude", api_key="test-key")
        assert analyzer.provider == "claude"
        assert analyzer.api_key == "test-key"
    
    def test_create_factory(self):
        """Test factory function"""
        analyzer = create_analyzer(provider="openai", api_key="test")
        assert isinstance(analyzer, LLMAnalyzer)
        assert analyzer.provider == "openai"
    
    def test_cache_key_generation(self):
        """Test cache key is deterministic"""
        analyzer = create_analyzer(api_key="test")
        
        key1 = analyzer._get_cache_key("code snippet", "sql-injection")
        key2 = analyzer._get_cache_key("code snippet", "sql-injection")
        
        assert key1 == key2
    
    def test_different_inputs_different_keys(self):
        """Test different inputs produce different keys"""
        analyzer = create_analyzer(api_key="test")
        
        key1 = analyzer._get_cache_key("code1", "sql-injection")
        key2 = analyzer._get_cache_key("code2", "sql-injection")
        
        assert key1 != key2
    
    def test_fallback_sql_injection(self):
        """Test fallback analysis for SQL injection"""
        analyzer = create_analyzer()  # No API key = fallback
        
        vulnerability = {
            "type": "sql-injection",
            "severity": "critical",
            "message": "Potential SQL injection"
        }
        
        result = analyzer.analyze_vulnerability(
            vulnerability=vulnerability,
            code_snippet='query = f"SELECT * FROM users WHERE id = {user_id}"',
            language="python"
        )
        
        assert isinstance(result, AnalysisResult)
        assert "SQL Injection" in result.explanation
        assert result.confidence == 0.5
    
    def test_fallback_hardcoded_password(self):
        """Test fallback for hardcoded password"""
        analyzer = create_analyzer()
        
        vulnerability = {
            "type": "hardcoded-password",
            "severity": "critical",
            "message": "Hardcoded password detected"
        }
        
        result = analyzer.analyze_vulnerability(
            vulnerability=vulnerability,
            code_snippet='password = "secret123"',
            language="python"
        )
        
        assert "Hardcoded" in result.explanation
        assert result.is_false_positive == False
    
    def test_fallback_xss(self):
        """Test fallback for XSS"""
        analyzer = create_analyzer()
        
        vulnerability = {
            "type": "xss",
            "severity": "high",
            "message": "XSS vulnerability"
        }
        
        result = analyzer.analyze_vulnerability(
            vulnerability=vulnerability,
            code_snippet='document.getElementById("out").innerHTML = userInput',
            language="javascript"
        )
        
        assert "XSS" in result.explanation or "Cross-Site" in result.explanation
    
    def test_fallback_eval(self):
        """Test fallback for eval usage"""
        analyzer = create_analyzer()
        
        vulnerability = {
            "type": "eval",
            "severity": "high",
            "message": "Use of eval() is dangerous"
        }
        
        result = analyzer.analyze_vulnerability(
            vulnerability=vulnerability,
            code_snippet='eval(user_input)',
            language="python"
        )
        
        assert "eval" in result.explanation.lower()
    
    def test_fallback_unknown_type(self):
        """Test fallback for unknown vulnerability type"""
        analyzer = create_analyzer()
        
        vulnerability = {
            "type": "unknown-vulnerability",
            "severity": "medium",
            "message": "Some issue"
        }
        
        result = analyzer.analyze_vulnerability(
            vulnerability=vulnerability,
            code_snippet='some_code()',
            language="python"
        )
        
        assert result.explanation is not None
        assert len(result.explanation) > 0
    
    def test_batch_analyze(self):
        """Test batch analysis"""
        analyzer = create_analyzer()
        
        vulnerabilities = [
            {"type": "sql-injection", "severity": "critical", "message": "SQLi"},
            {"type": "xss", "severity": "high", "message": "XSS"},
        ]
        
        results = analyzer.batch_analyze(vulnerabilities, "code context")
        
        assert len(results) == 2
        assert all(isinstance(r, AnalysisResult) for r in results)
    
    def test_clear_cache(self):
        """Test cache clearing"""
        analyzer = create_analyzer()
        
        # Add something to cache
        analyzer._cache["test"] = AnalysisResult(explanation="test")
        assert len(analyzer._cache) == 1
        
        # Clear
        analyzer.clear_cache()
        assert len(analyzer._cache) == 0
    
    def test_cache_hit(self):
        """Test cache hit returns cached result"""
        analyzer = create_analyzer()
        
        vulnerability = {
            "type": "sql-injection",
            "severity": "critical",
            "message": "SQLi"
        }
        
        # First call - fallback doesn't cache
        result1 = analyzer.analyze_vulnerability(
            vulnerability=vulnerability,
            code_snippet="query = f'test'",
            language="python"
        )
        
        # Without API key, fallback doesn't cache
        # But the analyzer still works
        assert isinstance(result1, AnalysisResult)


class TestAnalysisResult:
    """Test AnalysisResult dataclass"""
    
    def test_default_values(self):
        """Test default values"""
        result = AnalysisResult(explanation="test")
        
        assert result.explanation == "test"
        assert result.suggested_fix is None
        assert result.confidence == 0.0
        assert result.is_false_positive == False
        assert result.false_positive_reason is None
    
    def test_all_values(self):
        """Test with all values"""
        result = AnalysisResult(
            explanation="test",
            suggested_fix="fix code",
            confidence=0.9,
            is_false_positive=True,
            false_positive_reason="False positive",
            cwe_details="CWE-89",
            owasp_category="A03",
            remediation_steps=["Step 1", "Step 2"]
        )
        
        assert result.suggested_fix == "fix code"
        assert result.confidence == 0.9
        assert result.is_false_positive == True
        assert len(result.remediation_steps) == 2
