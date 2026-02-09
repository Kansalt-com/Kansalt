@echo off
REM Quick deployment script for Kansalt to Render.com (Windows)

setlocal enabledelayedexpansion

echo.
echo 🚀 Kansalt Deployment Assistant
echo ==================================
echo.

REM Check if git is installed
where git >nul 2>nul
if errorlevel 1 (
    echo ❌ Git is required but not installed. Please install Git first.
    pause
    exit /b 1
)

REM Check if we're in a git repo
git rev-parse --git-dir >nul 2>&1
if errorlevel 1 (
    echo 📦 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit: Kansalt job aggregator"
) else (
    echo ✅ Git repository found
)

REM Check for uncommitted changes
git diff-index --quiet HEAD --
if errorlevel 1 (
    echo ⚠️  Uncommitted changes detected. Committing...
    git add .
    git commit -m "Deployment update: %date% %time%"
)

echo.
echo 📋 Deployment Steps:
echo ===================
echo.
echo 1. Push to GitHub:
echo    git push origin main
echo.
echo 2. Go to https://render.com
echo    - Sign up (if needed)
echo    - Click 'New' ^→ 'Blueprint'
echo    - Select this GitHub repository
echo    - Authorize GitHub access
echo    - Click 'Deploy Blueprint'
echo.
echo 3. Wait 2-3 minutes for build and deployment
echo.
echo 4. Your app will be live at:
echo    https://kansalt.onrender.com
echo.
echo 5. (Optional) Add custom domain in Render dashboard
echo.

echo 📦 Files to be deployed:
echo =======================
git ls-files | findstr /R "\.py$ \.toml$ \.txt$ \.json$ \.yaml$ \.yml$ \.sh$ \.md$"

echo.
set /p continue="Ready to push to GitHub? (y/n): "
if /i "%continue%"=="y" (
    echo 🔄 Pushing to GitHub...
    git push origin main
    if errorlevel 0 (
        echo ✅ Pushed successfully!
        echo.
        echo 🎉 Next: Go to https://render.com ^→ New ^→ Blueprint
        echo    Select this repository and deploy
    ) else (
        echo ❌ Push failed. Check your GitHub connection.
    )
) else (
    echo ⏳ Deployment paused. Run this script again when ready.
)

pause
