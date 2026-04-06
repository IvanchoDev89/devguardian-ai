import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

# Must import app AFTER setting up test database
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

# Import Base and models before creating tables
from app.core.database import Base, get_db
from app.models.models import User, RefreshToken, PasswordResetToken, Scan, Vulnerability  # noqa

# Create tables
Base.metadata.create_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


from app.main import app
app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def client():
    # Clean tables before each test
    with test_engine.connect() as conn:
        for table in reversed(Base.metadata.sorted_tables):
            conn.execute(table.delete())
        conn.commit()
    yield TestClient(app)


@pytest.fixture(scope="function")
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


class TestHealth:
    def test_health_check(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


class TestAuth:
    def test_register(self, client):
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123",
                "full_name": "Test User"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["email"] == "test@example.com"
        assert data["username"] == "testuser"
        assert data["is_active"] == True

    def test_register_duplicate_email(self, client):
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser1",
                "password": "testpass123"
            }
        )
        response = client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser2",
                "password": "testpass123"
            }
        )
        assert response.status_code == 400
        assert "already registered" in response.json()["detail"]

    def test_login(self, client):
        # Register first
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123"
            }
        )
        
        # Login
        response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert "refresh_token" in data
        assert data["token_type"] == "bearer"

    def test_login_invalid_credentials(self, client):
        response = client.post(
            "/api/auth/login",
            data={
                "username": "wrong@example.com",
                "password": "wrongpass"
            }
        )
        assert response.status_code == 401

    def test_get_me(self, client):
        # Register and login
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123"
            }
        )
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123"
            }
        )
        token = login_response.json()["access_token"]
        
        # Get me
        response = client.get(
            "/api/auth/me",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert response.json()["email"] == "test@example.com"

    def test_refresh_token(self, client):
        # Register and login
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123"
            }
        )
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123"
            }
        )
        refresh_token = login_response.json()["refresh_token"]
        
        # Refresh
        response = client.post(
            "/api/auth/refresh",
            json={"refresh_token": refresh_token}
        )
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert "refresh_token" in response.json()


class TestVulnerabilities:
    def get_token(self, client):
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123"
            }
        )
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123"
            }
        )
        return login_response.json()["access_token"]

    def test_create_vulnerability(self, client):
        token = self.get_token(client)
        response = client.post(
            "/api/vulnerabilities",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "SQL Injection",
                "description": "SQL injection vulnerability",
                "severity": "critical",
                "cwe_id": "CWE-89"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "SQL Injection"
        assert data["severity"] == "critical"
        assert data["status"] == "open"

    def test_list_vulnerabilities(self, client):
        token = self.get_token(client)
        
        # Create some vulnerabilities
        for i in range(3):
            client.post(
                "/api/vulnerabilities",
                headers={"Authorization": f"Bearer {token}"},
                json={
                    "title": f"Vuln {i}",
                    "description": f"Description {i}",
                    "severity": "medium"
                }
            )
        
        response = client.get(
            "/api/vulnerabilities",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert len(response.json()) == 3

    def test_filter_vulnerabilities_by_severity(self, client):
        token = self.get_token(client)
        
        client.post(
            "/api/vulnerabilities",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Critical Vuln", "description": "Desc", "severity": "critical"}
        )
        client.post(
            "/api/vulnerabilities",
            headers={"Authorization": f"Bearer {token}"},
            json={"title": "Low Vuln", "description": "Desc", "severity": "low"}
        )
        
        response = client.get(
            "/api/vulnerabilities?severity=critical",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert len(response.json()) == 1
        assert response.json()[0]["severity"] == "critical"

    def test_update_vulnerability(self, client):
        token = self.get_token(client)
        
        create_response = client.post(
            "/api/vulnerabilities",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "Original Title",
                "description": "Original Desc",
                "severity": "high"
            }
        )
        vuln_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/vulnerabilities/{vuln_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"status": "resolved"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "resolved"

    def test_delete_vulnerability(self, client):
        token = self.get_token(client)
        
        create_response = client.post(
            "/api/vulnerabilities",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "title": "To Delete",
                "description": "Will be deleted",
                "severity": "low"
            }
        )
        vuln_id = create_response.json()["id"]
        
        response = client.delete(
            f"/api/vulnerabilities/{vuln_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        
        # Verify deleted
        get_response = client.get(
            f"/api/vulnerabilities/{vuln_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert get_response.status_code == 404

    def test_vulnerability_stats(self, client):
        token = self.get_token(client)
        
        for severity in ["critical", "high", "medium", "low"]:
            client.post(
                "/api/vulnerabilities",
                headers={"Authorization": f"Bearer {token}"},
                json={"title": f"{severity} Vuln", "description": "Desc", "severity": severity}
            )
        
        response = client.get(
            "/api/vulnerabilities/stats/summary",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 4
        assert data["by_severity"]["critical"] == 1


class TestScans:
    def get_token(self, client):
        client.post(
            "/api/auth/register",
            json={
                "email": "test@example.com",
                "username": "testuser",
                "password": "testpass123"
            }
        )
        login_response = client.post(
            "/api/auth/login",
            data={
                "username": "test@example.com",
                "password": "testpass123"
            }
        )
        return login_response.json()["access_token"]

    def test_create_scan(self, client):
        token = self.get_token(client)
        response = client.post(
            "/api/scans",
            headers={"Authorization": f"Bearer {token}"},
            json={
                "name": "My First Scan",
                "scan_type": "code",
                "target": "https://example.com"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "My First Scan"
        assert data["status"] == "pending"

    def test_list_scans(self, client):
        token = self.get_token(client)
        
        for i in range(2):
            client.post(
                "/api/scans",
                headers={"Authorization": f"Bearer {token}"},
                json={"name": f"Scan {i}", "scan_type": "code"}
            )
        
        response = client.get(
            "/api/scans",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert len(response.json()) == 2

    def test_update_scan_status(self, client):
        token = self.get_token(client)
        
        create_response = client.post(
            "/api/scans",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "Test Scan", "scan_type": "code"}
        )
        scan_id = create_response.json()["id"]
        
        response = client.put(
            f"/api/scans/{scan_id}",
            headers={"Authorization": f"Bearer {token}"},
            json={"status": "completed"}
        )
        assert response.status_code == 200
        assert response.json()["status"] == "completed"

    def test_scan_stats(self, client):
        token = self.get_token(client)
        
        client.post(
            "/api/scans",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "Scan 1", "scan_type": "code"}
        )
        client.post(
            "/api/scans",
            headers={"Authorization": f"Bearer {token}"},
            json={"name": "Scan 2", "scan_type": "secrets"}
        )
        
        response = client.get(
            "/api/scans/stats/summary",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["total"] == 2
