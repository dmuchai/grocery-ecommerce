#!/usr/bin/env python3
"""Quick debug script to test PesaPal integration on production"""
import os
from dotenv import load_dotenv
import requests

load_dotenv()

# Print environment variables (masked)
print("=== Environment Check ===")
print(f"PESAPAL_BASE_URL: {os.getenv('PESAPAL_BASE_URL')}")
print(f"PESAPAL_CONSUMER_KEY: {os.getenv('PESAPAL_CONSUMER_KEY', '')[:10]}...")
print(f"PESAPAL_CONSUMER_SECRET: {'SET' if os.getenv('PESAPAL_CONSUMER_SECRET') else 'NOT SET'}")
print(f"PESAPAL_IPN_ID: {os.getenv('PESAPAL_IPN_ID')}")
print(f"PESAPAL_CALLBACK_URL: {os.getenv('PESAPAL_CALLBACK_URL')}")
print()

# Test PesaPal authentication
print("=== Testing PesaPal Auth ===")
base_url = os.getenv('PESAPAL_BASE_URL', 'https://pay.pesapal.com/v3')
consumer_key = os.getenv('PESAPAL_CONSUMER_KEY')
consumer_secret = os.getenv('PESAPAL_CONSUMER_SECRET')

auth_url = f"{base_url}/api/Auth/RequestToken"
payload = {
    "consumer_key": consumer_key,
    "consumer_secret": consumer_secret
}

try:
    response = requests.post(auth_url, json=payload, headers={'Content-Type': 'application/json'})
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")
    
    if response.status_code == 200:
        data = response.json()
        token = data.get('token', '')
        print(f"\n✓ Auth successful! Token length: {len(token)}")
    else:
        print(f"\n✗ Auth failed!")
        
except Exception as e:
    print(f"✗ Error: {e}")
