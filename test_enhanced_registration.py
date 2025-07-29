#!/usr/bin/env python3
"""
Test script for enhanced registration form
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User

def test_enhanced_registration():
    """Test the enhanced registration form with profile fields"""
    
    with app.test_client() as client:
        with app.app_context():
            print("🧪 Testing Enhanced Registration Form...")
            
            # Test 1: Basic registration (required fields only)
            print("\n1️⃣ Testing basic registration...")
            response = client.post('/user/register', data={
                'username': 'testuser_basic',
                'email': 'basic@test.com',
                'password': 'TestPass123'
            })
            
            if response.status_code in [200, 302]:  # Success or redirect
                user = User.query.filter_by(username='testuser_basic').first()
                if user:
                    print("✅ Basic registration successful")
                    print(f"   Profile completed: {user.profile_completed}")
                    print(f"   Full name: {user.get_full_name()}")
                    db.session.delete(user)
                    db.session.commit()
                else:
                    print("❌ User not created")
                    return False
            else:
                print(f"❌ Registration failed with status {response.status_code}")
                return False
            
            # Test 2: Complete registration (all fields)
            print("\n2️⃣ Testing complete registration...")
            response = client.post('/user/register', data={
                'username': 'testuser_complete',
                'email': 'complete@test.com',
                'password': 'TestPass123',
                'first_name': 'John',
                'last_name': 'Doe',
                'phone': '+254701234567',
                'address': '123 Test Street',
                'city': 'Nairobi',
                'state': 'Nairobi County',
                'postal_code': '00100',
                'country': 'Kenya'
            })
            
            if response.status_code in [200, 302]:
                user = User.query.filter_by(username='testuser_complete').first()
                if user:
                    print("✅ Complete registration successful")
                    print(f"   Profile completed: {user.profile_completed}")
                    print(f"   Full name: {user.get_full_name()}")
                    print(f"   Full address: {user.get_full_address()}")
                    db.session.delete(user)
                    db.session.commit()
                else:
                    print("❌ Complete user not created")
                    return False
            else:
                print(f"❌ Complete registration failed with status {response.status_code}")
                return False
            
            # Test 3: Partial registration (some optional fields)
            print("\n3️⃣ Testing partial registration...")
            response = client.post('/user/register', data={
                'username': 'testuser_partial',
                'email': 'partial@test.com',
                'password': 'TestPass123',
                'first_name': 'Jane',
                'last_name': 'Smith',
                'phone': '+254700000000'
                # No address fields
            })
            
            if response.status_code in [200, 302]:
                user = User.query.filter_by(username='testuser_partial').first()
                if user:
                    print("✅ Partial registration successful")
                    print(f"   Profile completed: {user.profile_completed}")
                    print(f"   Full name: {user.get_full_name()}")
                    print(f"   Has address: {bool(user.address)}")
                    db.session.delete(user)
                    db.session.commit()
                else:
                    print("❌ Partial user not created")
                    return False
            else:
                print(f"❌ Partial registration failed with status {response.status_code}")
                return False
            
            # Test 4: Validation errors
            print("\n4️⃣ Testing validation errors...")
            
            # Missing required fields
            response = client.post('/user/register', data={
                'username': '',
                'email': 'test@test.com',
                'password': 'TestPass123'
            })
            
            if response.status_code == 400:
                print("✅ Missing username validation works")
            else:
                print(f"❌ Missing username validation failed: {response.status_code}")
                return False
            
            # Invalid email
            response = client.post('/user/register', data={
                'username': 'testuser',
                'email': 'invalid-email',
                'password': 'TestPass123'
            })
            
            if response.status_code == 400:
                print("✅ Invalid email validation works")
            else:
                print(f"❌ Invalid email validation failed: {response.status_code}")
                return False
            
            # Weak password
            response = client.post('/user/register', data={
                'username': 'testuser',
                'email': 'test@test.com',
                'password': 'weak'
            })
            
            if response.status_code == 400:
                print("✅ Weak password validation works")
            else:
                print(f"❌ Weak password validation failed: {response.status_code}")
                return False
            
            print("\n🎉 All enhanced registration tests passed!")
            return True

if __name__ == "__main__":
    if test_enhanced_registration():
        print("\n✅ Enhanced registration form is working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Enhanced registration tests failed!")
        sys.exit(1)
