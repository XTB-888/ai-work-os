@echo off
chcp 65001 >nul
echo 🚀 Starting AI Work OS Backend...
echo.

cd /d "C:\Users\monarch\Documents\AI-Work-OS\backend"

:: Activate virtual environment
call venv\Scripts\activate

:: Check if .env exists
if not exist .env (
    echo ⚠️  .env file not found. Creating from example...
    copy .env.example .env
    echo ⚠️  Please edit .env and add your DASHSCOPE_API_KEY
    pause
    exit /b 1
)

:: Run database migrations
echo 🔄 Running database migrations...
alembic upgrade head
if errorlevel 1 (
    echo ❌ Migration failed
    pause
    exit /b 1
)

:: Start backend
echo ✅ Starting backend server...
echo 📍 Backend will be available at: http://localhost:8001
echo 📍 API Docs: http://localhost:8001/docs
echo.

uvicorn app.main:app --reload --host 0.0.0.0 --port 8001

pause
