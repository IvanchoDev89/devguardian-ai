# DevGuardian AI - Local Development Setup

Complete setup guide for running DevGuardian AI locally.

## Architecture Overview

DevGuardian AI consists of two main components:

1. **Frontend** (Vue 3 + TypeScript) - Port 3000
2. **Backend** (FastAPI + PostgreSQL) - Port 8002

The previous Laravel backend and separate AI service have been deprecated. All functionality is now in the FastAPI backend.

## Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Node.js | 18+ | For frontend |
| Python | 3.11+ | For backend |
| PostgreSQL | 16+ | For database |
| Git | Any | For cloning |

### Optional: Security Tools

For full scanning capabilities, install:

```bash
# Bandit - Python security
pip install bandit

# Semgrep - Multi-language analysis
pip install semgrep

# gosec - Go security
go install github.com/securego/gosec/v2/cmd/gosec@latest

# Gitleaks - Secrets detection
# Download from: https://github.com/gitleaks/gitleaks/releases

# Trivy - Container scanning
# Download from: https://github.com/aquasecurity/trivy/releases
```

## Quick Start

### Step 1: Start PostgreSQL

**Option A: Docker**
```bash
docker run -d \
  --name devguardian-postgres \
  -e POSTGRES_DB=devguardian \
  -e POSTGRES_USER=devguardian \
  -e POSTGRES_PASSWORD=devguardian123 \
  -p 5433:5432 \
  postgres:16
```

**Option B: Local PostgreSQL**
```bash
# Create database
createdb -U postgres devguardian
# Or use pgAdmin/Adminer
```

### Step 2: Start Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate    # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your database URL:
# DATABASE_URL=postgresql://devguardian:devguardian123@localhost:5433/devguardian

# Start server
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

On first run, database tables are created automatically.

Verify backend is running:
```bash
curl http://127.0.0.1:8002/health
# {"status":"ok"}
```

API documentation: http://127.0.0.1:8002/docs

### Step 3: Start Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
# Create .env file:
echo "VITE_API_BASE_URL=http://127.0.0.1:8002" > .env

# Start development server
npm run dev
```

Frontend available at: http://localhost:3000

## Docker Deployment

For containerized deployment:

```bash
# Start all services (backend + PostgreSQL)
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f

# Stop services
docker-compose -f docker-compose.dev.yml down
```

## Testing the Setup

### 1. Register a User

```bash
curl -X POST http://127.0.0.1:8002/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@example.com",
    "username": "admin",
    "password": "Password123",
    "full_name": "Admin User"
  }'
```

### 2. Login

```bash
curl -X POST http://127.0.0.1:8002/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=Password123"
```

Response includes `access_token` and `refresh_token`.

### 3. Create a Vulnerability

```bash
TOKEN="your-access-token"

curl -X POST http://127.0.0.1:8002/api/vulnerabilities \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "SQL Injection",
    "description": "Unparameterized SQL query",
    "severity": "high",
    "status": "open",
    "file_path": "src/db/query.py",
    "cwe_id": "CWE-89"
  }'
```

### 4. Run a Security Scan

```bash
TOKEN="your-access-token"

curl -X POST http://127.0.0.1:8002/api/scans/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scan_type": "python",
    "target": "/path/to/your/code"
  }'
```

## Troubleshooting

### PostgreSQL Connection Error

```
sqlalchemy.exc.OperationalError: could not connect to server
```

**Solution**: Ensure PostgreSQL is running and the connection string in `.env` is correct.

### Port Already in Use

```
ERROR: bind: address already in use
```

**Solution**: Check if port 8002 is in use:
```bash
lsof -i :8002
# Kill the process or change port in .env
```

### Module Not Found

```
ModuleNotFoundError: No module named 'fastapi'
```

**Solution**: Activate the virtual environment:
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Frontend CORS Error

```
Access to fetch at 'http://127.0.0.1:8002' from origin 'http://localhost:3000' blocked by CORS policy
```

**Solution**: This should be handled by the backend. If persists, check CORS settings in `backend/app/core/config.py`.

## Environment Variables Reference

### Backend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | Required |
| `SECRET_KEY` | JWT signing key | Required |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration | 30 |
| `REFRESH_TOKEN_EXPIRE_DAYS` | Refresh token expiration | 7 |
| `ALGORITHM` | JWT algorithm | HS256 |
| `HOST` | Server host | 127.0.0.1 |
| `PORT` | Server port | 8002 |

### Frontend (.env)

| Variable | Description | Default |
|----------|-------------|---------|
| `VITE_API_BASE_URL` | Backend URL | http://127.0.0.1:8002 |

## Next Steps

- Review security tools installation for full scanning capabilities
- Explore the API at http://127.0.0.1:8002/docs
- Access the frontend dashboard at http://localhost:3000