# DevGuardian AI Backend

FastAPI-based REST API backend for the DevGuardian AI security vulnerability scanner.

## Overview

This backend provides:
- JWT-based authentication with refresh tokens
- CRUD operations for vulnerabilities and scans
- Multi-tool security scanning engine
- PostgreSQL database integration

## Tech Stack

- **Framework**: FastAPI (Python 3.11+)
- **ORM**: SQLAlchemy
- **Database**: PostgreSQL
- **Authentication**: JWT with access/refresh tokens

## Quick Start

### 1. Install Dependencies

```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your database credentials:

```bash
DATABASE_URL=postgresql://user:password@localhost:5433/devguardian
SECRET_KEY=your-secret-key
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

### 3. Start Server

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

Database tables are created automatically on first run.

## API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login` | POST | Login (returns tokens) |
| `/api/auth/refresh` | POST | Refresh access token |
| `/api/auth/logout` | POST | Logout (revoke token) |
| `/api/auth/me` | GET | Get current user |
| `/api/auth/request-password-reset` | POST | Request password reset |
| `/api/auth/reset-password` | POST | Reset password |

### Vulnerabilities

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/vulnerabilities` | GET | List vulnerabilities |
| `/api/vulnerabilities` | POST | Create vulnerability |
| `/api/vulnerabilities/{id}` | GET | Get vulnerability |
| `/api/vulnerabilities/{id}` | PUT | Update vulnerability |
| `/api/vulnerabilities/{id}` | DELETE | Delete vulnerability |
| `/api/vulnerabilities/stats/summary` | GET | Get statistics |

### Scans

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scans` | GET | List scans |
| `/api/scans` | POST | Create scan |
| `/api/scans/{id}` | GET | Get scan |
| `/api/scans/{id}` | PUT | Update scan |
| `/api/scans/{id}` | DELETE | Delete scan |
| `/api/scans/stats/summary` | GET | Get statistics |
| `/api/scans/run` | POST | Run security scan |

### Health

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/` | API | OpenAPI info |

## Security Scanning

The scanning engine integrates multiple security tools:

- **Semgrep**: Multi-language static analysis
- **Bandit**: Python security issues
- **gosec**: Go security vulnerabilities
- **Gitleaks**: Secrets detection
- **pip-audit**: Python dependencies
- **npm audit**: JavaScript dependencies
- **Trivy**: Docker container scanning

### Example: Run a Scan

```bash
# Login
TOKEN=$(curl -s -X POST http://127.0.0.1:8002/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=user@example.com&password=password" \
  | jq -r '.access_token')

# Run scan
curl -X POST http://127.0.0.1:8002/api/scans/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"scan_type": "python", "target": "/path/to/code"}'
```

## Testing

```bash
python -m pytest tests/ -v
```

## Docker

```bash
docker build -t devguardian-backend .
docker run -p 8002:8002 devguardian-backend
```