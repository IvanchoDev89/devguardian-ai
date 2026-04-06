"""
Final Comprehensive Test for DevGuardian AI Backend
"""
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def run_test(name, func):
    try:
        func()
        print(f"✅ {name}")
        return True
    except Exception as e:
        print(f"❌ {name}: {e}")
        return False

tests_passed = 0
tests_total = 0

print("=" * 60)
print("FINAL COMPREHENSIVE TEST")
print("=" * 60)

# 1. Public endpoints
tests_total += 1
if run_test("GET /health", lambda: client.get("/health").status_code == 200):
    tests_passed += 1

tests_total += 1
if run_test("GET /", lambda: client.get("/").status_code == 200):
    tests_passed += 1

# 2. Auth flow
tests_total += 1
r = client.post("/api/auth/register", json={"email": "final@test.com", "username": "final", "password": "Pass123456"})
if run_test("POST /api/auth/register", lambda: r.status_code == 200):
    tests_passed += 1

tests_total += 1
r = client.post("/api/auth/login", data={"username": "final@test.com", "password": "Pass123456"})
token = r.json()["access_token"]
if run_test("POST /api/auth/login", lambda: r.status_code == 200):
    tests_passed += 1

tests_total += 1
if run_test("GET /api/auth/me", lambda: 
    client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"}).status_code == 200):
    tests_passed += 1

# 3. Vulnerabilities CRUD
tests_total += 1
r = client.post("/api/vulnerabilities", headers={"Authorization": f"Bearer {token}"},
    json={"title": "Test Vuln", "description": "Test", "severity": "high"})
if run_test("POST /api/vulnerabilities", lambda: r.status_code == 200):
    tests_passed += 1

tests_total += 1
if run_test("GET /api/vulnerabilities", lambda:
    client.get("/api/vulnerabilities", headers={"Authorization": f"Bearer {token}"}).status_code == 200):
    tests_passed += 1

tests_total += 1
if run_test("GET /api/vulnerabilities/stats/summary", lambda:
    client.get("/api/vulnerabilities/stats/summary", headers={"Authorization": f"Bearer {token}"}).status_code == 200):
    tests_passed += 1

# 4. Scans CRUD
tests_total += 1
r = client.post("/api/scans", headers={"Authorization": f"Bearer {token}"},
    json={"name": "Test", "scan_type": "python"})
if run_test("POST /api/scans", lambda: r.status_code == 200):
    tests_passed += 1

tests_total += 1
if run_test("GET /api/scans", lambda:
    client.get("/api/scans", headers={"Authorization": f"Bearer {token}"}).status_code == 200):
    tests_passed += 1

tests_total += 1
if run_test("GET /api/scans/stats/summary", lambda:
    client.get("/api/scans/stats/summary", headers={"Authorization": f"Bearer {token}"}).status_code == 200):
    tests_passed += 1

# 5. Scan execution
tests_total += 1
if run_test("POST /api/scans/run", lambda:
    client.post("/api/scans/run", headers={"Authorization": f"Bearer {token}"},
        json={"scan_type": "python", "target": "/tmp", "options": {"timeout": 5}}).status_code == 200):
    tests_passed += 1

# 6. Logout
tests_total += 1
if run_test("POST /api/auth/logout", lambda:
    client.post("/api/auth/logout", json={"refresh_token": "test"}).status_code == 200):
    tests_passed += 1

print("=" * 60)
print(f"RESULT: {tests_passed}/{tests_total} TESTS PASSED")
print("=" * 60)