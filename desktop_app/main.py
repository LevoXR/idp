#!/usr/bin/env python3
"""
Main entry point for Aditya Setu Desktop Application
"""
import sys
import os

# Add the desktop_app directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models import init_database
from gui.main_window import MainWindow


def main():
    """Main application entry point"""
    # Initialize database
    print("Initializing database...")
    init_database()
    
    # Create and run the main window
    print("Starting application...")
    app = MainWindow()
    app.run()


if __name__ == '__main__':
    main()


