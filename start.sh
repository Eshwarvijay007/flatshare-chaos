#!/bin/bash

# Flatshare Chaos - Start All Servers
# This script starts the gpt-oss:20b model server and the FastAPI backend.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# --- Cleanup Function ---
# Ensures all background processes are stopped on exit.
cleanup() {
    echo -e "\n${YELLOW}?? Shutting down all servers...${NC}"
    # Kill all background jobs associated with this script's process group
    kill 0
    echo -e "${GREEN}?? All servers stopped.${NC}"
}

# Set up trap to call cleanup function on script exit (Ctrl+C, etc.)
trap cleanup SIGINT SIGTERM EXIT

echo -e "${BLUE}================================================================${NC}"
echo -e "${GREEN}?? Starting Flatshare Chaos Servers${NC}"
echo -e "${BLUE}================================================================${NC}"


# --- Step 1: Start the gpt-oss:20b Model Server ---

# The 'ollama' command is used here as a stand-in for the gpt-oss model runner.
# Check if the model runner command exists.
if ! command -v ollama &> /dev/null; then
    echo -e "${RED}?? Model runner command (ollama) not found.${NC}"
    echo -e "${YELLOW}Please install it to run the gpt-oss:20b model.${NC}"
    echo -e "${YELLOW}See: https://ollama.ai/download${NC}"
    exit 1
fi

# Check if the model server is already running.
if curl -s http://localhost:11434 >/dev/null 2>&1; then
    echo -e "${GREEN}?? Model server is already running.${NC}"
else
    echo -e "${BLUE}?? Starting gpt-oss:20b model server...${NC}"
    # Start the server in the background.
    ollama serve &
    
    # Wait for the server to launch.
    echo -e "${YELLOW}?? Waiting for model server to start...${NC}"
    for i in {1..30}; do
        if curl -s http://localhost:11434 >/dev/null 2>&1; then
            echo -e "${GREEN}?? Model server started successfully.${NC}"
            break
        fi
        sleep 1
    done
    
    if ! curl -s http://localhost:11434 >/dev/null 2>&1; then
        echo -e "${RED}?? Failed to start the model server.${NC}"
        exit 1
    fi
fi

# Check if the gpt-oss:20b model is available and pull it if not.
echo -e "${BLUE}?? Checking for gpt-oss:20b model...${NC}"
if ! ollama list | grep -q "gpt-oss:20b"; then
    echo -e "${YELLOW}?? Model 'gpt-oss:20b' not found. Pulling now... (this may take a while)${NC}"
    ollama pull gpt-oss:20b
fi
echo -e "${GREEN}?? gpt-oss:20b model is available.${NC}"


# --- Step 2: Start the FastAPI Backend Server ---

# Check if the FastAPI port is already in use.
if lsof -Pi :8000 -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${RED}?? Port 8000 is already in use.${NC}"
    echo -e "${YELLOW}The FastAPI server might already be running.${NC}"
    exit 1
fi

# Start the FastAPI server in the background.
echo -e "${BLUE}?? Starting FastAPI server...${NC}"
python3 -m uvicorn server.main:app --host 0.0.0.0 --port 8000 &

# Wait for the server to launch.
echo -e "${YELLOW}?? Waiting for FastAPI server to start...${NC}"
for i in {1..15}; do
    if curl -s http://localhost:8000/health >/dev/null 2>&1; then
        echo -e "${GREEN}?? FastAPI server started successfully.${NC}"
        break
    fi
    sleep 1
done

if ! curl -s http://localhost:8000/health >/dev/null 2>&1; then
    echo -e "${RED}?? Failed to start FastAPI server.${NC}"
    exit 1
fi


# --- All Servers Running ---


echo -e "\n${GREEN}?? All servers are running! In another terminal, run the CLI:${NC}"
echo -e "${YELLOW}   python -m app.ui.cli --spice=2${NC}"
echo -e "\n${YELLOW}??  Press Ctrl+C to stop all servers${NC}"
echo -e "${BLUE}================================================================${NC}"

# Wait indefinitely until the script is terminated. The 'cleanup' function will handle shutdown.
wait