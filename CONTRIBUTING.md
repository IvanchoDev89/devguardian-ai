# Contributing to DevGuardian AI

Thank you for your interest in contributing to DevGuardian AI! This document provides guidelines and information for contributors.

## 🚀 Getting Started

### Prerequisites
- Docker & Docker Compose
- Node.js 18+
- PHP 8.3+
- Python 3.11+

### Development Setup
1. Fork the repository
2. Clone your fork locally
3. Run `make dev-setup` to initialize the development environment
4. Create a feature branch for your contribution

## 📋 Development Guidelines

### Code Style
- **PHP**: Follow PSR-12 standards, use Laravel Pint
- **Python**: Follow PEP 8, use Black formatter
- **TypeScript/Vue**: Use ESLint and Prettier
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

Example: `feat(ai-service): add vulnerability analysis endpoint`

### Testing
- Write tests for new features
- Ensure all tests pass before submitting
- Maintain test coverage above 80%

## 🔄 Pull Request Process

1. **Update Documentation**: Update README.md if needed
2. **Test Changes**: Run `make test` to ensure all tests pass
3. **Create Pull Request**: Use descriptive title and description
4. **Code Review**: Respond to review comments promptly
5. **Merge**: Once approved, your PR will be merged

## 🏗️ Project Structure

```
devguardian-ai/
├── laravel-backend/     # Laravel API application
├── ai-service/         # Python FastAPI service
├── frontend/           # Vue 3 + TypeScript app
├── docker/             # Docker configurations
├── kubernetes/         # K8s deployment manifests
└── .github/workflows/  # CI/CD pipelines
```

## 🐛 Bug Reports

When reporting bugs, please include:
- Description of the issue
- Steps to reproduce
- Expected vs actual behavior
- Environment details
- Screenshots if applicable

## 💡 Feature Requests

Feature requests are welcome! Please:
- Check existing issues first
- Provide clear description of the feature
- Explain the use case and benefits
- Consider implementation suggestions

## 📧 Getting Help

- Create an issue for bugs or questions
- Join our Discord community
- Check the documentation

## 📜 Code of Conduct

Please be respectful and professional in all interactions. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) for details.

## 🎯 Areas for Contribution

We welcome contributions in:
- **Security Scanners**: Add new vulnerability detection tools
- **AI Models**: Improve fix generation algorithms
- **Frontend**: Enhance UI/UX and add features
- **Documentation**: Improve guides and API docs
- **Testing**: Add more test coverage
- **DevOps**: Improve CI/CD and deployment

## 🙏 Thank You

Your contributions help make DevGuardian AI better for everyone! We appreciate all forms of contribution, whether code, documentation, testing, or feedback.
