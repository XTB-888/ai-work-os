#!/bin/bash

# AI Work OS - Local Development Startup Script (No Docker)
# This script starts the backend and frontend directly without Docker

echo "🚀 Starting AI Work OS in local development mode..."
echo ""

# Check if required tools are installed
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required but not installed. Aborting."; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required but not installed. Aborting."; exit 1; }
command -v pnpm >/dev/null 2>&1 || { echo "❌ pnpm is required but not installed. Install with: npm install -g pnpm"; exit 1; }

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}Step 1: Checking environment...${NC}"

# Check if PostgreSQL is running
if pg_isready -h localhost -p 5433 >/dev/null 2>&1; then
    echo -e "${GREEN}✓ PostgreSQL is running on port 5433${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not running on port 5433${NC}"
    echo "Please start PostgreSQL first:"
    echo "  Windows: Start PostgreSQL service"
    echo "  macOS: brew services start postgresql"
    echo "  Linux: sudo service postgresql start"
    exit 1
fi

# Check if Redis is running
if redis-cli -p 6380 ping >/dev/null 2>&1; then
    echo -e "${GREEN}✓ Redis is running on port 6380${NC}"
else
    echo -e "${RED}✗ Redis is not running on port 6380${NC}"
    echo "Please start Redis first:"
    echo "  redis-server --port 6380"
    exit 1
fi

echo ""
echo -e "${YELLOW}Step 2: Setting up backend...${NC}"

cd backend

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
if [ ! -f "venv/installed" ]; then
    echo "Installing Python dependencies..."
    pip install -r requirements.txt 2>/dev/null || pip install fastapi uvicorn sqlalchemy asyncpg psycopg2-binary alembic pydantic python-jose passlib python-multipart redis langchain langchain-openai langgraph openai httpx websockets
    touch venv/installed
fi

# Check if .env exists
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠ .env file not found. Creating from example...${NC}"
    cp .env.example .env
    echo -e "${RED}⚠ Please edit backend/.env and add your OPENAI_API_KEY${NC}"
fi

echo -e "${GREEN}✓ Backend setup complete${NC}"

echo ""
echo -e "${YELLOW}Step 3: Running database migrations...${NC}"
alembic upgrade head

echo ""
echo -e "${YELLOW}Step 4: Starting backend server...${NC}"
echo "Backend will be available at: http://localhost:8001"
echo ""

# Start backend in background
uvicorn app.main:app --reload --host 0.0.0.0 --port 8001 &
BACKEND_PID=$!

cd ..

echo ""
echo -e "${YELLOW}Step 5: Setting up frontend...${NC}"

cd frontend

# Install dependencies
if [ ! -d "node_modules" ]; then
    echo "Installing Node.js dependencies..."
    pnpm install
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

echo ""
echo -e "${YELLOW}Step 6: Starting frontend server...${NC}"
echo "Frontend will be available at: http://localhost:3001"
echo ""

# Start frontend
pnpm dev &
FRONTEND_PID=$!

cd ..

echo ""
echo -e "${GREEN}✅ AI Work OS is running!${NC}"
echo ""
echo "📍 Frontend: http://localhost:3001"
echo "📍 Backend API: http://localhost:8001"
echo "📍 API Docs: http://localhost:8001/docs"
echo ""
echo "Press Ctrl+C to stop all services"
echo ""

# Wait for interrupt
trap "echo ''; echo -e '${YELLOW}Stopping services...${NC}'; kill $BACKEND_PID 2>/dev/null; kill $FRONTEND_PID 2>/dev/null; echo -e '${GREEN}Services stopped${NC}'; exit 0" INT
wait
