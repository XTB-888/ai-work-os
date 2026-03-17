#!/usr/bin/env bash
# Development startup script

echo "🚀 Starting AI Work OS Development Environment..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker first."
    exit 1
fi

# Start services
echo "📦 Starting Docker services..."
docker-compose up -d postgres redis

# Wait for PostgreSQL
echo "⏳ Waiting for PostgreSQL..."
sleep 5

# Run migrations
echo "🔄 Running database migrations..."
cd backend
poetry run alembic upgrade head
cd ..

# Start backend
echo "🐍 Starting FastAPI backend..."
cd backend
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!
cd ..

# Start frontend (if exists)
if [ -d "frontend" ]; then
    echo "⚛️  Starting Next.js frontend..."
    cd frontend
    pnpm dev &
    FRONTEND_PID=$!
    cd ..
fi

echo ""
echo "✅ AI Work OS is running!"
echo ""
echo "📍 Backend API: http://localhost:8000"
echo "📍 API Docs: http://localhost:8000/docs"
if [ -d "frontend" ]; then
    echo "📍 Frontend: http://localhost:3000"
fi
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "echo ''; echo '👋 Stopping services...'; kill $BACKEND_PID 2>/dev/null; kill $FRONTEND_PID 2>/dev/null; docker-compose down; exit 0" INT
wait
