#!/usr/bin/env python3
"""
PesaPal Credential Checker
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_credentials():
    print("🔍 PesaPal Credential Checker")
    print("=" * 40)
    
    consumer_key = os.getenv('PESAPAL_CONSUMER_KEY')
    consumer_secret = os.getenv('PESAPAL_CONSUMER_SECRET')
    
    if not consumer_key or not consumer_secret:
        print("❌ Missing credentials in .env file!")
        print("Please add:")
        print("PESAPAL_CONSUMER_KEY=your_key_here")
        print("PESAPAL_CONSUMER_SECRET=your_secret_here")
        return
    
    print(f"🔑 Consumer Key: {consumer_key}")
    print(f"🔐 Consumer Secret: {consumer_secret}")
    print()
    
    # Test both sandbox and production URLs (updated with correct endpoints)
    environments = [
        ("Sandbox", "https://cybqa.pesapal.com/pesapalv3"),
        ("Production", "https://pay.pesapal.com/v3")
    ]
    
    for env_name, base_url in environments:
        print(f"🧪 Testing {env_name} environment...")
        print(f"URL: {base_url}")
        
        auth_url = f"{base_url}/api/Auth/RequestToken"
        
        payload = {
            "consumer_key": consumer_key,
            "consumer_secret": consumer_secret
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(auth_url, json=payload, headers=headers, timeout=10)
            print(f"Status Code: {response.status_code}")
            print(f"Response: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                if data.get('token'):
                    print(f"✅ {env_name} authentication successful!")
                    print(f"Token: {data.get('token')[:20]}...")
                else:
                    print(f"❌ {env_name} authentication failed!")
                    if 'error' in data:
                        error = data['error']
                        print(f"Error: {error.get('message', error.get('code', 'Unknown error'))}")
            else:
                print(f"❌ {env_name} request failed with status {response.status_code}")
                
        except requests.exceptions.Timeout:
            print(f"⏰ {env_name} request timed out")
        except requests.exceptions.RequestException as e:
            print(f"🌐 {env_name} network error: {e}")
        except Exception as e:
            print(f"❌ {env_name} unexpected error: {e}")
        
        print("-" * 40)
    
    print("\n💡 Troubleshooting Tips:")
    print("1. Check your PesaPal Developer Portal account")
    print("2. Ensure your credentials are activated")
    print("3. Verify you're using the correct environment (sandbox vs production)")
    print("4. Check if your account has API access enabled")
    print("5. Contact PesaPal support if issues persist")

if __name__ == "__main__":
    check_credentials()
