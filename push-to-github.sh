#!/bin/bash

# GitHub Repository Setup Script
# Run this after creating your repository on GitHub

echo "🚀 Setting up GitHub repository for DevGuardian AI..."
echo ""

# Add the remote repository
echo "📡 Adding remote repository..."
git remote add origin https://github.com/ivanbermudez/devguardian-ai.git

# Verify the remote was added
echo "✅ Remote added:"
git remote -v

echo ""
echo "📤 Pushing to GitHub..."
echo "You may be prompted for your GitHub credentials..."

# Push to GitHub
git push -u origin main

echo ""
echo "🎉 Repository successfully pushed to GitHub!"
echo "📍 Visit: https://github.com/ivanbermudez/devguardian-ai"
echo ""
echo "📋 Next steps:"
echo "1. Visit your repository on GitHub"
echo "2. Enable Issues for bug tracking"
echo "3. Enable Projects for project management"
echo "4. Set up branch protection for main branch"
echo "5. Add collaborators if working with a team"
