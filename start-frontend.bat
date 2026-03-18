@echo off
chcp 65001 >nul
echo 🚀 Starting AI Work OS Frontend...
echo.

cd /d "C:\Users\monarch\Documents\AI-Work-OS\frontend"

:: Check if node_modules exists
if not exist node_modules (
    echo 📦 Installing dependencies...
    call pnpm install --registry https://registry.npmmirror.com
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

:: Start frontend
echo ✅ Starting frontend server...
echo 📍 Frontend will be available at: http://localhost:3001
echo.

call pnpm dev

pause
