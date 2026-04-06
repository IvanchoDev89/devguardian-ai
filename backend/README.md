# DevGuardian Backend - FastAPI

## Stack
- **FastAPI** - API framework
- **SQLAlchemy** - ORM
- **PostgreSQL** - Database
- **Redis** - Cache
- **JWT** - Authentication

## Setup

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## API Endpoints

### Auth
- POST /api/auth/register
- POST /api/auth/login
- GET /api/auth/me

### Vulnerabilities
- GET /api/vulnerabilities
- POST /api/vulnerabilities
- GET /api/vulnerabilities/{id}
- PUT /api/vulnerabilities/{id}
- DELETE /api/vulnerabilities/{id}

### Scans
- POST /api/scans
- GET /api/scans
- GET /api/scans/{id}
