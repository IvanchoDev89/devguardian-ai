#!/bin/bash

echo "🗄️ DevGuardian AI - Database Test"
echo "================================="
echo ""

# Check if Docker is running
if ! sudo docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Clean up any existing database container
echo "🧹 Cleaning up existing database..."
sudo docker stop devguardian-postgres 2>/dev/null || true
sudo docker rm devguardian-postgres 2>/dev/null || true

# Start database
echo "🗄️ Starting PostgreSQL database..."
sudo docker run -d \
    --name devguardian-postgres \
    -e POSTGRES_DB=devguardian \
    -e POSTGRES_USER=devguardian \
    -e POSTGRES_PASSWORD=devguardian_password \
    -p 5432:5432 \
    timescale/timescaledb:latest-pg16

# Wait for database to be ready
echo "⏳ Waiting for database to be ready..."
for i in {1..30}; do
    if sudo docker exec devguardian-postgres pg_isready -U devguardian > /dev/null 2>&1; then
        echo "✅ Database is ready"
        break
    fi
    echo "Waiting for database... ($i/30)"
    sleep 2
done

# Test database connection
echo "🔍 Testing database connection..."
if sudo docker exec devguardian-postgres psql -U devguardian -d devguardian -c "SELECT version();" > /dev/null 2>&1; then
    echo "✅ Database connection successful"
    echo "📊 Database version:"
    sudo docker exec devguardian-postgres psql -U devguardian -d devguardian -c "SELECT version();"
else
    echo "❌ Database connection failed"
    echo "🔍 Checking database logs:"
    sudo docker logs devguardian-postgres | tail -10
    exit 1
fi

# Create TimescaleDB extension
echo "🔧 Setting up TimescaleDB extension..."
sudo docker exec devguardian-postgres psql -U devguardian -d devguardian -c "CREATE EXTENSION IF NOT EXISTS timescaledb;"

echo ""
echo "🎉 Database is ready!"
echo "====================="
echo ""
echo "🔍 Connect to database:"
echo "sudo docker exec -it devguardian-postgres psql -U devguardian -d devguardian"
echo ""
echo "🛑 Stop database:"
echo "sudo docker stop devguardian-postgres"
echo ""
echo "🗑️ Remove database:"
echo "sudo docker rm devguardian-postgres"
