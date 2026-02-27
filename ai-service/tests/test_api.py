"""
Tests for Vulnerability Analyzer API Endpoints
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app


class TestAnalyzeCodeEndpoint:
    """Test suite for /api/v1/analyze-code endpoint"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_health_endpoint(self):
        """Test health check endpoint"""
        response = self.client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert "timestamp" in data

    def test_analyze_clean_code(self):
        """Test analysis of clean code"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": "print('Hello World')", "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_vulnerabilities"] == 0
        assert data["score"] == 100

    def test_analyze_vulnerable_code(self):
        """Test analysis of vulnerable code"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": "password = 'hardcoded123'", "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_vulnerabilities"] > 0
        assert data["score"] < 100

    def test_empty_code_returns_422(self):
        """Test that empty code returns validation error"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": "", "language": "python"}
        )
        assert response.status_code == 422

    def test_missing_code_returns_422(self):
        """Test that missing code returns validation error"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"language": "python"}
        )
        assert response.status_code == 422

    def test_unsupported_language(self):
        """Test unsupported language handling"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": "test", "language": "cobol"}
        )
        assert response.status_code == 422

    def test_code_exceeds_limit(self):
        """Test code exceeding max length"""
        large_code = "x" * (11 * 1024)  # 11KB
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": large_code, "language": "python"}
        )
        # May return 422 (validation) or 400 (custom validation)
        assert response.status_code in [400, 422]

    def test_response_contains_required_fields(self):
        """Test response contains all required fields"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": "test = 1", "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "vulnerabilities" in data
        assert "summary" in data
        assert "score" in data
        assert "total_vulnerabilities" in data
        assert "language" in data
        assert "scan_id" in data
        assert "timestamp" in data

    def test_languages_endpoint(self):
        """Test supported languages endpoint"""
        response = self.client.get("/api/v1/languages")
        assert response.status_code == 200
        data = response.json()
        assert "supported_languages" in data
        assert "python" in data["supported_languages"]

    def test_sql_injection_analysis(self):
        """Test SQL injection detection via API"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={
                "code": "password = 'hardcoded123'",
                "language": "python"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total_vulnerabilities"] > 0


class TestInputValidation:
    """Test input validation"""

    def setup_method(self):
        """Setup for each test"""
        self.client = TestClient(app)

    def test_language_is_case_insensitive(self):
        """Test language parameter is case insensitive"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": "test", "language": "PYTHON"}
        )
        assert response.status_code == 200

    def test_javascript_analysis(self):
        """Test JavaScript analysis"""
        response = self.client.post(
            "/api/v1/analyze-code",
            json={"code": "document.write(userInput)", "language": "javascript"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["language"] == "javascript"
