# DevGuardian AI 🛡️

Enterprise-grade AI-powered security vulnerability scanner with real SAST tools integration.

## 🚀 Features

### Core Security Scanning
- **Real SAST Tools**: Semgrep + Bandit for accurate vulnerability detection
- **Multi-Language Support**: Python, JavaScript, TypeScript, Java, PHP, Go, Rust, C#, Ruby
- **Repository Scanning**: Clone and scan GitHub, GitLab, Bitbucket repositories
- **Dependency Scanning**: npm audit, pip-audit, bundle-audit
- **Docker/K8s Security**: Scan Dockerfiles and Kubernetes configs

### User Management
- **JWT Authentication**: Secure login/signup with access + refresh tokens
- **Free Trial**: 3 free scans for new users
- **API Keys**: Programmatic access with quota management
- **Webhooks**: Real-time notifications on scan completion
- **Teams**: Collaborate with team members

### Enterprise Features
- **Rate Limiting**: Prevent abuse
- **Audit Logging**: Complete activity tracking
- **Admin Dashboard**: System-wide statistics
- **Security Reports**: PDF export functionality

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Vue 3 Frontend                        │
│              (http://localhost:3001)                     │
└─────────────────────┬───────────────────────────────────┘
                      │
        ┌─────────────┴─────────────┐
        ▼                           ▼
┌───────────────────┐    ┌───────────────────────┐
│   FastAPI Backend │    │   Real Security Scanner│
│   (Port 8003)     │    │   - Semgrep           │
│                   │    │   - Bandit            │
│   - Auth          │    │   - Dependency Check │
│   - API Keys      │    └───────────────────────┘
│   - Webhooks      │
│   - Teams         │
│   - Scan History  │
└───────────────────┘
```

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- SQLite (included)
- Optional: Docker

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone https://github.com/IvanchoDev89/devguardian-ai.git
cd devguardian-ai
```

### 2. Start Backend (AI Service)
```bash
cd ai-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start server
uvicorn main:app --host 0.0.0.0 --port 8003
```

### 3. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:3001
- **Scanner**: http://localhost:3001/scan
- **Repositories**: http://localhost:3001/repositories
- **Admin**: http://localhost:3001/admin
- **API**: http://localhost:8003

## 🎯 Quick Start

1. **Register**: Create an account at http://localhost:3001/signup
2. **Scan Code**: Go to /scan, paste your code
3. **View Results**: See vulnerabilities with severity scores
4. **Get AI Fixes**: Click "Get AI Fix Suggestions"
5. **Scan Repos**: Visit /repositories to scan GitHub/GitLab repos

## 📊 API Endpoints

### Authentication
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Register new user |
| `/api/auth/login` | POST | Login |
| `/api/auth/me` | GET | Get current user |
| `/api/auth/refresh` | POST | Refresh token |
| `/api/auth/free-trial-status` | GET | Get free trial info |

### Security Scanner
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/security/scanner/status` | GET | Check available tools |
| `/api/v1/security/scan/code` | POST | Scan code (Real SAST) |
| `/api/v1/security/scan/repository` | POST | Scan repository |
| `/api/v1/security/scans` | GET | List scans |
| `/api/v1/security/scans/{id}` | GET | Get scan details |
| `/api/v1/security/admin/stats` | GET | Admin statistics |

### Legacy Scanner
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/analyze-code` | POST | Basic code analysis |
| `/api/v1/scans` | GET | Scan history |
| `/api/v1/scans/{id}` | GET | Scan details |

### Management
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/keys` | GET/POST | API Keys |
| `/api/webhooks` | GET/POST | Webhooks |
| `/api/teams/teams` | GET/POST | Teams |

## 🔧 Environment Variables

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8003
VITE_API_URL=http://localhost:8003/api
```

### Backend (.env)
```env
PORT=8003
HOST=0.0.0.0
LOG_LEVEL=info

# Database (SQLite - default)
DATABASE_URL=sqlite:///./devguardian.db

# Optional: OpenAI for AI fixes
OPENAI_API_KEY=sk-...

# Optional: Claude for AI analysis
ANTHROPIC_API_KEY=sk-ant-...
```

## 🧪 Testing

```bash
# Backend tests
cd ai-service
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

## 🔒 Security Features

### Detected Vulnerabilities
- **Injection**: SQL, Command, Code, XSS
- **Cryptography**: Weak algorithms, hardcoded keys
- **Authentication**: Hardcoded credentials
- **Files**: Path traversal, unsafe deserialization
- **Processes**: Unsafe subprocess, shell=true
- **Containers**: Running as root, missing security contexts
- **Dependencies**: Known CVEs

### Security Best Practices Applied
- ✅ JWT with refresh tokens
- ✅ Password hashing (bcrypt)
- ✅ Rate limiting
- ✅ Audit logging
- ✅ Non-root containers
- ✅ Kubernetes security contexts

## 📈 Screenshots

### Scanner Page
Modern interface with:
- Code editor with syntax highlighting
- Real-time vulnerability detection
- Severity scoring (0-100)
- AI-powered fix suggestions

### Repository Scanner
- GitHub/GitLab/Bitbucket integration
- Full repository cloning
- Multi-tool scanning (Semgrep + Bandit)
- Dependency vulnerability detection

### Admin Dashboard
- System-wide statistics
- User management
- API key management
- Activity logs

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/IvanchoDev89/devguardian-ai/issues)
- **Documentation**: [Wiki](https://github.com/IvanchoDev89/devguardian-ai/wiki)

## 📄 License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with ❤️ by DevGuardian AI Team
