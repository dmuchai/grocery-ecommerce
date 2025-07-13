#!/usr/bin/env python3
"""
Simple test script to check if the app can start
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    print("Testing Flask app startup...")
    
    from flask import Flask
    print("✓ Flask imported successfully")
    
    from config import Config
    print("✓ Config imported successfully")
    
    app = Flask(__name__)
    app.config.from_object(Config)
    print("✓ App configured successfully")
    
    @app.route('/')
    def hello():
        return "Hello! Grocery app is working!"
    
    print("✓ Basic route defined")
    print("\nStarting test server...")
    app.run(debug=True, host='0.0.0.0', port=5000)
    
except Exception as e:
    print(f"✗ Error: {e}")
    import traceback
    traceback.print_exc()
