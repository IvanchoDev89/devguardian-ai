#!/bin/bash

echo "🚀 DevGuardian AI - Project Status"
echo "================================="
echo ""

echo "✅ Project Structure:"
echo "• 🐘 Laravel Backend - API and business logic"
echo "• 🤖 AI Service - Python FastAPI with ML capabilities"
echo "• 🎨 Frontend - Vue 3 + TypeScript"
echo "• 🐳 Docker - Multi-service containerization"
echo "• ☸️ Kubernetes - Production deployment"
echo "• 🔄 CI/CD - GitHub Actions workflows"
echo ""

echo "📁 Clean Directory Structure:"
ls -la | grep -E "^d" | awk '{print "• " $9}' | head -10
echo ""

echo "🔧 Quick Start:"
echo "1. ./start.sh - Start the entire system"
echo "2. ./stop.sh - Stop the system"
echo "3. sudo docker-compose ps - Check status"
echo "4. sudo docker-compose logs -f [service] - View logs"
echo ""

echo "🌐 Access Points:"
echo "• Frontend: http://localhost:3000"
echo "• Laravel API: http://localhost:8000"
echo "• AI Service: http://localhost:8001"
echo "• Database: localhost:5432"
echo "• Redis: localhost:6379"
echo ""

echo "📚 Documentation:"
echo "• README.md - Complete setup guide"
echo "• LICENSE - MIT License"
echo "• CONTRIBUTING.md - Contribution guidelines"
echo "• CODE_OF_CONDUCT.md - Community guidelines"
echo "• CHANGELOG.md - Version history"
echo ""

echo "🌐 Repository:"
echo "https://github.com/IvanchoDev89/devguardian-ai"
echo ""

echo "🎯 Status: PRODUCTION READY"
