#!/usr/bin/env python3.11
"""
Simple server runner for Flatshare Chaos.
Starts both Ollama and FastAPI servers in one command.
"""

import subprocess
import time
import sys
import os
import signal
import requests
from concurrent.futures import ThreadPoolExecutor

def print_colored(message, color="white"):
    """Print colored messages."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m", 
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m"
    }
    print(f"{colors.get(color, '')}{message}{colors['reset']}")

def check_ollama():
    """Check if Ollama is running."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=3)
        return response.status_code == 200
    except:
        return False

def check_fastapi():
    """Check if FastAPI is running."""
    try:
        response = requests.get("http://localhost:8000/health", timeout=3)
        return response.status_code == 200
    except:
        return False

def start_ollama():
    """Start Ollama server."""
    if check_ollama():
        print_colored("Ollama is already running", "green")
        return None
    
    print_colored("Starting Ollama server...", "blue")
    try:
        process = subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        
        # Wait for Ollama to start
        for i in range(30):
            if check_ollama():
                print_colored("Ollama server started", "green")
                return process
            time.sleep(1)
        
        print_colored("Ollama failed to start", "red")
        return None
        
    except FileNotFoundError:
        print_colored("Ollama not found. Install from: https://ollama.ai/download", "red")
        return None

def start_fastapi():
    """Start FastAPI server."""
    if check_fastapi():
        print_colored("FastAPI is already running", "green")
        return None
    
    print_colored("Starting FastAPI server...", "blue")
    try:
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn",
            "server.main:app",
            "--host", "0.0.0.0",
            "--port", "8000"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Wait for FastAPI to start
        for i in range(15):
            if check_fastapi():
                print_colored("FastAPI server started", "green")
                return process
            time.sleep(1)
        
        print_colored("FastAPI failed to start", "red")
        return None
        
    except Exception as e:
        print_colored(f"Error starting FastAPI: {e}", "red")
        return None

def ensure_model():
    """Ensure the required model is available."""
    print_colored("Checking for gpt-oss:20b model...", "blue")
    try:
        result = subprocess.run(["ollama", "list"], capture_output=True, text=True)
        if "gpt-oss:20b" in result.stdout:
            print_colored("Model gpt-oss:20b is available", "green")
            return
        
        print_colored("Pulling gpt-oss:20b model... (this may take a while)", "yellow")
        subprocess.run(["ollama", "pull", "gpt-oss:20b"], check=True)
        print_colored("Model gpt-oss:20b pulled successfully", "green")
        
    except subprocess.CalledProcessError:
        print_colored("Failed to pull model", "red")
    except FileNotFoundError:
        print_colored("Ollama command not found", "red")

def show_status():
    """Show server status."""
    print_colored("\n" + "="*60, "cyan")
    print_colored("FLATSHARE CHAOS SERVERS", "magenta")
    print_colored("="*60, "cyan")
    
    if check_ollama():
        print_colored("Ollama Server: http://localhost:11434", "green")
    else:
        print_colored("Ollama Server: Not running", "red")
    
    if check_fastapi():
        print_colored("FastAPI Server: http://localhost:8000", "green")
    else:
        print_colored("FastAPI Server: Not running", "red")
    
    print_colored("\nReady! Run the CLI:", "green")
    print_colored("   python3.11 -m app.ui.cli --spice=2 --stream", "yellow")
    
    print_colored("\nAvailable endpoints:", "blue")
    print_colored("   Health: http://localhost:8000/health", "white")
    print_colored("   Docs: http://localhost:8000/docs", "white")
    
    print_colored("\n  Press Ctrl+C to stop servers", "yellow")
    print_colored("="*60, "cyan")

def main():
    """Main function."""
    processes = []
    
    def cleanup(signum=None, frame=None):
        print_colored("\nStopping servers...", "yellow")
        for process in processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except:
                try:
                    process.kill()
                except:
                    pass
        print_colored("All servers stopped", "green")
        sys.exit(0)
    
    # Set up signal handlers
    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)
    
    print_colored("Starting Flatshare Chaos Servers...", "magenta")
    
    # Start servers
    ollama_process = start_ollama()
    if ollama_process:
        processes.append(ollama_process)
    
    if check_ollama():
        ensure_model()
    
    fastapi_process = start_fastapi()
    if fastapi_process:
        processes.append(fastapi_process)
    
    # Show status
    show_status()
    
    # Keep running
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cleanup()

if __name__ == "__main__":
    main()
