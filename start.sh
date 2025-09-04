#!/bin/bash

# Flatshare Chaos - Start All Servers
# This script starts both Ollama and FastAPI servers

set -e

echo "🎭 Starting Flatshare Chaos Servers..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to check if Ollama is running
check_ollama() {
    if curl -s http://localhost:11434/api/tags >/dev/null 2>&1; then
        return 0  # Ollama is running
    else
        return 1  # Ollama is not running
    fi
}

# Cleanup function
cleanup() {
    echo -e "\n${YELLOW}🛑 Shutting down servers...${NC}"
    
    # Kill background jobs
    jobs -p | xargs -r kill 2>/dev/null || true
    
    # Kill any remaining processes
    pkill -f "ollama serve" 2>/dev/null || true
    pkill -f "uvicorn server.main:app" 2>/dev/null || true
    
    echo -e "${GREEN}✅ All servers stopped.${NC}"
    exit 0
}

# Set up trap for cleanup
trap cleanup SIGINT SIGTERM EXIT

# Check if Ollama is installed
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}❌ Ollama is not installed.${NC}"
    echo -e "${BLUE}Please install Ollama from: https://ollama.ai/download${NC}"
    exit 1
fi

# Start Ollama if not running
if check_ollama; then
    echo -e "${GREEN}✅ Ollama is already running${NC}"
else
    echo -e "${BLUE}🚀 Starting Ollama server...${NC}"
    ollama serve &
    OLLAMA_PID=$!
    
    # Wait for Ollama to start
    echo -e "${YELLOW}⏳ Waiting for Ollama to start...${NC}"
    for i in {1..30}; do
        if check_ollama; then
            echo -e "${GREEN}✅ Ollama server started successfully${NC}"
            break
        fi
        sleep 1
    done
    
    if ! check_ollama; then
        echo -e "${RED}❌ Failed to start Ollama server${NC}"
        exit 1
    fi
fi

# Check if model is available
echo -e "${BLUE}📋 Checking for llama3.1 model...${NC}"
if ! ollama list | grep -q "llama3.1"; then
    echo -e "${YELLOW}📥 Pulling llama3.1 model... (this may take a while)${NC}"
    ollama pull llama3.1
fi
echo -e "${GREEN}✅ Model llama3.1 is available${NC}"

# Check if FastAPI port is available
if check_port 8000; then
    echo -e "${YELLOW}⚠️  Port 8000 is already in use${NC}"
    echo -e "${BLUE}FastAPI server might already be running${NC}"
else
    # Start FastAPI server
    echo -e "${BLUE}🚀 Starting FastAPI server...${NC}"
    python3.11 -m uvicorn server.main:app --host 0.0.0.0 --port 8000 --reload &
    FASTAPI_PID=$!
    
    # Wait for FastAPI to start
    echo -e "${YELLOW}⏳ Waiting for FastAPI to start...${NC}"
    for i in {1..10}; do
        if curl -s http://localhost:8000/health >/dev/null 2>&1; then
            echo -e "${GREEN}✅ FastAPI server started successfully${NC}"
            break
        fi
        sleep 1
    done
fi

# Show status
echo -e "\n${BLUE}================================================================${NC}"
echo -e "${GREEN}🎭 FLATSHARE CHAOS SERVERS RUNNING${NC}"
echo -e "${BLUE}================================================================${NC}"

if check_ollama; then
    echo -e "${GREEN}✅ Ollama Server: http://localhost:11434${NC}"
else
    echo -e "${RED}❌ Ollama Server: Not running${NC}"
fi

if curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${GREEN}✅ FastAPI Server: http://localhost:8000${NC}"
else
    echo -e "${RED}❌ FastAPI Server: Not running${NC}"
fi

echo -e "\n${GREEN}🚀 Ready to use! Run the CLI with:${NC}"
echo -e "${YELLOW}   python3.11 -m app.ui.cli --spice=2 --stream${NC}"

echo -e "\n${BLUE}📚 Available endpoints:${NC}"
echo -e "   • Health check: ${YELLOW}http://localhost:8000/health${NC}"
echo -e "   • API docs: ${YELLOW}http://localhost:8000/docs${NC}"

echo -e "\n${YELLOW}⏹️  Press Ctrl+C to stop all servers${NC}"
echo -e "${BLUE}================================================================${NC}"

# Keep script running
while true; do
    sleep 1
done