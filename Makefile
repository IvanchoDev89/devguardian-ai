.PHONY: help build up down logs test clean install

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
	@echo ""
	@echo "Development commands:"
	@echo "  make dev-setup - Complete development setup"
	@echo "  make migrate   - Run database migrations"
	@echo "  make seed      - Seed database with sample data"
	@echo "  make scan      - Run repository scan"
	@echo ""

# Build Docker images
build:
	docker-compose build

# Start all services
up:
	docker-compose up -d
	@echo "Services started. Access the app at http://localhost"

# Stop all services
down:
	docker-compose down

# Show logs
logs:
	docker-compose logs -f

# Run tests
test:
	@echo "Running Laravel tests..."
	cd laravel-backend && php artisan test
	@echo "Running AI service tests..."
	cd ai-service && pytest
	@echo "Running frontend tests..."
	cd frontend && npm run test

# Clean up Docker resources
clean:
	docker-compose down -v
	docker system prune -f

# Install dependencies
install:
	@echo "Installing Laravel dependencies..."
	cd laravel-backend && composer install
	@echo "Installing AI service dependencies..."
	cd ai-service && pip install -r requirements.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install

# Development setup
dev-setup: install up migrate
	@echo "Setting up development environment..."
	@echo "1. Generating Laravel key..."
	cd laravel-backend && php artisan key:generate
	@echo "2. Running migrations..."
	cd laravel-backend && php artisan migrate
	@echo "3. Seeding database..."
	cd laravel-backend && php artisan db:seed
	@echo "4. Building frontend..."
	cd frontend && npm run build
	@echo "Development setup complete!"

# Database migrations
migrate:
	cd laravel-backend && php artisan migrate

# Seed database
seed:
	cd laravel-backend && php artisan db:seed

# Run repository scan
scan:
	@echo "Running repository scan..."
	cd laravel-backend && php artisan scan:all

# Access containers
shell-laravel:
	docker-compose exec laravel bash

shell-ai:
	docker-compose exec ai-service bash

shell-db:
	docker-compose exec postgres psql -U devguardian devguardian

# Production deployment
deploy-prod:
	@echo "Deploying to production..."
	docker-compose -f docker-compose.prod.yml up -d

# Development utilities
dev-logs:
	docker-compose logs -f laravel ai-service

dev-restart:
	docker-compose restart laravel ai-service

dev-status:
	docker-compose ps

# Quality checks
lint:
	@echo "Running PHP linter..."
	cd laravel-backend && ./vendor/bin/pint
	@echo "Running Python linter..."
	cd ai-service && flake8 app/
	@echo "Running frontend linter..."
	cd frontend && npm run lint

# Security audit
audit:
	@echo "Running security audit..."
	cd laravel-backend && composer audit
	cd ai-service && pip-audit
	cd frontend && npm audit

# Backup database
backup:
	docker-compose exec postgres pg_dump -U devguardian devguardian > backup_$(shell date +%Y%m%d_%H%M%S).sql

# Restore database
restore:
	@read -p "Enter backup file: " backup; \
	docker-compose exec -T postgres psql -U devguardian devguardian < $$backup
