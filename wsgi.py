#!/usr/bin/env python3
"""
WSGI entry point for production deployment
"""
import sys
import os

# Add your application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask application
from app import app as application

if __name__ == "__main__":
    application.run()
