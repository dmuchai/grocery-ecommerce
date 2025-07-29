#!/usr/bin/env python3
"""
Passenger WSGI file for Host Africa hosting
This is the entry point for your Flask application on Host Africa
"""

import sys
import os

# Add your application directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

# Import your Flask application
from app import app as application

# For Host Africa, make sure we're in production mode
if hasattr(application.config, 'update'):
    application.config.update(
        FLASK_ENV='production',
        FLASK_DEBUG=False
    )

# This is what Host Africa will use to run your app
if __name__ == "__main__":
    application.run()
