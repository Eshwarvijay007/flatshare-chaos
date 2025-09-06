#!/usr/bin/env python3.11
"""
Startup script to run both Ollama and FastAPI servers for Flatshare Chaos.
This eliminates the need for multiple terminals.
"""

import subprocess
import time
import sys
import os
import signal
import requests
from typing import List, Optional

class ServerManager:
    def __init__(self):
        self.processes: List[subprocess.Popen] = []
        self.ollama_url = os.getenv("OLLAMA_URL", "http://127.0.0.1:11434")
        self.fastapi_port = os.getenv("FASTAPI_PORT", "8000")
        
    def cleanup(self, signum=None, frame=None):
        """Clean up all running processes."""
        print("\n?? Shutting down servers...")
        for process in self.processes:
            try:
                process.terminate()
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()
            except Exception:
                pass
        print("?? All servers stopped.")
        sys.exit(0)
    
    def check_ollama_running(self) -> bool:
        """Check if Ollama is already running."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=5)
            return response.status_code == 200
        except Exception:
            return False
    
    def start_ollama(self) -> Optional[subprocess.Popen]:
        """Start Ollama server if not already running."""
        if self.check_ollama_running():
            print("?? Ollama is already running")
            return None
        
        print("?? Starting Ollama server...")
        try:
            # Try to start Ollama
            process = subprocess.Popen(
                ["ollama", "serve"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Wait a bit for Ollama to start
            time.sleep(3)
            
            if process.poll() is None and self.check_ollama_running():
                print("?? Ollama server started successfully")
                return process
            else:
                print("?? Failed to start Ollama server")
                return None
                
        except FileNotFoundError:
            print("?? Ollama not found. Please install Ollama first:")
            print("   Visit: https://ollama.ai/download")
            return None
        except Exception as e:
            print(f"?? Error starting Ollama: {e}")
            return None
    
    def check_model_available(self, model_name: str = "llama3.1") -> bool:
        """Check if the required model is available."""
        try:
            response = requests.get(f"{self.ollama_url}/api/tags", timeout=10)
            if response.status_code == 200:
                models = response.json().get("models", [])
                available_models = [m["name"] for m in models]
                return any(model_name in model for model in available_models)
            return False
        except Exception:
            return False
    
    def pull_model(self, model_name: str = "gpt-oss:20b"):
        """Pull the required model if not available."""
        if self.check_model_available(model_name):
            print(f"?? Model {model_name} is available")
            return
        
        print(f"?? Pulling model {model_name}... (this may take a while)")
        try:
            subprocess.run(["ollama", "pull", model_name], check=True)
            print(f"?? Model {model_name} pulled successfully")
        except subprocess.CalledProcessError:
            print(f"?? Failed to pull model {model_name}")
        except FileNotFoundError:
            print("?? Ollama command not found")
    
    def start_fastapi(self) -> Optional[subprocess.Popen]:
        """Start FastAPI server."""
        print("?? Starting FastAPI server...")
        try:
            process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", 
                "server.main:app", 
                "--host", "0.0.0.0", 
                "--port", self.fastapi_port,
                "--reload"
            ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            
            # Wait a bit for FastAPI to start
            time.sleep(2)
            
            if process.poll() is None:
                print(f"?? FastAPI server started on http://localhost:{self.fastapi_port}")
                return process
            else:
                print("?? Failed to start FastAPI server")
                return None
                
        except Exception as e:
            print(f"?? Error starting FastAPI server: {e}")
            return None
    
    def wait_for_servers(self):
        """Wait for servers to be ready."""
        print("?? Waiting for servers to be ready...")
        
        # Wait for Ollama
        for i in range(30):  # 30 second timeout
            if self.check_ollama_running():
                break
            time.sleep(1)
        else:
            print("??  Ollama server not responding")
        
        # Wait for FastAPI
        for i in range(10):  # 10 second timeout
            try:
                response = requests.get(f"http://localhost:{self.fastapi_port}/health", timeout=2)
                if response.status_code == 200:
                    break
            except Exception:
                pass
            time.sleep(1)
        else:
            print("??  FastAPI server not responding")
    
    def show_status(self):
        """Show server status and usage instructions."""
        print("\n" + "="*60)
        print("?? FLATSHARE CHAOS SERVERS RUNNING")
        print("="*60)
        
        # Check Ollama status
        if self.check_ollama_running():
            print(f"?? Ollama Server: {self.ollama_url}")
        else:
            print("?? Ollama Server: Not running")
        
        # Check FastAPI status
        try:
            response = requests.get(f"http://localhost:{self.fastapi_port}/health", timeout=2)
            if response.status_code == 200:
                print(f"?? FastAPI Server: http://localhost:{self.fastapi_port}")
            else:
                print("?? FastAPI Server: Not responding")
        except Exception:
            print("?? FastAPI Server: Not running")
        
        print("\n?? Ready to use! Run the CLI with:")
        print(f"   python3.11 -m app.ui.cli --spice=2 --stream")
        print("\n?? Available endpoints:")
        print(f"   ? Health check: http://localhost:{self.fastapi_port}/health")
        print(f"   ? API docs: http://localhost:{self.fastapi_port}/docs")
        print("\n???  Press Ctrl+C to stop all servers")
        print("="*60)
    
    def run(self):
        """Main run method."""
        # Set up signal handlers for clean shutdown
        signal.signal(signal.SIGINT, self.cleanup)
        signal.signal(signal.SIGTERM, self.cleanup)
        
        print("?? Starting Flatshare Chaos Servers...")
        
        # Start Ollama
        ollama_process = self.start_ollama()
        if ollama_process:
            self.processes.append(ollama_process)
        
        # Wait for Ollama to be ready
        if not self.check_ollama_running():
            print("?? Ollama server is not running. Please start it manually:")
            print("   ollama serve")
            return
        
        # Pull model if needed
        self.pull_model()
        
        # Start FastAPI
        fastapi_process = self.start_fastapi()
        if fastapi_process:
            self.processes.append(fastapi_process)
        
        # Wait for servers to be ready
        self.wait_for_servers()
        
        # Show status
        self.show_status()
        
        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
                # Check if any process died
                for process in self.processes[:]:  # Copy list to avoid modification during iteration
                    if process.poll() is not None:
                        print(f"??  A server process stopped unexpectedly")
                        self.processes.remove(process)
        except KeyboardInterrupt:
            self.cleanup()


def main():
    """Main entry point."""
    print("?? Flatshare Chaos Server Manager")
    print("This script will start both Ollama and FastAPI servers for you.\n")
    
    # Check dependencies
    try:
        import uvicorn
        import fastapi
        import requests
    except ImportError as e:
        print(f"?? Missing dependency: {e}")
        print("Please install requirements:")
        print("   pip install -r requirements.txt")
        return
    
    manager = ServerManager()
    manager.run()


if __name__ == "__main__":
    main()
