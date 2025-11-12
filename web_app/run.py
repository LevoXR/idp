#!/usr/bin/env python3
"""
Quick start script for Aditya Setu
Run this from the project root: python run.py
"""
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Change to backend directory for templates/static
os.chdir(os.path.join(os.path.dirname(__file__), 'backend'))

from server import run_server
from models import init_database

if __name__ == '__main__':
    # Initialize database
    print("Initializing database...")
    init_database()
    
    # Get configuration
    port = int(os.environ.get('PORT', 8000))
    host = os.environ.get('HOST', '0.0.0.0')
    
    # Import get_local_ip helper
    import socket
    def get_local_ip():
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            except Exception:
                ip = '127.0.0.1'
            finally:
                s.close()
            return ip
        except Exception:
            return '127.0.0.1'
    
    print(f"Starting Aditya Setu on http://{host}:{port}")
    if host == '0.0.0.0':
        local_ip = get_local_ip()
        print(f"\nServer is accessible from:")
        print(f"  - Local: http://localhost:{port}")
        print(f"  - Network: http://{local_ip}:{port}")
        print(f"\nNote: Make sure your firewall allows connections on port {port}")
        print(f"      Other devices on your network can access: http://{local_ip}:{port}")
    
    # Run server - bind to 0.0.0.0 to allow access from any network interface
    run_server(port, host)

