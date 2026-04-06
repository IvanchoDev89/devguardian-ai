# DevGuardian AI 🛡️

Enterprise-grade AI-powered security vulnerability scanner with real SAST tools integration.

## 🚀 Features

### Core Security Scanning
- **Real SAST Tools**: Semgrep + Bandit + gosec + Gitleaks + Trivy
- **Multi-Language Support**: Python, JavaScript, Go, Docker
- **Repository Scanning**: Clone and scan GitHub, GitLab, Bitbucket repositories
- **Dependency Scanning**: pip-audit, npm audit
- **Docker/K8s Security**: Scan Dockerfiles and Kubernetes configs
- **Secrets Detection**: Hardcoded API keys, passwords, tokens

### User Management
- **JWT Authentication**: Secure login/signup with access + refresh tokens
- **Password Reset**: Secure password recovery flow
- **Rate Limiting**: Prevent abuse

### REST API Backend (FastAPI)
- Full CRUD for vulnerabilities and scans
- Multi-tool security scanning engine
- PostgreSQL database
- Comprehensive stats and analytics

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                    Vue 3 Frontend (Port 3000)                      │
│              (Dashboard, Scanner, Vulnerabilities)                   │
└────────────────────────────┬──────────────────────────────────────┘
                             │ HTTP
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│                    FastAPI Backend (Port 8002)                    │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ API Endpoints                                               │   │
│  │ • /api/auth/* - Authentication (JWT + Refresh)              │   │
│  │ • /api/vulnerabilities/* - CRUD + Stats                    │   │
│  │ • /api/scans/* - CRUD                                     │   │
│  │ • /api/scans/run - Multi-tool Scanner                     │   │
│  └─────────────────────────────────────────────────────────────┘   │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │ Scanning Engine                                            │   │
│  │ • Semgrep - Multi-language static analysis                 │   │
│  │ • Bandit - Python security                                │   │
│  │ • gosec - Go security                                     │   │
│  │ • Gitleaks - Secrets detection                             │   │
│  │ • pip-audit - Python dependencies                         │   │
│  │ • npm audit - JavaScript dependencies                     │   │
│  │ • Trivy - Docker container scanning                       │   │
│  └─────────────────────────────────────────────────────────────┘   │
└────────────────────────────┬──────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────┐
│              PostgreSQL Database (Port 5433)                       │
│  Tables: users, vulnerabilities, scans, refresh_tokens,            │
│           password_reset_tokens                                   │
└─────────────────────────────────────────────────────────────────────┘
```

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- PostgreSQL 16+
- Docker (optional)

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/devguardian-ai/devguardian-ai.git
cd devguardian-ai
```

### 2. Backend Setup
```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your PostgreSQL credentials

# Start server (creates tables automatically)
uvicorn app.main:app --host 127.0.0.1 --port 8002
```

### 3. Frontend Setup
```bash
cd frontend
npm install
npm run dev
```

### 4. Docker (Optional)
```bash
# With PostgreSQL
docker-compose -f docker-compose.dev.yml up -d
```

## 📡 API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login` | POST | Login (returns access + refresh tokens) |
| `/api/auth/refresh` | POST | Refresh access token |
| `/api/auth/logout` | POST | Revoke refresh token |
| `/api/auth/me` | GET | Get current user profile |
| `/api/auth/request-password-reset` | POST | Request password reset |
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
| `/api/scans` | GET | List scans |
| `/api/scans` | POST | Create scan |
| `/api/scans/{id}` | GET | Get scan details |
| `/api/scans/{id}` | PUT | Update scan |
| `/api/scans/{id}` | DELETE | Delete scan |
| `/api/scans/stats/summary` | GET | Get scan statistics |
| `/api/scans/run` | POST | **Execute security scan** |

### Health
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check |
| `/` | GET | API information |

## 🔍 Scanning Engine

### Supported Scan Types
| Type | Tools Used | Description |
|------|------------|-------------|
| `all` | All tools | Complete security scan |
| `python` | Semgrep, Bandit, gosec | Python code analysis |
| `javascript` | Semgrep, npm audit | JavaScript/TypeScript |
| `go` | gosec, Semgrep | Go code analysis |
| `secrets` | Gitleaks, Regex | Hardcoded secrets detection |
| `dependencies` | pip-audit, npm audit | Vulnerable dependencies |
| `docker` | Trivy | Container scanning |

### Example: Execute a Scan
```bash
# Login and get token
TOKEN=$(curl -s -X POST http://127.0.0.1:8002/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=Pass123456" \
  | jq -r '.access_token')

# Run a Python security scan
curl -X POST http://127.0.0.1:8002/api/scans/run \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "scan_type": "python",
    "target": "/path/to/your/code",
    "options": {
      "timeout": 120,
      "rules": "p/owasp-top-ten"
    }
  }'
```

## Environment Variables

### Backend (.env)
```env
# Database (PostgreSQL)
DATABASE_URL=postgresql://devguardian:devguardian_password@127.0.0.1:5433/devguardian_ai
USE_POSTGRES=true

# JWT
SECRET_KEY=your-super-secret-key-at-least-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Security
EMAIL_VERIFICATION_REQUIRED=false

# App
DEBUG=true
```

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8002
```

## 🎯 Quick Start

1. **Start Backend**: `cd backend && uvicorn app.main:app --host 127.0.0.1 --port 8002`
2. **Start Frontend**: `cd frontend && npm run dev`
3. **Access**: http://localhost:3000
4. **Register**: Create account at /signup
5. **Scan**: Navigate to /app/scan

## 🔒 Security Features

### Authentication
- JWT access tokens (30 min expiry)
- Refresh tokens (30 day expiry)
- Secure password hashing (bcrypt)
- Rate limiting (5 requests/minute)

### Detected Vulnerabilities
- **Code Injection**: SQL, Command, Code, XSS
- **Cryptography**: Weak algorithms, hardcoded keys
- **Authentication**: Hardcoded credentials
- **Dependencies**: Known CVEs

## 📊 Database Schema

```
users
├── id (PK)
├── email (unique)
├── username (unique)
├── hashed_password
├── full_name
├── is_active
├── is_superuser
├── verification_token
└── timestamps

vulnerabilities
├── id (PK)
├── title
├── description
├── severity (critical|high|medium|low)
├── status (open|in_progress|resolved|false_positive)
├── cwe_id
├── cvss_score
├── file_path
├── line_number
├── code_snippet
├── fix_suggestion
├── owner_id (FK)
├── scan_id (FK, nullable)
└── timestamps

scans
├── id (PK)
├── name
├── scan_type
├── status (pending|running|completed|failed)
├── target
├── results (JSON)
├── owner_id (FK)
├── created_at
└── completed_at

refresh_tokens / password_reset_tokens
├── id (PK)
├── token (hashed)
├── user_id (FK)
├── expires_at
└── created_at
```

## 🧪 Testing

```bash
# Run all tests
cd backend
PYTHONPATH=. python3 -m pytest tests/ -v

# Run specific test file
PYTHONPATH=. python3 -m pytest tests/test_api.py -v
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ by DevGuardian AI Team