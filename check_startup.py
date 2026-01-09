#!/usr/bin/env python3
"""
Quick diagnostic script to check if the app can start
Run this on the server to identify startup issues
"""
import sys
import os

print("=" * 60)
print("Flask App Startup Diagnostic")
print("=" * 60)

# Test 1: Basic imports
print("\n1. Testing basic imports...")
try:
    from flask import Flask
    print("   ✓ Flask imported")
except Exception as e:
    print(f"   ✗ Flask import failed: {e}")
    sys.exit(1)

# Test 2: Config import
print("\n2. Testing config import...")
try:
    from config import Config
    print("   ✓ Config imported")
except Exception as e:
    print(f"   ✗ Config import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

# Test 3: Database connection
print("\n3. Testing database connection...")
try:
    from models import db
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    with app.app_context():
        db.engine.connect()
    print("   ✓ Database connection successful")
except Exception as e:
    print(f"   ✗ Database connection failed: {e}")
    import traceback
    traceback.print_exc()

# Test 4: Model imports
print("\n4. Testing model imports...")
try:
    from models.order import Order
    print("   ✓ Order model imported")
    from models.user import User
    print("   ✓ User model imported")
except Exception as e:
    print(f"   ✗ Model import failed: {e}")
    import traceback
    traceback.print_exc()

# Test 5: Route imports
print("\n5. Testing route imports...")
try:
    from routes.payment import payment_bp
    print("   ✓ Payment routes imported")
except Exception as e:
    print(f"   ✗ Route import failed: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Error handlers
print("\n6. Testing error handlers...")
try:
    from utils.error_handlers import register_error_handlers, setup_logging
    print("   ✓ Error handlers imported")
except Exception as e:
    print(f"   ✗ Error handlers import failed: {e}")
    import traceback
    traceback.print_exc()

# Test 7: Template files
print("\n7. Testing template files...")
template_files = [
    'templates/errors/404.html',
    'templates/errors/500.html',
    'templates/errors/403.html',
    'templates/payment/success.html',
]
for template in template_files:
    if os.path.exists(template):
        print(f"   ✓ {template} exists")
    else:
        print(f"   ✗ {template} MISSING!")

# Test 8: Full app import
print("\n8. Testing full app import...")
try:
    import app
    print("   ✓ App module imported successfully")
except Exception as e:
    print(f"   ✗ App import failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("Diagnostic complete!")
print("=" * 60)
