# AI Work OS - Development Startup Script (Windows)

Write-Host "🚀 Starting AI Work OS Development Environment..." -ForegroundColor Green

# Check if Docker is running
try {
    docker info | Out-Null
} catch {
    Write-Host "❌ Docker is not running. Please start Docker Desktop first." -ForegroundColor Red
    exit 1
}

# Start services
Write-Host "📦 Starting Docker services..." -ForegroundColor Cyan
docker-compose up -d postgres redis

# Wait for PostgreSQL
Write-Host "⏳ Waiting for PostgreSQL..." -ForegroundColor Yellow
Start-Sleep -Seconds 5

# Run migrations
Write-Host "🔄 Running database migrations..." -ForegroundColor Cyan
Set-Location backend
poetry run alembic upgrade head
Set-Location ..

# Start backend
Write-Host "🐍 Starting FastAPI backend..." -ForegroundColor Cyan
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

# Start frontend (if exists)
if (Test-Path "frontend") {
    Write-Host "⚛️  Starting Next.js frontend..." -ForegroundColor Cyan
    Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; pnpm dev"
}

Write-Host ""
Write-Host "✅ AI Work OS is running!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Backend API: http://localhost:8001" -ForegroundColor White
Write-Host "📍 API Docs: http://localhost:8001/docs" -ForegroundColor White
if (Test-Path "frontend") {
    Write-Host "📍 Frontend: http://localhost:3001" -ForegroundColor White
}
Write-Host ""
Write-Host "Press Ctrl+C in the backend/frontend windows to stop services" -ForegroundColor Yellow
