#!/bin/bash

echo "🛑 DevGuardian AI - System Shutdown"
echo "=================================="
echo ""

echo "🔄 Stopping all services..."
sudo docker-compose down

echo "🧹 Cleaning up..."
sudo docker-compose down -v

echo "✅ System stopped successfully"
echo ""
echo "🚀 Start system again:"
echo "./start.sh"
