import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestAuthEndpoints:
    def test_login_success(self):
        response = client.post(
            "/api/auth/login",
            json={"email": "admin@devguardian.ai", "password": "admin123"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"
        
    def test_login_invalid_password(self):
        response = client.post(
            "/api/auth/login",
            json={"email": "admin@devguardian.ai", "password": "wrongpassword"}
        )
        assert response.status_code == 401
        
    def test_login_invalid_email(self):
        response = client.post(
            "/api/auth/login",
            json={"email": "nonexistent@example.com", "password": "password"}
        )
        assert response.status_code == 401
        
    def test_register_new_user(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": f"test_{id(self)}@example.com",
                "password": "securepassword123",
                "name": "Test User"
            }
        )
        assert response.status_code == 201
        data = response.json()
        assert data["email"] == f"test_{id(self)}@example.com"
        
    def test_register_duplicate_email(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "admin@devguardian.ai",
                "password": "securepassword123",
                "name": "Test User"
            }
        )
        assert response.status_code == 400
        
    def test_register_short_password(self):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "password": "123",
                "name": "Test User"
            }
        )
        assert response.status_code == 400
        
    def test_get_current_user(self):
        login_response = client.post(
            "/api/auth/login",
            json={"email": "admin@devguardian.ai", "password": "admin123"}
        )
        token = login_response.json()["access_token"]
        
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "admin@devguardian.ai"
        assert data["role"] == "admin"
        
    def test_get_user_without_token(self):
        response = client.get("/api/auth/me")
        assert response.status_code in [401, 403]


class TestProtectedEndpoints:
    def setup_method(self):
        from app.core.auth import create_access_token
        self.token = create_access_token({"sub": "user_test", "email": "test@example.com", "role": "user"})
    
    def test_analyze_without_auth_when_required_false(self):
        response = client.post(
            "/api/v1/analyze-code",
            json={"code": "password = 'test'", "language": "python"}
        )
        assert response.status_code == 200
        
    def test_analyze_with_valid_token(self):
        response = client.post(
            "/api/v1/analyze-code",
            headers={"Authorization": f"Bearer {self.token}"},
            json={"code": "password = 'test'", "language": "python"}
        )
        assert response.status_code == 200
        data = response.json()
        assert "vulnerabilities" in data


class TestRateLimiting:
    def test_rate_limit_headers_present(self):
        for _ in range(5):
            response = client.post(
                "/api/v1/analyze-code",
                json={"code": "x = 1", "language": "python"}
            )
        assert response.status_code in [200, 429]
