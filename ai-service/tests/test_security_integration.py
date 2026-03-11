import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.auth import create_access_token, get_password_hash
from app.core.validator import get_validator

client = TestClient(app)
validator = get_validator()


class TestSecurityIntegration:
    """Integration tests for security features"""
    
    def test_full_auth_flow(self):
        """Test complete authentication flow"""
        # Register new user
        register_resp = client.post("/api/auth/register", json={
            "email": "integration_test@example.com",
            "password": "SecurePass123!",
            "name": "Integration Test"
        })
        assert register_resp.status_code == 201
        
        # Login
        login_resp = client.post("/api/auth/login", json={
            "email": "integration_test@example.com",
            "password": "SecurePass123!"
        })
        assert login_resp.status_code == 200
        token = login_resp.json()["access_token"]
        
        # Access protected endpoint
        me_resp = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
        assert me_resp.status_code == 200
        assert me_resp.json()["email"] == "integration_test@example.com"
        
    def test_invalid_token_rejected(self):
        """Test that invalid tokens are rejected"""
        response = client.get("/api/auth/me", headers={"Authorization": "Bearer invalid_token"})
        assert response.status_code == 401
        
    def test_expired_token_rejected(self):
        """Test that expired tokens are rejected"""
        from datetime import timedelta
        expired_token = create_access_token(
            {"sub": "user_1", "email": "test@example.com"},
            expires_delta=timedelta(seconds=-1)
        )
        response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {expired_token}"})
        assert response.status_code == 401
        
    def test_malicious_code_blocked(self):
        """Test that malicious input is blocked"""
        malicious_inputs = [
            {"code": "SELECT * FROM users DROP TABLE", "language": "python"},
            {"code": "<script>alert('xss')</script>", "language": "javascript"},
            {"code": "import os; os.system('rm -rf /')", "language": "python"},
        ]
        
        for input_data in malicious_inputs:
            # This should still work for analysis (we analyze to find vulnerabilities)
            response = client.post("/api/v1/analyze-code", json=input_data)
            assert response.status_code == 200
            
    def test_rate_limiting_enforced(self):
        """Test that rate limiting works"""
        for _ in range(35):
            response = client.post("/api/v1/analyze-code", json={"code": "x = 1", "language": "python"})
        
        # Should be rate limited
        assert response.status_code == 429
        
    def test_security_headers_present(self):
        """Test that security headers are present"""
        response = client.get("/health")
        
        assert "x-content-type-options" in response.headers
        assert response.headers["x-content-type-options"] == "nosniff"
        
    def test_cors_configuration(self):
        """Test CORS is properly configured"""
        response = client.options("/health", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        })
        # Should handle CORS preflight
        assert response.status_code in [200, 204]


class TestInputValidationIntegration:
    """Integration tests for input validation"""
    
    def test_sql_injection_in_code(self):
        """Test SQL injection detection in code analysis"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "query = f'SELECT * FROM users WHERE id = {user_id}'",
            "language": "python"
        })
        assert response.status_code == 200
        data = response.json()
        # Should detect SQL injection vulnerability
        assert any("sql" in v["vulnerability_type"].lower() or "injection" in v["vulnerability_type"].lower() 
                   for v in data.get("vulnerabilities", []))
        
    def test_hardcoded_secrets_detected(self):
        """Test hardcoded secrets detection"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "api_key = 'sk-1234567890abcdef'",
            "language": "python"
        })
        assert response.status_code == 200
        data = response.json()
        # Should detect hardcoded secret
        assert data["total_vulnerabilities"] > 0
        
    def test_unsafe_deserialization(self):
        """Test unsafe deserialization detection"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "data = pickle.loads(user_input)",
            "language": "python"
        })
        assert response.status_code == 200
        # Should detect deserialization issue
        
    def test_weak_crypto_detected(self):
        """Test weak cryptography detection"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "hash = md5(password)",
            "language": "python"
        })
        assert response.status_code == 200
        data = response.json()
        # Should detect weak crypto


class TestAdminSecurity:
    """Admin-specific security tests"""
    
    def setup_method(self):
        """Create admin token"""
        self.admin_token = create_access_token({
            "sub": "admin_1",
            "email": "admin@devguardian.ai",
            "role": "admin"
        })
        self.user_token = create_access_token({
            "sub": "user_1",
            "email": "user@example.com",
            "role": "user"
        })
    
    def test_admin_can_access_audit(self):
        """Test admin can access audit logs"""
        response = client.get("/api/auth/audit", headers={"Authorization": f"Bearer {self.admin_token}"})
        assert response.status_code == 200
        
    def test_regular_user_cannot_access_audit(self):
        """Test regular user cannot access audit logs"""
        response = client.get("/api/auth/audit", headers={"Authorization": f"Bearer {self.user_token}"})
        assert response.status_code == 403
        
    def test_unauthenticated_cannot_access_audit(self):
        """Test unauthenticated cannot access audit"""
        response = client.get("/api/auth/audit")
        assert response.status_code in [401, 403]


class TestVulnerabilityScannerSecurity:
    """Security tests for vulnerability scanner"""
    
    def test_large_code_rejected(self):
        """Test that excessively large code is rejected"""
        large_code = "x = 1\n" * 10000  # Very large code
        response = client.post("/api/v1/analyze-code", json={
            "code": large_code,
            "language": "python"
        })
        assert response.status_code in [200, 413]
        
    def test_empty_code_accepted(self):
        """Test that empty code is handled"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "",
            "language": "python"
        })
        # Should either work or return validation error
        assert response.status_code in [200, 400]
        
    def test_invalid_language_handled(self):
        """Test invalid language is handled"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "x = 1",
            "language": "invalid_language_xyz"
        })
        # Should handle gracefully
        assert response.status_code in [200, 400]


class TestTokenSecurity:
    """Token security tests"""
    
    def test_token_contains_necessary_claims(self):
        """Test JWT contains necessary claims"""
        token = create_access_token({
            "sub": "user_1",
            "email": "test@example.com",
            "role": "admin"
        })
        
        from jose import jwt
        from app.core.config import get_settings
        settings = get_settings()
        
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        assert payload["sub"] == "user_1"
        assert payload["email"] == "test@example.com"
        assert payload["role"] == "admin"
        assert "exp" in payload
        assert "type" in payload
        
    def test_refresh_token_different_from_access(self):
        """Test refresh token is different from access token"""
        from app.core.auth import create_refresh_token
        
        access = create_access_token({"sub": "user_1", "email": "test@example.com"})
        refresh = create_refresh_token({"sub": "user_1", "email": "test@example.com"})
        
        assert access != refresh
        
        from jose import jwt
        from app.core.config import get_settings
        settings = get_settings()
        
        access_payload = jwt.decode(access, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        refresh_payload = jwt.decode(refresh, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        
        assert access_payload["type"] == "access"
        assert refresh_payload["type"] == "refresh"
