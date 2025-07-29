#!/usr/bin/env python3
"""
PesaPal API Endpoint Tester
Testing your official Denncathy Enterprises credentials
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_official_credentials():
    print("🎯 Testing Official Denncathy Enterprises PesaPal Credentials")
    print("=" * 60)
    
    # Your official credentials from PesaPal
    consumer_key = "EUhWl3sqfn0SvLhSxyejGh1Vt/3LAg3s"
    consumer_secret = "aa3mvsfopr5kHr/gUIhjw7d8H5c="
    
    print(f"🔑 Consumer Key: {consumer_key}")
    print(f"🔐 Consumer Secret: {consumer_secret}")
    print()
    
    # Test different endpoint variations
    endpoints = [
        ("Sandbox v3", "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"),
        ("Production v3", "https://pay.pesapal.com/v3/api/Auth/RequestToken"),
        ("Alternative Sandbox", "https://demo.pesapal.com/API/PostPesapalDirectOrderV4"),
        ("Alternative Production", "https://www.pesapal.com/API/PostPesapalDirectOrderV4"),
        ("New API Sandbox", "https://cybqa.pesapal.com/pesapalv3/api/Auth/RequestToken"),
        ("New API Production", "https://pay.pesapal.com/pesapalv3/api/Auth/RequestToken"),
    ]
    
    for env_name, auth_url in endpoints:
        print(f"🧪 Testing {env_name}...")
        print(f"URL: {auth_url}")
        
        # Standard payload
        payload = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(auth_url, json=payload, headers=headers, timeout=15)
            print(f"Status Code: {response.status_code}")
            
            # Check if response is JSON
            try:
                data = response.json()
                print(f"JSON Response: {data}")
                
                if response.status_code == 200 and data.get('token'):
                    print(f"✅ {env_name} authentication successful!")
                    print(f"Token: {data.get('token')[:30]}...")
                    return env_name, auth_url.replace('/api/Auth/RequestToken', ''), data.get('token')
                elif 'error' in data:
                    error = data.get('error', {})
                    print(f"❌ {env_name} error: {error.get('message', error.get('code', 'Unknown'))}")
                else:
                    print(f"⚠️  {env_name} unexpected response")
                    
            except ValueError:
                # Not JSON response
                print(f"Non-JSON Response (first 200 chars): {response.text[:200]}")
                if response.status_code == 404:
                    print(f"❌ {env_name} endpoint not found")
                else:
                    print(f"⚠️  {env_name} unexpected format")
                
        except requests.exceptions.Timeout:
            print(f"⏰ {env_name} request timed out")
        except requests.exceptions.RequestException as e:
            print(f"🌐 {env_name} network error: {e}")
        except Exception as e:
            print(f"❌ {env_name} unexpected error: {e}")
        
        print("-" * 50)
    
    print("\n❌ None of the endpoints worked with your credentials.")
    print("\n🔍 Possible reasons:")
    print("1. Credentials need to be activated by PesaPal")
    print("2. These are production credentials (not sandbox)")
    print("3. API endpoint has changed")
    print("4. Account needs additional setup")
    print("\n📞 Next steps:")
    print("1. Contact PesaPal support: developers@pesapal.com")
    print("2. Verify account status in PesaPal merchant portal")
    print("3. Ask about API v3 endpoint requirements")
    
    return None, None, None

def test_ipn_registration_with_working_endpoint(base_url, token):
    """Test IPN registration if we find a working endpoint"""
    print(f"\n🧪 Testing IPN registration with working endpoint...")
    
    # Try different IPN endpoint patterns
    ipn_endpoints = [
        f"{base_url}/api/URLSetup/RegisterIPN",
        f"{base_url}/api/IPN/RegisterIPN",
        f"{base_url}/URLSetup/RegisterIPN"
    ]
    
    for ipn_url in ipn_endpoints:
        print(f"📡 Trying IPN endpoint: {ipn_url}")
        
        payload = {
            "url": "https://denncathy.co.ke/payment/ipn",
            "ipn_notification_type": "GET"
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {token}'
        }
        
        try:
            response = requests.post(ipn_url, json=payload, headers=headers, timeout=10)
            print(f"IPN Status: {response.status_code}")
            print(f"IPN Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ipn_id'):
                    print(f"✅ IPN registered successfully!")
                    print(f"IPN ID: {data.get('ipn_id')}")
                    return data.get('ipn_id')
            
        except Exception as e:
            print(f"IPN Error: {e}")
        
        print("-" * 30)
    
    return None

if __name__ == "__main__":
    env_name, base_url, token = test_official_credentials()
    
    if token and base_url:
        ipn_id = test_ipn_registration_with_working_endpoint(base_url, token)
        if ipn_id:
            print(f"\n🎉 SUCCESS!")
            print(f"Add this to your .env file:")
            print(f"PESAPAL_IPN_ID={ipn_id}")
