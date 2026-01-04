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

# Start the database first
echo "🗄️ Starting PostgreSQL database..."
sudo docker-compose up -d postgres

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
sleep 10

# Check if database is ready
if sudo docker-compose exec -T postgres pg_isready -U devguardian > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database failed to start"
    exit 1
fi

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

# Start Laravel backend
echo "🐘 Starting Laravel backend..."
sudo docker-compose up -d laravel

# Wait for Laravel
sleep 15

# Check Laravel health
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Laravel backend is ready"
else
    echo "⚠️ Laravel backend might still be starting..."
fi

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
echo "sudo docker-compose down"
echo ""
echo "📊 View logs:"
echo "sudo docker-compose logs -f [service-name]"
