# DevGuardian AI

A precision-focused AI-powered security platform with zero-noise vulnerability detection and automated fix generation.

## 🎯 Philosophy

**DevGuardian AI is a silent guardian.** It detects only real vulnerabilities. Precision > Coverage. No noise. No magic. No hype.

## 🚀 Features

- **Zero-Noise Detection**: Only reports exploitable vulnerabilities
- **AI-Powered Pentesting**: Advanced security testing with 0-day vulnerability detection
- **Super Admin Dashboard**: Enterprise-wide security monitoring and analytics
- **Precision SQL Injection Scanner**: Extreme accuracy for JavaScript/Node.js
- **Context-Aware Analysis**: Understands your code's actual risk
- **Real-time Dashboard**: Monitor security metrics without false positives
- **Developer-Friendly**: Clear explanations and actionable fixes
- **Automated Fix Generation**: AI-generated vulnerability fixes with one-click apply

## 🏗️ Architecture

### Services
- **Laravel API Backend** (PHP 8.3 + Octane + Swoole)
- **Python AI Service** (FastAPI + PyTorch + Transformers)
- **PostgreSQL + TimescaleDB** (Metrics and time-series data)
- **Redis Cluster** (Queue and caching)
- **Vue 3 + TypeScript Frontend**

### Key Components
- **Domain-Driven Design**: Clean architecture with proper separation of concerns
- **Hexagonal Architecture**: Ports and adapters pattern for testability
- **Event-Driven Processing**: Queue-based vulnerability processing
- **Microservices**: Scalable AI service with async processing

## 📋 Prerequisites

- Docker & Docker Compose
- Node.js 18+
- PHP 8.3+
- Python 3.11+

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd codesentinel
```

### 2. Environment Setup
```bash
# Copy environment files
cp laravel-backend/.env.example laravel-backend/.env
cp ai-service/.env.example ai-service/.env

# Generate application keys
cd laravel-backend
php artisan key:generate
```

### 3. Start Services with Docker
```bash
docker-compose up -d
```

### 4. Install Dependencies
```bash
# Laravel backend
cd laravel-backend
composer install
php artisan migrate
php artisan db:seed

# AI Service
cd ../ai-service
pip install -r requirements.txt

# Frontend
cd ../frontend
npm install
npm run build
```

### 5. Configure OAuth
Add your OAuth credentials to the `.env` files:
- GitHub OAuth App
- GitLab OAuth App
- Bitbucket OAuth App

## 🚀 Quick Start

1. **Access the Application**: Open `http://localhost` in your browser
2. **Connect Repositories**: Use the UI to connect your repositories
3. **Run Security Scans**: Trigger scans to detect vulnerabilities
4. **Review AI Fixes**: Examine AI-generated fixes and apply them

## 📊 Usage

### Scanning Repositories
```bash
# Manual scan
php artisan scan:repository <repository-id>

# Batch scan
php artisan scan:organization <organization-id>
```

### AI Service API
```bash
# Generate fix
curl -X POST http://localhost:8001/api/v1/generate-fix \
  -H "Content-Type: application/json" \
  -d @fix-request.json

# Validate fix
curl -X POST http://localhost:8001/api/v1/validate-fix \
  -H "Content-Type: application/json" \
  -d '{"fix_id": "fix-uuid"}'
```

## 🔧 Configuration

### Laravel Backend (.env)
```env
# Database
DB_CONNECTION=pgsql
DB_HOST=postgres
DB_DATABASE=devguardian
DB_USERNAME=devguardian
DB_PASSWORD=devguardian_password

# AI Service
AI_SERVICE_URL=http://ai-service:8000

# OAuth
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITLAB_CLIENT_ID=your_gitlab_client_id
GITLAB_CLIENT_SECRET=your_gitlab_client_secret

# Queue
QUEUE_CONNECTION=redis
```

### AI Service (.env)
```env
PORT=8000
HOST=0.0.0.0
REDIS_URL=redis://redis:6379
LOG_LEVEL=info
```

## 🧪 Testing

### Laravel Tests
```bash
cd laravel-backend
php artisan test
```

### AI Service Tests
```bash
cd ai-service
pytest
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 📈 Monitoring

### Health Checks
- Laravel: `http://localhost:8000/health`
- AI Service: `http://localhost:8001/health`
- PostgreSQL: `localhost:5432`
- Redis: `localhost:6379`

### Metrics
- Laravel Horizon: `http://localhost/horizon`
- Application metrics available at `/api/metrics`

## 🔒 Security

- **API Authentication**: Laravel Sanctum tokens
- **Webhook Verification**: Signature validation
- **Data Encryption**: Sensitive data encrypted at rest
- **Access Control**: Role-based permissions
- **Audit Logging**: Comprehensive security event tracking

## 🚀 Deployment

### Production Docker
```bash
docker-compose -f docker-compose.prod.yml up -d
```

### Kubernetes
```bash
kubectl apply -f kubernetes/
```

## 📚 API Documentation

- **Laravel API**: `http://localhost:8000/docs`
- **AI Service**: `http://localhost:8001/docs`

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: [docs.codesentinel.ai](https://docs.codesentinel.ai)
- **Issues**: [GitHub Issues](https://github.com/your-org/codesentinel/issues)
- **Discord**: [Join our Discord](https://discord.gg/codesentinel)

## 🎯 Roadmap

- [ ] Advanced ML models for fix generation
- [ ] Support for more programming languages
- [ ] Custom rule engine
- [ ] Advanced compliance reporting
- [ ] Mobile applications
- [ ] Enterprise SSO integration
- [ ] Advanced threat intelligence feeds

---

Built with ❤️ by CodeSentinel team
