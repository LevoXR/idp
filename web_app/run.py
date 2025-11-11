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
    
    print(f"Starting Aditya Setu on http://localhost:{port}")
    
    # Run server
    run_server(port)

