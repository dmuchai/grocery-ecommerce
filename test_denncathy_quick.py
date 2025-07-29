#!/usr/bin/env python3
"""
Quick Production Test for denncathy.co.ke after migration
"""

import requests
import sys

def test_site():
    print("🧪 Testing denncathy.co.ke after migration...")
    
    base_url = "https://denncathy.co.ke"
    
    tests = [
        ("Homepage", "/"),
        ("Registration Page", "/user/register"),
        ("Products", "/products"),
        ("About", "/about"),
        ("Contact", "/contact"),
        ("Login", "/user/login")
    ]
    
    all_passed = True
    
    for name, path in tests:
        try:
            url = f"{base_url}{path}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                print(f"✅ {name}: Working")
            elif response.status_code in [301, 302]:
                print(f"🔄 {name}: Redirect (normal)")
            else:
                print(f"❌ {name}: Status {response.status_code}")
                all_passed = False
                
        except Exception as e:
            print(f"❌ {name}: Error - {e}")
            all_passed = False
    
    # Test enhanced registration form specifically
    try:
        response = requests.get(f"{base_url}/user/register", timeout=10)
        if response.status_code == 200:
            content = response.text.lower()
            
            enhanced_features = [
                ('first_name', 'name="first_name"' in content),
                ('phone', 'name="phone"' in content),
                ('address', 'name="address"' in content),
                ('country', 'name="country"' in content),
                ('profile_section', 'profile information' in content),
                ('address_section', 'address information' in content)
            ]
            
            print("\n📝 Enhanced Registration Form Check:")
            for feature, exists in enhanced_features:
                status = "✅" if exists else "❌"
                print(f"  {feature}: {status}")
                all_passed = all_passed and exists
                
    except Exception as e:
        print(f"❌ Registration form check failed: {e}")
        all_passed = False
    
    print("\n" + "="*50)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ denncathy.co.ke is ready with enhanced features!")
    else:
        print("⚠️  Some tests failed - check above")
    print("="*50)
    
    return all_passed

if __name__ == "__main__":
    success = test_site()
    sys.exit(0 if success else 1)
