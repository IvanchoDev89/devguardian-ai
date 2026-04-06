# Contributing to DevGuardian AI

Thank you for your interest in contributing to DevGuardian AI! This document provides guidelines and information for contributors.

## Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- Python 3.11+
- PostgreSQL 16+ (or use Docker)

### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Start PostgreSQL (via Docker or local installation)
4. Run backend: `cd backend && pip install -r requirements.txt && uvicorn app.main:app --port 8002`
5. Run frontend: `cd frontend && npm install && npm run dev`
6. Create a feature branch for your contribution

## Development Guidelines

### Code Style
- **Python (Backend)**: Follow PEP 8, use Black formatter
- **TypeScript/Vue (Frontend)**: Use ESLint and Prettier
- **YAML**: Use 2 spaces for indentation

### Commit Messages
Use conventional commit format:
- `feat:` for new features
- `fix:` for bug fixes
- `docs:` for documentation
- `style:` for code style changes
- `refactor:` for code refactoring
- `test:` for adding tests
- `chore:` for maintenance tasks

Example: `feat(backend): add vulnerability statistics endpoint`

### Testing
- Write tests for new features
- Ensure all tests pass before submitting
- Run: `cd backend && pytest tests/`

## Pull Request Process

1. **Update Documentation**: Update README.md if needed
2. **Test Changes**: Run backend and frontend tests
3. **Create Pull Request**: Use descriptive title and description
4. **Code Review**: Respond to review comments promptly
5. **Merge**: Once approved, your PR will be merged

## Project Structure

```
devguardian-ai/
├── backend/              # FastAPI application
│   ├── app/
│   │   ├── api/         # API endpoints
│   │   ├── core/        # Core functionality
│   │   └── models/      # Database models
│   └── tests/           # Backend tests
├── frontend/            # Vue 3 + TypeScript app
├── docker-compose.yml   # Docker configuration
└── .github/workflows/   # CI/CD pipelines
```

## Bug Reports

When reporting bugs, please include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

## Feature Requests

Feature requests are welcome! Please:
- Check existing issues first
- Provide clear description of the feature
- Explain the use case and benefits
- Consider implementation suggestions

## Security Tools

To run security scans locally:

```bash
# Install security tools for full scanning
pip install bandit semgrep
go install github.com/securego/gosec/v2/cmd/gosec@latest

# Run scans
bandit -r backend/app/
semgrep --config=auto backend/
gosec ./backend/
```