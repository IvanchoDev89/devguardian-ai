#!/bin/bash

echo "🚀 DevGuardian AI - Simple Startup"
echo "==================================="
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
sudo docker stop $(sudo docker ps -aq) 2>/dev/null || true
sudo docker rm $(sudo docker ps -aq) 2>/dev/null || true

# Start database only
echo "🗄️ Starting PostgreSQL database..."
sudo docker run -d \
    --name devguardian-postgres \
    -e POSTGRES_DB=devguardian \
    -e POSTGRES_USER=devguardian \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -p 5432:5432 \
    timescale/timescaledb:latest-pg16

# Wait for database
echo "⏳ Waiting for database..."
sleep 15

# Test database
if sudo docker exec devguardian-postgres pg_isready -U devguardian > /dev/null 2>&1; then
    echo "✅ Database is ready"
else
    echo "❌ Database failed to start"
    exit 1
fi

# Start Redis
echo "🚀 Starting Redis..."
sudo docker run -d \
    --name devguardian-redis \
    -p 6379:6379 \
    redis:7-alpine

# Wait for Redis
sleep 5

if sudo docker exec devguardian-redis redis-cli ping > /dev/null 2>&1; then
    echo "✅ Redis is ready"
else
    echo "❌ Redis failed to start"
    exit 1
fi

echo ""
echo "🎉 Core Services Started!"
echo "=========================="
echo ""
echo "🌐 Access Points:"
echo "• Database: localhost:5432"
echo "• Redis: localhost:6379"
echo ""
echo "🔍 Test database:"
echo "sudo docker exec -it devguardian-postgres psql -U devguardian -d devguardian"
echo ""
echo "🛑 Stop services:"
echo "sudo docker stop devguardian-postgres devguardian-redis"
echo "sudo docker rm devguardian-postgres devguardian-redis"
echo ""
echo "📊 Next steps:"
echo "• Laravel and AI services can be started manually"
echo "• Frontend can be run with npm run dev"
echo "• Database and Redis are ready for connections"
