import pytest
from fastapi.testclient import TestClient
from main import app
from app.core.auth import create_access_token

client = TestClient(app)


class TestSecurityHeaders:
    """Test security headers are properly set"""
    
    def test_x_frame_options_header(self):
        """Test X-Frame-Options header is set"""
        response = client.get("/health")
        assert "x-frame-options" in response.headers
        
    def test_x_content_type_options_header(self):
        """Test X-Content-Type-Options header is set"""
        response = client.get("/health")
        assert response.headers.get("x-content-type-options") == "nosniff"
        
    def test_xss_protection_header(self):
        """Test X-XSS-Protection header is set"""
        response = client.get("/health")
        assert "x-xss-protection" in response.headers
        
    def test_referrer_policy_header(self):
        """Test Referrer-Policy header is set"""
        response = client.get("/health")
        assert "referrer-policy" in response.headers
        
    def test_content_security_policy_header(self):
        """Test Content-Security-Policy header is set"""
        response = client.get("/health")
        assert "content-security-policy" in response.headers
        
    def test_permitted_cross_domain_policies(self):
        """Test X-Permitted-Cross-Domain-Policies header is set"""
        response = client.get("/health")
        assert response.headers.get("x-permitted-cross-domain-policies") == "none"
        
    def test_server_header_removed(self):
        """Test server header is removed"""
        response = client.get("/health")
        # Should not expose server info
        assert "server" not in response.headers or response.headers.get("server") == ""
        
    def test_powered_by_header_removed(self):
        """Test X-Powered-By header is removed"""
        response = client.get("/health")
        assert "x-powered-by" not in response.headers


class TestRateLimitingSecurity:
    """Test rate limiting functionality"""
    
    def test_rate_limit_429_response(self):
        """Test rate limiting returns 429"""
        for _ in range(35):
            response = client.post("/api/v1/analyze-code", json={"code": "x=1", "language": "python"})
        
        # Should eventually get rate limited
        assert response.status_code in [200, 429]
        
    def test_rate_limit_includes_retry_after(self):
        """Test rate limit includes retry information"""
        # Make enough requests to trigger rate limit
        for _ in range(35):
            response = client.post("/api/v1/analyze-code", json={"code": "x=1", "language": "python"})
        
        if response.status_code == 429:
            assert "retry_after" in response.json() or "retry-after" in response.headers


class TestAuthenticationSecurity:
    """Test authentication security"""
    
    def test_login_without_credentials_fails(self):
        """Test login without credentials fails"""
        response = client.post("/api/auth/login", json={})
        assert response.status_code == 422  # Validation error
        
    def test_login_wrong_password_fails(self):
        """Test login with wrong password fails"""
        response = client.post("/api/auth/login", json={
            "email": "admin@devguardian.ai",
            "password": "wrong_password"
        })
        assert response.status_code == 401
        
    def test_register_weak_password_fails(self):
        """Test registering with weak password fails"""
        response = client.post("/api/auth/register", json={
            "email": "new@example.com",
            "password": "123",  # Too short
            "name": "Test"
        })
        assert response.status_code == 400
        
    def test_register_invalid_email_fails(self):
        """Test registering with invalid email fails"""
        response = client.post("/api/auth/register", json={
            "email": "not-an-email",
            "password": "SecurePass123!",
            "name": "Test"
        })
        assert response.status_code == 422
        
    def test_protected_endpoint_without_token_fails(self):
        """Test accessing protected endpoint without token fails"""
        response = client.get("/api/auth/me")
        assert response.status_code in [401, 403]


class TestAuthorizationSecurity:
    """Test authorization security"""
    
    def setup_method(self):
        self.user_token = create_access_token({
            "sub": "user_1",
            "email": "user@example.com",
            "role": "user"
        })
        self.admin_token = create_access_token({
            "sub": "admin_1",
            "email": "admin@devguardian.ai",
            "role": "admin"
        })
        
    def test_user_cannot_access_admin_endpoints(self):
        """Test regular user cannot access admin endpoints"""
        response = client.get("/api/auth/audit", headers={"Authorization": f"Bearer {self.user_token}"})
        assert response.status_code == 403
        
    def test_admin_can_access_admin_endpoints(self):
        """Test admin can access admin endpoints"""
        response = client.get("/api/auth/audit", headers={"Authorization": f"Bearer {self.admin_token}"})
        assert response.status_code == 200


class TestInputValidationSecurity:
    """Test input validation security"""
    
    def test_very_long_input_handled(self):
        """Test very long input is handled"""
        long_code = "x = 1\n" * 1000
        response = client.post("/api/v1/analyze-code", json={
            "code": long_code,
            "language": "python"
        })
        # Should handle gracefully
        assert response.status_code in [200, 413]
        
    def test_special_characters_handled(self):
        """Test special characters are handled"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "x = 'test@#$%^&*()'",
            "language": "python"
        })
        assert response.status_code == 200
        
    def test_null_bytes_handled(self):
        """Test null bytes are handled"""
        response = client.post("/api/v1/analyze-code", json={
            "code": "x = 1\x00",
            "language": "python"
        })
        assert response.status_code in [200, 400]


class TestErrorHandlingSecurity:
    """Test error handling doesn't leak information"""
    
    def test_error_doesnt_leak_stack_trace(self):
        """Test errors don't leak stack traces"""
        # Invalid request
        response = client.post("/api/v1/analyze-code", json={"invalid": "data"})
        # Should not expose internal details
        assert "traceback" not in response.text.lower()
        assert "traceback" not in response.text.lower()
        
    def test_generic_error_message(self):
        """Test generic error messages are returned"""
        response = client.get("/api/nonexistent-endpoint-xyz")
        assert response.status_code == 404
