# DevGuardian AI - Local Development Setup

This guide covers setting up the MVP vulnerability scanner for local development.

## Prerequisites

- Node.js 18+
- Python 3.11+

## Quick Start

### 1. Start AI Service (Required)

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

### 3. Start Frontend

```bash
cd frontend
npm install
npm run dev
```

### 4. Access the Application

- **Frontend**: http://localhost:3000
- **Scan Page**: http://localhost:3000/scan

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
  "language": "python|javascript|typescript|java|csharp|php|go|rust"
}
```

### AI Analysis (requires API key)
```
POST /api/llm/analyze
Content-Type: application/json

{
  "vulnerability": {
    "type": "sql_injection",
    "severity": "critical",
    "message": "..."
  },
  "code_snippet": "string",
  "language": "python",
  "generate_fix": true
}
```

### Get Supported Languages
```
GET /api/v1/languages
```

## Environment Variables

### AI Service (.env)

Create `.env` in `ai-service/`:

```env
PORT=8000
HOST=0.0.0.0
LOG_LEVEL=info

# Optional: OpenAI API (for AI analysis)
OPENAI_API_KEY=sk-...

# Optional: Claude API (for AI analysis)
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Ollama (local AI)
OLLAMA_BASE_URL=http://localhost:11434
```

### Frontend (.env)

The frontend already has defaults configured:

```env
VITE_API_BASE_URL=http://localhost:8001/api
VITE_AI_SERVICE_URL=http://localhost:## Supported Vulnerabilities

The8000
```

 scanner detects:
- **SQL Injection** - String concatenation in queries
- **Hardcoded Passwords** - Credentials in source code
- **Hardcoded API Keys** - Secrets and tokens
- **XSS** - Cross-site scripting patterns
- **Command Injection** - Unsafe system calls
- **Weak Cryptography** - MD5, SHA1 usage
- **Path Traversal** - Unsafe file operations
- **Insecure Deserialization** - Pickle/YAML loading

## Running Tests

```bash
cd ai-service
source venv/bin/activate

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_vulnerability_scanner.py -v
```

## Project Structure

```
devguardian-ai/
├── README.md                 # Project overview
├── SETUP.md                  # This file
├── ai-service/               # Python FastAPI service
│   ├── main.py               # Application entry point
│   ├── requirements.txt      # Python dependencies
│   ├── app/
│   │   ├── scanners/
│   │   │   └── vulnerability_scanner.py  # Core scanner
│   │   ├── services/
│   │   │   └── llm_analyzer.py            # AI analysis
│   │   └── api/
│   │       └── endpoints/
│   │           ├── vulnerability_analyzer.py
│   │           └── llm_analyzer.py
│   └── tests/
│       ├── test_vulnerability_scanner.py
│       └── test_llm_analyzer.py
├── frontend/                 # Vue 3 frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── Landing.vue    # Home page
│   │   │   └── ScanPage.vue   # Scanner page
│   │   ├── components/
│   │   │   └── Navbar.vue
│   │   └── services/
│   │       └── api.ts
│   └── package.json
└── laravel-backend/         # Optional Laravel API (not required for MVP)
```

## Troubleshooting

### Port Already in Use
```bash
# Find process using port 8000
lsof -ti:8000

# Kill it
lsof -ti:8000 | xargs kill -9
```

### Import Errors
Ensure you're running from the correct directory and virtual environment is activated.

### Frontend not loading
Check the frontend is running on port 3000:
```bash
curl http://localhost:3000
```

### Tests Failing
Ensure all dependencies are installed:
```bash
pip install pytest pytest-asyncio httpx
```

## API Examples

### Basic Vulnerability Scan
```bash
curl -X POST http://localhost:8000/api/v1/analyze-code \
  -H "Content-Type: application/json" \
  -d '{"code": "password = \"mysecret123\"\nquery = f\"SELECT * FROM users WHERE id = {user_id}\"", "language": "python"}'
```

Response:
```json
{
  "vulnerabilities": [
    {
      "line_number": 1,
      "vulnerability_type": "Hardcoded Password",
      "severity": "critical",
      "description": "Hardcoded password detected. Use environment variables.",
      "cwe_id": "CWE-259"
    },
    {
      "line_number": 2,
      "vulnerability_type": "SQL Injection",
      "severity": "critical",
      "description": "SQL query built using string interpolation.",
      "cwe_id": "CWE-89"
    }
  ],
  "score": 60,
  "total_vulnerabilities": 2
}
```

### AI Analysis (requires API key)
```bash
curl -X POST http://localhost:8000/api/llm/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "vulnerability": {
      "type": "sql_injection",
      "severity": "critical",
      "message": "SQL query built using string interpolation"
    },
    "code_snippet": "query = f\"SELECT * FROM users WHERE id = {user_id}\"",
    "language": "python",
    "generate_fix": true
  }'
```

## Next Steps

1. ✅ Basic vulnerability scanner (MVP) - DONE
2. ✅ Web interface with scan page - DONE
3. [ ] Database integration for storing scan history
4. [ ] User authentication
5. [ ] Repository scanning
6. [ ] Advanced AI models for fix generation
