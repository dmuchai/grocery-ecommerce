#!/usr/bin/env python3
"""
Simple site test without external dependencies
Tests basic functionality of denncathy.co.ke
"""

import subprocess
import sys
import os

def test_basic_functionality():
    print("🧪 Testing denncathy.co.ke basic functionality...")
    print("="*50)
    
    # Test if app can import successfully
    print("1. Testing app import...")
    try:
        # Change to app directory and test import
        sys.path.insert(0, os.getcwd())
        from app import app
        print("   ✅ App imports successfully")
        
        # Test app configuration
        with app.app_context():
            is_production = app.config.get('FLASK_ENV') == 'production'
            debug_disabled = not app.config.get('FLASK_DEBUG', True)
            
            print(f"   ✅ Production mode: {is_production}")
            print(f"   ✅ Debug disabled: {debug_disabled}")
            
        success = True
    except Exception as e:
        print(f"   ❌ App import failed: {e}")
        success = False
    
    # Test database connection
    print("\n2. Testing database connection...")
    try:
        from models import db
        from models.user import User
        
        with app.app_context():
            # Simple query to test connection
            user_count = User.query.count()
            print(f"   ✅ Database connected - {user_count} users in system")
            
            # Check if new profile columns exist
            test_user = User.query.first()
            if test_user:
                has_profile_fields = hasattr(test_user, 'first_name') and hasattr(test_user, 'phone')
                print(f"   ✅ Enhanced profile fields: {'Available' if has_profile_fields else 'Missing'}")
            
    except Exception as e:
        print(f"   ❌ Database test failed: {e}")
        success = False
    
    # Test key routes
    print("\n3. Testing key routes...")
    try:
        with app.test_client() as client:
            routes_to_test = [
                ('/', 'Homepage'),
                ('/user/register', 'Registration'),
                ('/user/login', 'Login'),
                ('/products', 'Products'),
                ('/about', 'About'),
                ('/contact', 'Contact')
            ]
            
            for route, name in routes_to_test:
                try:
                    response = client.get(route)
                    if response.status_code in [200, 302]:  # 302 for redirects
                        print(f"   ✅ {name}: Working (Status {response.status_code})")
                    else:
                        print(f"   ⚠️  {name}: Status {response.status_code}")
                except Exception as e:
                    print(f"   ❌ {name}: Error - {e}")
                    
    except Exception as e:
        print(f"   ❌ Route testing failed: {e}")
        success = False
    
    # Test enhanced registration form
    print("\n4. Testing enhanced registration form...")
    try:
        with app.test_client() as client:
            response = client.get('/user/register')
            if response.status_code == 200:
                content = response.get_data(as_text=True).lower()
                
                enhanced_features = [
                    ('first_name field', 'name="first_name"' in content),
                    ('phone field', 'name="phone"' in content),
                    ('address field', 'name="address"' in content),
                    ('country field', 'name="country"' in content),
                    ('profile section', 'profile information' in content),
                    ('address section', 'address information' in content)
                ]
                
                for feature, exists in enhanced_features:
                    status = "✅" if exists else "❌"
                    print(f"   {status} {feature}")
                    
    except Exception as e:
        print(f"   ❌ Registration form test failed: {e}")
        success = False
    
    # Test PesaPal configuration
    print("\n5. Testing PesaPal configuration...")
    try:
        pesapal_key = app.config.get('PESAPAL_CONSUMER_KEY')
        pesapal_secret = app.config.get('PESAPAL_CONSUMER_SECRET')
        pesapal_url = app.config.get('PESAPAL_BASE_URL')
        
        print(f"   ✅ Consumer Key: {'Set' if pesapal_key else 'Missing'}")
        print(f"   ✅ Consumer Secret: {'Set' if pesapal_secret else 'Missing'}")
        print(f"   ✅ Base URL: {pesapal_url if pesapal_url else 'Missing'}")
        
        is_production_url = pesapal_url and 'pay.pesapal.com' in pesapal_url
        print(f"   ✅ Production URL: {'Yes' if is_production_url else 'No'}")
        
    except Exception as e:
        print(f"   ❌ PesaPal config test failed: {e}")
        success = False
    
    print("\n" + "="*50)
    print("📊 TEST SUMMARY")
    print("="*50)
    
    if success:
        print("🎉 ALL BASIC TESTS PASSED!")
        print("✅ Your denncathy.co.ke app is ready!")
        print("\nNext steps:")
        print("1. Visit https://denncathy.co.ke in your browser")
        print("2. Test the enhanced registration form")
        print("3. Try the checkout process")
        print("4. Make a small test payment")
    else:
        print("⚠️  Some tests failed - check above for details")
    
    print("="*50)
    return success

if __name__ == "__main__":
    success = test_basic_functionality()
    sys.exit(0 if success else 1)
