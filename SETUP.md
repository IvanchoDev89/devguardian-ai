# DevGuardian AI - Local Development Setup

This guide covers setting up the MVP vulnerability scanner for local development.

## Prerequisites

- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PHP 8.3+

## Quick Start (MVP Only)

### 1. Start AI Service

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

### 2. Verify API is Running

```bash
curl http://localhost:8000/api/v1/health
# Expected: {"status":"ok","timestamp":"...","service":"DevGuardian Vulnerability Scanner","version":"1.0.0"}
```

### 3. Test the Vulnerability Scanner

```bash
# Analyze code for vulnerabilities
curl -X POST http://localhost:8000/api/v1/analyze-code \
  -H "Content-Type: application/json" \
  -d '{"code": "password = \"mysecret123\"", "language": "python"}'
```

### 4. Start Frontend (Optional)

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

### Health Check
```
GET /api/v1/health
```

### Analyze Code
```
POST /api/v1/analyze-code
Content-Type: application/json

{
  "code": "string (max 10KB)",
  "language": "python|javascript|typescript|java|csharp|php|ruby|go|rust|c|cpp"
}
```

### Get Supported Languages
```
GET /api/v1/languages
```

## Supported Vulnerabilities

The scanner detects:
- SQL Injection
- Hardcoded Passwords/API Keys
- XSS (Cross-Site Scripting)
- Command Injection
- Weak Cryptography (MD5, SHA1)
- Insecure Deserialization
- Path Traversal
- And more...

## Running Tests

```bash
cd ai-service
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_vulnerability_scanner.py -v
```

## Environment Variables

Create `.env` in `ai-service/`:

```env
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info
```

## Docker Deployment

```bash
# Build and run
docker-compose up -d ai-service

# Check logs
docker-compose logs -f ai-service
```

## Project Structure

```
devguardian-ai/
├── ai-service/
│   ├── app/
│   │   ├── scanners/
│   │   │   └── vulnerability_scanner.py  # Core scanner logic
│   │   └── api/
│   │       └── endpoints/
│   │           └── vulnerability_analyzer.py  # API endpoint
│   ├── tests/
│   │   ├── test_vulnerability_scanner.py
│   │   └── test_api.py
│   ├── main.py
│   └── requirements.txt
├── frontend/
│   └── src/
│       ├── components/
│       │   ├── CodeInput.vue
│       │   └── ResultsDisplay.vue
│       ├── pages/
│       │   └── ScanPage.vue
│       └── services/
│           └── api.ts
└── README.md
```

## Troubleshooting

### Import Errors
Ensure you're running from the correct directory and virtual environment is activated.

### Port Already in Use
Kill existing process:
```bash
lsof -ti:8000 | xargs kill -9
```

### Tests Failing
Ensure all dependencies are installed:
```bash
pip install pytest pytest-asyncio
```

## Next Steps

1. ✅ Basic vulnerability scanner (MVP) - DONE
2. Database integration for storing scan history
3. User authentication
4. Repository scanning
5. AI-powered fix suggestions
