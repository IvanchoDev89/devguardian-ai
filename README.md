# DevGuardian AI

A code security scanner with pattern-based detection for common vulnerabilities.

## ⚠️ Honest Assessment

**This is a code quality tool, NOT a security product.**
- Uses pattern matching (regex), not security analysis
- Will miss most real vulnerabilities (business logic, IDOR, auth bypass, etc.)
- For educational purposes and basic hygiene only
- Do NOT rely on this for actual security assessments

## Features

- **Pattern Detection**: Detects common issues like hardcoded passwords, obvious SQLi
- **Quick Scanner**: Fast code scanning
- **Multiple Languages**: Python, JavaScript, TypeScript, Java, PHP, Go, Rust, C#
- **Rate Limiting**: Prevents abuse
- **Audit Logging**: Tracks scan activity

## 🏗️ Architecture

### Services
- **Vue 3 + TypeScript Frontend** (Port 3000)
- **Python AI Service** (FastAPI - Port 8000)
- **Laravel API Backend** (PHP 8.3 + Octane - Port 8001) - Optional for MVP

### Key Components
- **Vulnerability Scanner**: Pattern-matching + AI analysis
- **LLM Analyzer**: OpenAI, Claude, or Ollama integration for fix suggestions
- **Vue 3 SPA**: Modern responsive frontend

## 📋 Prerequisites

- Node.js 18+
- Python 3.11+
- (Optional) Docker for Laravel backend

## 🛠️ Installation

### 1. Clone Repository
```bash
git clone <repository-url>
cd devguardian-ai
```

### 2. Start AI Service (Required)
```bash
cd ai-service

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start the server
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 3. Start Frontend
```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application
- **Frontend**: http://localhost:3000
- **Scan Page**: http://localhost:3000/scan
- **AI Service API**: http://localhost:8000

## 🚀 Quick Start

1. **Access the Application**: Open http://localhost:3000
2. **Go to Scanner**: Click "Scan" in the navigation or visit /scan
3. **Paste Code**: Enter your code to analyze
4. **View Results**: See vulnerabilities and security score
5. **Get AI Fixes**: Click "AI Fix" for remediation suggestions

## 📊 Usage

### API Usage
```bash
# Health check
curl http://localhost:8000/api/v1/health

# Analyze code
curl -X POST http://localhost:8000/api/v1/analyze-code \
  -H "Content-Type: application/json" \
  -d '{"code": "password = \"secret123\"", "language": "python"}'

# AI analysis (requires OpenAI/Claude API key)
curl -X POST http://localhost:8000/api/llm/analyze \
  -H "Content-Type: application/json" \
  -d '{"vulnerability": {"type": "sql_injection", "severity": "critical"}, "code_snippet": "...", "language": "python"}'
```

## 🔧 Configuration

### Frontend (.env)
```env
VITE_API_BASE_URL=http://localhost:8001/api
VITE_AI_SERVICE_URL=http://localhost:8000
```

### AI Service (.env)
```env
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info

# Optional: OpenAI API
OPENAI_API_KEY=sk-...

# Optional: Claude API
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Ollama (local AI)
OLLAMA_BASE_URL=http://localhost:11434
```

## 🧪 Testing

### AI Service Tests
```bash
cd ai-service
source venv/bin/activate
pytest tests/ -v
```

### Frontend Tests
```bash
cd frontend
npm run test
```

## 🔒 Security - Detected Vulnerabilities

The scanner detects:
- **SQL Injection** - String concatenation in queries
- **Hardcoded Passwords** - Credentials in source code
- **Hardcoded API Keys** - Secrets and tokens
- **XSS** - Cross-site scripting patterns
- **Command Injection** - Unsafe system calls
- **Weak Cryptography** - MD5, SHA1 usage
- **Path Traversal** - Unsafe file operations
- **Insecure Deserialization** - Pickle/YAML loading

## 📈 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/health` | GET | Service health check |
| `/api/v1/analyze-code` | POST | Analyze code for vulnerabilities |
| `/api/v1/languages` | GET | Get supported languages |
| `/api/llm/analyze` | POST | AI-powered vulnerability analysis |
| `/api/llm/fix` | POST | Generate fix suggestions |
| `/api/llm/health` | GET | LLM service health |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Issues**: [GitHub Issues](https://github.com/IvanchoDev89/devguardian-ai/issues)

## 🎯 Roadmap

- [x] Basic vulnerability scanner (MVP)
- [x] Web interface with scan page
- [ ] Database integration for scan history
- [ ] User authentication
- [ ] Repository scanning
- [ ] Advanced AI models for fix generation

---

Built with ❤️ by DevGuardian AI Team
