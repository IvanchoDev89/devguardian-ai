.PHONY: help build up down logs test clean install dev

# Default target
help:
	@echo "DevGuardian AI - Available commands:"
	@echo ""
	@echo "  make build     - Build all Docker images"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make logs      - Show logs from all services"
	@echo "  make test      - Run all tests"
	@echo "  make clean     - Clean up Docker resources"
	@echo "  make install   - Install dependencies"
	@echo "  make dev       - Start development environment"
	@echo ""

# Build Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d
	@echo "Services started. Access the app at http://localhost:3000"

# Stop all services
down:
	docker-compose down

# Show logs
logs:
	docker-compose logs -f

# Run tests
test:
	@echo "Running backend tests..."
	cd backend && python -m pytest tests/ -v
	@echo "Running frontend tests..."
	cd frontend && npm run test

# Clean up Docker resources
clean:
	docker-compose down -v
	docker system prune -f

# Install dependencies
install:
	@echo "Installing backend dependencies..."
	cd backend && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Start development environment
dev:
	@echo "Starting development environment..."
	@echo "1. Starting PostgreSQL..."
	docker-compose up -d postgres
	@echo "2. Starting backend..."
	cd backend && source venv/bin/activate && uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload
	@echo "3. Starting frontend..."
	cd frontend && npm run dev
	@echo "Development environment ready!"

# Backend only (for manual development)
backend-dev:
	cd backend && source venv/bin/activate && uvicorn app.main:app --host 127.0.0.1 --port 8002 --reload

# Frontend only
frontend-dev:
	cd frontend && npm run dev

# Access containers
shell-backend:
	docker-compose exec backend bash

shell-db:
	docker-compose exec postgres psql -U devguardian devguardian_ai

# Production deployment
deploy-prod:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.prod.yml up -d

# Quality checks
lint:
	@echo "Running backend linter..."
	cd backend && flake8 app/ || true
	@echo "Running frontend linter..."
	cd frontend && npm run lint

# Security audit
audit:
	@echo "Running security audit..."
	cd backend && pip-audit || true
	cd frontend && npm audit

# Backup database
backup:
	docker-compose exec postgres pg_dump -U devguardian devguardian_ai > backup_$$(date +%Y%m%d_%H%M%S).sql

# Restore database
restore:
	@read -p "Enter backup file: " backup; \
	docker-compose exec -T postgres psql -U devguardian devguardian_ai < "$$backup"