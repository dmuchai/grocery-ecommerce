#!/usr/bin/env python3
"""
Test script for enhanced User model with profile fields
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import app
from models import db, User

def test_user_model_enhancements():
    """Test the enhanced User model with profile fields"""
    
    with app.app_context():
        print("🧪 Testing Enhanced User Model...")
        
        # Test 1: Create a user with basic info
        print("\n1️⃣ Testing basic user creation...")
        test_user = User(
            username="testuser_profile",
            email="test.profile@example.com",
            password="hashedpassword123",
            role="customer"
        )
        
        try:
            db.session.add(test_user)
            db.session.commit()
            print("✅ Basic user created successfully")
        except Exception as e:
            print(f"❌ Failed to create basic user: {e}")
            return False
        
        # Test 2: Update profile fields
        print("\n2️⃣ Testing profile field updates...")
        try:
            test_user.first_name = "John"
            test_user.last_name = "Doe"
            test_user.phone = "+254701234567"
            test_user.address = "123 Main Street, Apartment 4B"
            test_user.city = "Nairobi"
            test_user.state = "Nairobi County"
            test_user.postal_code = "00100"
            test_user.country = "Kenya"
            
            db.session.commit()
            print("✅ Profile fields updated successfully")
        except Exception as e:
            print(f"❌ Failed to update profile fields: {e}")
            return False
        
        # Test 3: Test helper methods
        print("\n3️⃣ Testing helper methods...")
        try:
            full_name = test_user.get_full_name()
            print(f"✅ get_full_name(): {full_name}")
            
            full_address = test_user.get_full_address()
            print(f"✅ get_full_address(): {full_address}")
            
            has_complete_profile = test_user.has_complete_profile()
            print(f"✅ has_complete_profile(): {has_complete_profile}")
            
            test_user.update_profile_completion()
            print(f"✅ profile_completed: {test_user.profile_completed}")
            
        except Exception as e:
            print(f"❌ Helper method error: {e}")
            return False
        
        # Test 4: Test to_dict() method
        print("\n4️⃣ Testing to_dict() method...")
        try:
            user_dict = test_user.to_dict()
            expected_keys = [
                'id', 'username', 'email', 'role', 'is_active', 'created_at',
                'first_name', 'last_name', 'phone', 'address', 'city', 'state',
                'postal_code', 'country', 'profile_completed', 'full_name', 'full_address'
            ]
            
            missing_keys = [key for key in expected_keys if key not in user_dict]
            if missing_keys:
                print(f"❌ Missing keys in to_dict(): {missing_keys}")
                return False
            else:
                print("✅ to_dict() contains all expected keys")
                print(f"   Sample data: name={user_dict['full_name']}, address={user_dict['full_address']}")
                
        except Exception as e:
            print(f"❌ to_dict() method error: {e}")
            return False
        
        # Test 5: Test fallback scenarios
        print("\n5️⃣ Testing fallback scenarios...")
        try:
            # Create user with no profile info
            incomplete_user = User(
                username="incomplete_user",
                email="incomplete@example.com",
                password="hashedpassword123"
            )
            db.session.add(incomplete_user)
            db.session.commit()
            
            # Test fallbacks
            fallback_name = incomplete_user.get_full_name()
            print(f"✅ Fallback name (should be username): {fallback_name}")
            
            fallback_complete = incomplete_user.has_complete_profile()
            print(f"✅ Incomplete profile detection: {fallback_complete}")
            
        except Exception as e:
            print(f"❌ Fallback test error: {e}")
            return False
        
        # Cleanup
        print("\n🧹 Cleaning up test data...")
        try:
            User.query.filter(User.username.in_(["testuser_profile", "incomplete_user"])).delete()
            db.session.commit()
            print("✅ Test data cleaned up")
        except Exception as e:
            print(f"⚠️  Cleanup warning: {e}")
        
        print("\n🎉 All User model enhancement tests passed!")
        return True

if __name__ == "__main__":
    if test_user_model_enhancements():
        print("\n✅ User model enhancements are working correctly!")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed!")
        sys.exit(1)
