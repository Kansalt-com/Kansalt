#!/bin/bash
# Quick deployment script for Kansalt to Render.com
# This script automates the deployment process

set -e

echo "🚀 Kansalt Deployment Assistant"
echo "=================================="
echo ""

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo "❌ Git is required but not installed. Please install Git first."
    exit 1
fi

# Check if we're in a git repo
if ! git rev-parse --git-dir > /dev/null 2>&1; then
    echo "📦 Initializing git repository..."
    git init
    git add .
    git commit -m "Initial commit: Kansalt job aggregator"
else
    echo "✅ Git repository found"
fi

# Check for uncommitted changes
if ! git diff-index --quiet HEAD --; then
    echo "⚠️  Uncommitted changes detected. Committing..."
    git add .
    git commit -m "Deployment update: $(date)"
fi

echo ""
echo "📋 Deployment Steps:"
echo "==================="
echo ""
echo "1. Push to GitHub:"
echo "   git push origin main"
echo ""
echo "2. Go to https://render.com"
echo "   - Sign up (if needed)"
echo "   - Click 'New' → 'Blueprint'"
echo "   - Select this GitHub repository"
echo "   - Authorize GitHub access"
echo "   - Click 'Deploy Blueprint'"
echo ""
echo "3. Wait 2-3 minutes for build and deployment"
echo ""
echo "4. Your app will be live at:"
echo "   https://kansalt.onrender.com"
echo ""
echo "5. (Optional) Add custom domain in Render dashboard"
echo ""

# Optional: Show what files will be deployed
echo "📦 Files to be deployed:"
echo "======================="
git ls-files | grep -E '\.(py|toml|txt|json|yaml|yml|sh|md)$' | head -20
echo "   ... and more"
echo ""

# Prompt user to continue
read -p "Ready to push to GitHub? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🔄 Pushing to GitHub..."
    git push origin main
    echo "✅ Pushed successfully!"
    echo ""
    echo "🎉 Next: Go to https://render.com → New → Blueprint"
    echo "   Select this repository and deploy"
else
    echo "⏳ Deployment paused. Run this script again when ready."
fi
