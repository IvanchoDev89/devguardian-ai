#!/bin/bash

echo "🚀 DevGuardian AI - System Startup"
echo "=================================="
echo ""

# Check if Docker is running
if ! sudo docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Clean up any existing containers
echo "🧹 Cleaning up existing containers..."
sudo docker-compose down -v 2>/dev/null || true

# Start the database first
echo "🗄️ Starting PostgreSQL database..."
sudo docker-compose up -d postgres

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
for i in {1..30}; do
    if sudo docker-compose exec -T postgres pg_isready -U devguardian > /dev/null 2>&1; then
        echo "✅ Database is ready"
        break
    fi
    echo "Waiting for database... ($i/30)"
    sleep 2
done

# Double check database connection
if ! sudo docker-compose exec -T postgres pg_isready -U devguardian > /dev/null 2>&1; then
    echo "❌ Database failed to start properly"
    echo "🔍 Checking database logs:"
    sudo docker-compose logs postgres | tail -10
    exit 1
fi

# Create database if it doesn't exist
echo "🔧 Setting up database..."
sudo docker-compose exec -T postgres psql -U devguardian -c "CREATE DATABASE IF NOT EXISTS devguardian;" 2>/dev/null || true

# Start Redis
echo "🚀 Starting Redis..."
sudo docker-compose up -d redis

# Wait for Redis
sleep 5

if sudo docker-compose exec -T redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis failed to start"
    exit 1
fi

# Run Laravel migrations
echo "🐘 Running Laravel migrations..."
sudo docker-compose up -d laravel
sleep 10

# Wait for Laravel to be ready and run migrations
for i in {1..20}; do
    if sudo docker-compose exec -T laravel php artisan migrate:status > /dev/null 2>&1; then
        echo "✅ Laravel is ready, running migrations..."
        sudo docker-compose exec -T laravel php artisan migrate --force
        break
    fi
    echo "Waiting for Laravel... ($i/20)"
    sleep 3
done

# Start AI service
echo "🤖 Starting AI service..."
sudo docker-compose up -d ai-service

# Wait for AI service
sleep 10

# Check AI service health
if curl -s http://localhost:8001/health > /dev/null 2>&1; then
    echo "✅ AI service is ready"
else
    echo "⚠️ AI service might still be starting..."
fi

# Start Frontend
echo "🎨 Starting Frontend..."
sudo docker-compose up -d frontend

# Wait for Frontend
sleep 10

echo ""
echo "🎉 DevGuardian AI System Started!"
echo "================================="
echo ""
echo "🌐 Access Points:"
echo "• Frontend: http://localhost:3000"
echo "• Laravel API: http://localhost:8000"
echo "• AI Service: http://localhost:8001"
echo "• Database: localhost:5432"
echo "• Redis: localhost:6379"
echo ""
echo "🔍 Check system status:"
echo "sudo docker-compose ps"
echo ""
echo "🛑 Stop system:"
echo "./stop.sh"
echo ""
echo "📊 View logs:"
echo "sudo docker-compose logs -f [service-name]"
echo ""
echo "🗄️ Database connection test:"
echo "sudo docker-compose exec postgres psql -U devguardian -d devguardian -c \"SELECT version();\""
