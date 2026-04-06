# DevGuardian AI 🛡️

Enterprise-grade AI-powered security vulnerability scanner with real SAST (Static Application Security Testing) tools integration.

## Overview

DevGuardian AI is a comprehensive security platform that identifies vulnerabilities in code repositories using industry-standard security tools. It provides a modern Vue 3 frontend with a FastAPI backend, storing data in PostgreSQL.

## Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Vue 3 Frontend (Port 3000)                      │
│              (Dashboard, Scanner, Vulnerabilities)                 │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Port 8002)                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ API Endpoints                                               │   │
│  │ • /api/auth/* - Authentication (JWT + Refresh Tokens)      │   │
│  │ • /api/vulnerabilities/* - CRUD + Statistics                │   │
│  │ • /api/scans/* - Scan Management                            │   │
│  │ • /api/scans/run - Multi-tool Scanner                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Scanning Engine                                            │   │
│  │ • Semgrep     - Multi-language static analysis             │   │
│  │ • Bandit      - Python security vulnerabilities             │   │
│  │ • gosec       - Go security vulnerabilities                  │   │
│  │ • Gitleaks    - Secrets/credentials detection               │   │
│  │ • pip-audit   - Python dependency vulnerabilities           │   │
│  │ • npm audit   - JavaScript dependency vulnerabilities      │   │
│  │ • Trivy       - Docker container image scanning             │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PostgreSQL Database (Port 5433)                       │
│  Tables: users, vulnerabilities, scans, refresh_tokens,          │
│          password_reset_tokens                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Vue 3 + TypeScript + Pinia |
| Backend | FastAPI (Python 3.11+) |
| Database | PostgreSQL |
| Authentication | JWT with Refresh Tokens |
| Security Tools | Semgrep, Bandit, gosec, Gitleaks, Trivy |

## Features

### Core Security Scanning
- **Multi-Language Support**: Python, JavaScript, Go, Docker
- **Real SAST Integration**: Industry-standard security tools
- **Repository Scanning**: Clone and scan GitHub, GitLab, Bitbucket repositories
- **Dependency Scanning**: pip-audit, npm audit for vulnerable dependencies
- **Docker Security**: Scan Dockerfiles and container images with Trivy
- **Secrets Detection**: Hardcoded API keys, passwords, tokens, and credentials

### User Management
- **JWT Authentication**: Secure login/signup with access + refresh tokens
- **Password Reset**: Secure password recovery flow
- **Rate Limiting**: Protection against abuse on authentication endpoints

### REST API Backend
- Full CRUD operations for vulnerabilities and scans
- Multi-tool security scanning engine
- Comprehensive statistics and analytics
- Pagination and filtering support

## Prerequisites

| Requirement | Version |
|-------------|---------|
| Node.js | 18+ |
| Python | 3.11+ |
| PostgreSQL | 16+ |
| Docker | Optional |

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/IvanchoDev89/devguardian-ai.git
cd devguardian-ai
```

### 2. Backend Setup (FastAPI)

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment variables
cp .env.example .env
# Edit .env with your PostgreSQL credentials:
# DATABASE_URL=postgresql://user:password@localhost:5433/devguardian
# SECRET_KEY=your-secret-key-here
# ACCESS_TOKEN_EXPIRE_MINUTES=30
# REFRESH_TOKEN_EXPIRE_DAYS=7

# Start the backend server
# Database tables are created automatically on first run
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

The backend will be available at `http://127.0.0.1:8002`

API documentation (Swagger UI): `http://127.0.0.1:8002/docs`

### 3. Frontend Setup (Vue 3)

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
# Create .env file:
# VITE_API_BASE_URL=http://127.0.0.1:8002

# Start development server
npm run dev
```

The frontend will be available at `http://localhost:3000`

### 4. Docker Setup (Optional)

For containerized deployment with PostgreSQL:

```bash
# Start all services
docker-compose -f docker-compose.dev.yml up -d

# View logs
docker-compose -f docker-compose.dev.yml logs -f backend
```

## Security Tools Installation

For full scanning capabilities, install the security tools:

```bash
# Python security - Bandit
pip install bandit

# Multi-language analysis - Semgrep
pip install semgrep
semgrep install

# Go security - gosec
go install github.com/securego/gosec/v2/cmd/gosec@latest

# Secrets detection - Gitleaks
# Download from: https://github.com/gitleaks/gitleaks/releases

# Container scanning - Trivy
# Download from: https://github.com/aquasecurity/trivy/releases

# Python dependencies - pip-audit
pip install pip-audit

# JavaScript dependencies - npm audit (included with Node.js)
npm audit
```

## API Endpoints

### Authentication

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login` | POST | Login (returns access + refresh tokens) |
| `/api/auth/refresh` | POST | Refresh access token |
| `/api/auth/logout` | POST | Revoke refresh token |
| `/api/auth/me` | GET | Get current user profile |
| `/api/auth/request-password-reset` | POST | Request password reset email |
| `/api/auth/reset-password` | POST | Reset password with token |

### Vulnerabilities

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/vulnerabilities` | GET | List vulnerabilities (paginated) |
| `/api/vulnerabilities` | POST | Create vulnerability |
| `/api/vulnerabilities/{id}` | GET | Get vulnerability details |
| `/api/vulnerabilities/{id}` | PUT | Update vulnerability |
| `/api/vulnerabilities/{id}` | DELETE | Delete vulnerability |
| `/api/vulnerabilities/stats/summary` | GET | Get vulnerability statistics |

### Scans

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/scans` | GET | List scans (paginated) |
| `/api/scans` | POST | Create new scan |
| `/api/scans/{id}` | GET | Get scan details |
| `/api/scans/{id}` | PUT | Update scan |
| `/api/scans/{id}` | DELETE | Delete scan |
| `/api/scans/stats/summary` | GET | Get scan statistics |
| `/api/scans/run` | POST | Execute security scan |

### Health

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/` | GET | API information |

## Scanning Engine

### Supported Scan Types

| Type | Tools Used | Description |
|------|-------------|-------------|
| `all` | All tools | Complete security scan |
| `python` | Semgrep, Bandit, gosec | Python code analysis |
| `javascript` | Semgrep, npm audit | JavaScript/TypeScript |
| `go` | gosec, Semgrep | Go code analysis |
| `secrets` | Gitleaks, Regex | Hardcoded secrets detection |
| `dependencies` | pip-audit, npm audit | Vulnerable dependencies |
| `docker` | Trivy | Container scanning |

### Example: Execute a Security Scan

```bash
# Step 1: Login and get access token
TOKEN=$(curl -s -X POST http://127.0.0.1:8002/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=YourPassword123" \
  | jq -r '.access_token')

# Step 2: Run a Python security scan
curl -X POST http://127.0.0.1:8002/api/scans/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scan_type": "python",
    "target": "/path/to/your/python/code"
  }'

# Step 3: Get scan results
curl -H "Authorization: Bearer $TOKEN" \
  http://127.0.0.1:8002/api/scans/1
```

### Scan Response Format

```json
{
  "id": 1,
  "name": "Python Scan",
  "scan_type": "python",
  "status": "completed",
  "target": "/path/to/code",
  "results": {
    "semgrep": {
      "vulnerabilities": [...],
      "summary": { "high": 3, "medium": 5, "low": 2 }
    },
    "bandit": {
      "issues": [...],
      "confidence": "HIGH"
    }
  },
  "vulnerabilities_found": 10,
  "created_at": "2026-04-06T12:00:00Z",
  "completed_at": "2026-04-06T12:05:00Z"
}
```

## Environment Variables

### Backend (.env)

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5433/devguardian

# Security
SECRET_KEY=your-super-secret-key-change-in-production
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
ALGORITHM=HS256

# Server
HOST=127.0.0.1
PORT=8002
```

### Frontend (.env)

```bash
VITE_API_BASE_URL=http://127.0.0.1:8002
```

## Project Structure

```
devguardian-ai/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/endpoints/     # API route handlers
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── vulnerabilities.py
│   │   │   ├── scans.py
│   │   │   └── scanning.py    # Security scanning engine
│   │   ├── core/              # Core functionality
│   │   │   ├── config.py      # Settings
│   │   │   ├── database.py    # Database connection
│   │   │   └── security.py    # JWT/password handling
│   │   └── models/            # Database models & schemas
│   ├── tests/                 # Backend tests
│   ├── Dockerfile             # Container image
│   ├── requirements.txt       # Python dependencies
│   └── .env.example           # Environment template
│
├── frontend/                   # Vue 3 frontend
│   ├── src/
│   │   ├── pages/             # Vue page components
│   │   ├── components/        # Reusable components
│   │   ├── stores/            # Pinia state management
│   │   ├── services/          # API client
│   │   └── styles.css         # Global styles
│   ├── package.json
│   └── vite.config.ts
│
├── docker-compose.dev.yml     # Docker configuration
├── README.md                   # This file
├── SETUP.md                   # Detailed setup guide
└── SECURITY.md                # Security policy
```

## Testing

### Backend Tests

```bash
cd backend
source venv/bin/activate
python -m pytest tests/ -v
```

### API Health Check

```bash
curl http://127.0.0.1:8002/health
# Expected: {"status":"ok"}
```

## Security Considerations

- All ports are bound to `127.0.0.1` for local development
- JWT tokens include expiration times
- Passwords are hashed (bcrypt/SHA256)
- Rate limiting on authentication endpoints
- CORS configured for frontend origin only

## License

MIT License - See LICENSE file for details

## Support

For issues and questions:
- GitHub Issues: https://github.com/IvanchoDev89/devguardian-ai/issues
- Security vulnerabilities: See SECURITY.md