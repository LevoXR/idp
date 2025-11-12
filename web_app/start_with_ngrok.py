#!/usr/bin/env python3
"""
Start Aditya Setu server with ngrok tunnel for external access
This script requires ngrok to be installed and configured
"""

import os
import sys
import subprocess
import time
import signal
import urllib.request
import json

# Fix Windows console encoding issues
if sys.platform == 'win32':
    try:
        # Try to set UTF-8 encoding for Windows console
        import codecs
        sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
        sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')
    except:
        pass

def check_ngrok_installed():
    """Check if ngrok is installed"""
    try:
        result = subprocess.run(['ngrok', 'version'], 
                              capture_output=True, 
                              text=True, 
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False

def get_ngrok_url():
    """Get the ngrok tunnel URL"""
    try:
        # ngrok API endpoint (default)
        response = urllib.request.urlopen('http://127.0.0.1:4040/api/tunnels', timeout=2)
        data = json.loads(response.read().decode())
        tunnels = data.get('tunnels', [])
        if tunnels:
            # Prefer HTTPS URL if available
            for tunnel in tunnels:
                if tunnel.get('proto') == 'https':
                    return tunnel.get('public_url')
            # Otherwise return the first URL
            return tunnels[0].get('public_url')
        return None
    except Exception:
        return None

def main():
    print("=" * 60)
    print("Aditya Setu - Starting with ngrok Tunnel")
    print("=" * 60)
    print()
    
    # Check if ngrok is installed
    if not check_ngrok_installed():
        print("ERROR: ngrok is not installed or not in PATH")
        print()
        print("Please install ngrok:")
        print("1. Download from: https://ngrok.com/download")
        print("2. Extract and add to PATH, or place in project directory")
        print("3. Sign up at https://ngrok.com and get your authtoken")
        print("4. Run: ngrok config add-authtoken YOUR_TOKEN")
        print()
        sys.exit(1)
    
    print("[OK] ngrok is installed")
    print()
    
    # Change to project root directory
    project_root = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_root)
    
    print("Starting Aditya Setu server...")
    print()
    
    # Start the server using run.py
    server_process = subprocess.Popen(
        [sys.executable, 'run.py'],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1,
        cwd=project_root
    )
    
    # Wait a bit for server to start
    time.sleep(2)
    
    print("Starting ngrok tunnel...")
    print()
    
    # Start ngrok in a subprocess
    ngrok_process = subprocess.Popen(
        ['ngrok', 'http', '8000'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for ngrok to start
    time.sleep(3)
    
    # Get ngrok URL
    ngrok_url = None
    max_attempts = 10
    for i in range(max_attempts):
        ngrok_url = get_ngrok_url()
        if ngrok_url:
            break
        time.sleep(1)
    
    print("=" * 60)
    print("Server is running!")
    print("=" * 60)
    print()
    print("Local access:    http://localhost:8000")
    if ngrok_url:
        print(f"External access: {ngrok_url}")
        print()
        print("You can now access your server from anywhere using the ngrok URL above!")
    else:
        print("External access: Waiting for ngrok URL...")
        print("Check ngrok web interface: http://127.0.0.1:4040")
    print()
    print("Press Ctrl+C to stop both server and ngrok")
    print()
    
    def signal_handler(sig, frame):
        print("\nShutting down...")
        server_process.terminate()
        ngrok_process.terminate()
        server_process.wait()
        ngrok_process.wait()
        print("Server and ngrok stopped.")
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Monitor server output
    try:
        for line in server_process.stdout:
            print(line, end='')
    except KeyboardInterrupt:
        signal_handler(None, None)

if __name__ == '__main__':
    main()

