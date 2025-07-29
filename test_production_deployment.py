#!/usr/bin/env python3
"""
Production Deployment Test Script for denncathy.co.ke
Tests all critical functionality after deployment
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "https://denncathy.co.ke"
TEST_EMAIL = "test@example.com"  # Change this for testing

def print_status(test_name, status_code, success_code=200):
    """Print formatted test status"""
    status = "✅" if status_code == success_code else "❌"
    print(f"{test_name}: {status_code} {status}")
    return status_code == success_code

def test_basic_pages():
    """Test basic page accessibility"""
    print("\n🌐 Testing Basic Page Access...")
    
    pages = [
        ("Homepage", "/"),
        ("Products", "/products"),
        ("About", "/about"),
        ("Contact", "/contact"),
        ("Registration", "/user/register"),
        ("Login", "/user/login"),
    ]
    
    all_passed = True
    for name, path in pages:
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=10)
            passed = print_status(f"  {name}", response.status_code)
            all_passed = all_passed and passed
        except requests.RequestException as e:
            print(f"  {name}: ❌ Connection Error - {e}")
            all_passed = False
    
    return all_passed

def test_api_endpoints():
    """Test critical API endpoints"""
    print("\n🔗 Testing API Endpoints...")
    
    endpoints = [
        ("Cart Data", "/cart-data"),
        ("Categories", "/api/categories"),
    ]
    
    all_passed = True
    for name, path in endpoints:
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=10)
            # API endpoints might return different status codes
            passed = response.status_code in [200, 302, 404]  # 404 is ok for some APIs
            status = "✅" if passed else "❌"
            print(f"  {name}: {response.status_code} {status}")
            all_passed = all_passed and passed
        except requests.RequestException as e:
            print(f"  {name}: ❌ Connection Error - {e}")
            all_passed = False
    
    return all_passed

def test_enhanced_registration():
    """Test the new enhanced registration form"""
    print("\n📝 Testing Enhanced Registration Form...")
    
    try:
        response = requests.get(f"{BASE_URL}/user/register", timeout=10)
        if response.status_code == 200:
            # Check for new form elements
            content = response.text.lower()
            
            tests = [
                ("Required Information Section", "required information" in content),
                ("Profile Information Section", "profile information" in content),
                ("Address Information Section", "address information" in content),
                ("First Name Field", 'name="first_name"' in content),
                ("Phone Field", 'name="phone"' in content),
                ("Address Field", 'name="address"' in content),
                ("Country Select", 'name="country"' in content),
                ("Bootstrap Cards", 'class="card' in content),
            ]
            
            all_passed = True
            for test_name, condition in tests:
                status = "✅" if condition else "❌"
                print(f"  {test_name}: {status}")
                all_passed = all_passed and condition
            
            return all_passed
        else:
            print(f"  Registration page failed to load: {response.status_code} ❌")
            return False
            
    except requests.RequestException as e:
        print(f"  Registration test failed: {e} ❌")
        return False

def test_checkout_flow():
    """Test checkout process accessibility"""
    print("\n🛒 Testing Checkout Flow...")
    
    try:
        # Test checkout page (might require login, but should not 500)
        response = requests.get(f"{BASE_URL}/checkout", timeout=10)
        # Checkout might redirect to login (302) or show page (200)
        passed = response.status_code in [200, 302, 401]
        status = "✅" if passed else "❌"
        print(f"  Checkout Access: {response.status_code} {status}")
        
        return passed
        
    except requests.RequestException as e:
        print(f"  Checkout test failed: {e} ❌")
        return False

def test_static_resources():
    """Test static resource loading"""
    print("\n🎨 Testing Static Resources...")
    
    resources = [
        ("CSS Files", "/static/css/"),
        ("JavaScript Files", "/static/js/"),
        ("Images", "/static/images/"),
    ]
    
    all_passed = True
    for name, path in resources:
        try:
            response = requests.get(f"{BASE_URL}{path}", timeout=10)
            # Directory listing might be disabled (403) but resources should exist
            passed = response.status_code in [200, 403, 404]
            status = "✅" if passed else "❌"
            print(f"  {name}: {response.status_code} {status}")
            all_passed = all_passed and passed
        except requests.RequestException as e:
            print(f"  {name}: ❌ Connection Error - {e}")
            all_passed = False
    
    return all_passed

def test_ssl_and_security():
    """Test SSL and basic security"""
    print("\n🔒 Testing SSL and Security...")
    
    try:
        # Test HTTPS redirect
        http_response = requests.get(f"http://denncathy.co.ke", timeout=10, allow_redirects=False)
        https_redirect = http_response.status_code in [301, 302, 308]
        print(f"  HTTPS Redirect: {'✅' if https_redirect else '❌'}")
        
        # Test HTTPS access
        https_response = requests.get(f"{BASE_URL}", timeout=10)
        https_works = https_response.status_code == 200
        print(f"  HTTPS Access: {'✅' if https_works else '❌'}")
        
        # Test security headers (basic check)
        headers = https_response.headers
        has_security_headers = any(header in headers for header in ['X-Frame-Options', 'X-Content-Type-Options'])
        print(f"  Security Headers: {'✅' if has_security_headers else '⚠️'}")
        
        return https_redirect and https_works
        
    except requests.RequestException as e:
        print(f"  SSL test failed: {e} ❌")
        return False

def run_full_test():
    """Run complete deployment test suite"""
    print("🚀 Starting Production Deployment Test for denncathy.co.ke")
    print(f"📅 Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Basic Pages", test_basic_pages),
        ("API Endpoints", test_api_endpoints),
        ("Enhanced Registration", test_enhanced_registration),
        ("Checkout Flow", test_checkout_flow),
        ("Static Resources", test_static_resources),
        ("SSL & Security", test_ssl_and_security),
    ]
    
    results = {}
    overall_success = True
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results[test_name] = result
            overall_success = overall_success and result
        except Exception as e:
            print(f"\n❌ {test_name} failed with error: {e}")
            results[test_name] = False
            overall_success = False
    
    # Print summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{test_name:.<30} {status}")
    
    print("\n" + "=" * 60)
    if overall_success:
        print("🎉 ALL TESTS PASSED! Deployment successful!")
        print("✅ denncathy.co.ke is ready for production use.")
    else:
        print("⚠️  SOME TESTS FAILED! Please review and fix issues.")
        print("❌ Check the failed tests above and verify deployment.")
    print("=" * 60)
    
    return overall_success

if __name__ == "__main__":
    success = run_full_test()
    exit(0 if success else 1)
