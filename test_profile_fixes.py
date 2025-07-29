#!/usr/bin/env python3
"""
Test script to validate profile page and cart-data fixes
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User
from flask import session

def test_profile_routes():
    """Test the profile routes we just added"""
    
    with app.test_client() as client:
        with app.app_context():
            print("🧪 Testing Profile Routes and Cart Data...")
            
            # Test 1: Profile page without login (should redirect)
            print("\n1️⃣ Testing profile access without login...")
            response = client.get('/user/profile')
            if response.status_code in [302, 401]:
                print("✅ Profile correctly requires login (redirects)")
            else:
                print(f"❌ Expected redirect, got {response.status_code}")
                return False
            
            # Test 2: Test cart-data endpoint
            print("\n2️⃣ Testing cart-data endpoint...")
            response = client.get('/cart-data')
            if response.status_code == 200:
                print("✅ Cart-data endpoint accessible")
                try:
                    data = response.get_json()
                    if 'items' in data:
                        print("✅ Cart-data returns proper JSON structure")
                    else:
                        print("❌ Cart-data missing 'items' key")
                        return False
                except Exception as e:
                    print(f"❌ Cart-data JSON parsing error: {e}")
                    return False
            else:
                print(f"❌ Cart-data endpoint failed: {response.status_code}")
                return False
            
            # Test 3: Create a test user and test profile access
            print("\n3️⃣ Testing profile access with login simulation...")
            try:
                # Create test user
                test_user = User(
                    username="profile_test_user",
                    email="profile.test@example.com",
                    password="hashedpassword123",
                    first_name="Test",
                    last_name="User",
                    phone="+254701234567"
                )
                db.session.add(test_user)
                db.session.commit()
                
                # Simulate login by setting session
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                
                # Test profile page access
                response = client.get('/user/profile')
                if response.status_code == 200:
                    print("✅ Profile page accessible with login")
                    
                    # Check if page contains user data
                    page_content = response.get_data(as_text=True)
                    if 'profile_test_user' in page_content and 'Test User' in page_content:
                        print("✅ Profile page displays user information")
                    else:
                        print("⚠️  Profile page accessible but may not display all user data")
                else:
                    print(f"❌ Profile page failed with login: {response.status_code}")
                    return False
                
                # Cleanup
                db.session.delete(test_user)
                db.session.commit()
                
            except Exception as e:
                print(f"❌ Profile test with login failed: {e}")
                return False
            
            # Test 4: Test User model methods
            print("\n4️⃣ Testing User model enhanced methods...")
            try:
                test_user = User(
                    username="method_test_user",
                    email="method.test@example.com",
                    password="hashedpassword123"
                )
                
                # Test fallback behavior
                fallback_name = test_user.get_full_name()
                if fallback_name == "method_test_user":
                    print("✅ get_full_name() fallback works correctly")
                else:
                    print(f"❌ get_full_name() fallback failed: {fallback_name}")
                    return False
                
                # Test with actual names
                test_user.first_name = "Method"
                test_user.last_name = "Test"
                full_name = test_user.get_full_name()
                if full_name == "Method Test":
                    print("✅ get_full_name() with names works correctly")
                else:
                    print(f"❌ get_full_name() with names failed: {full_name}")
                    return False
                
                # Test profile completion
                incomplete = test_user.has_complete_profile()
                if not incomplete:
                    print("✅ has_complete_profile() correctly identifies incomplete profile")
                else:
                    print("❌ has_complete_profile() should return False for incomplete profile")
                    return False
                
            except Exception as e:
                print(f"❌ User model method testing failed: {e}")
                return False
            
            print("\n🎉 All profile and cart-data tests passed!")
            return True

if __name__ == "__main__":
    if test_profile_routes():
        print("\n✅ Profile routes and fixes are working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
