#!/usr/bin/env python3
"""
Simple PesaPal IPN Test Script
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_pesapal_connection():
    consumer_key = os.getenv('PESAPAL_CONSUMER_KEY')
    consumer_secret = os.getenv('PESAPAL_CONSUMER_SECRET')
    base_url = 'https://cybqa.pesapal.com/pesapalv3'
    
    print(f"🔑 Consumer Key: {consumer_key[:10]}..." if consumer_key else "❌ No consumer key")
    print(f"🔐 Consumer Secret: {consumer_secret[:10]}..." if consumer_secret else "❌ No consumer secret")
    print(f"🌐 Base URL: {base_url}")
    print()
    
    # Step 1: Get auth token
    auth_url = f"{base_url}/api/Auth/RequestToken"
    
    payload = {
        "consumer_key": consumer_key,
        "consumer_secret": consumer_secret
    }
    
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    
    print("🔐 Getting authentication token...")
    try:
        response = requests.post(auth_url, json=payload, headers=headers)
        print(f"Auth Response Status: {response.status_code}")
        print(f"Auth Response: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            auth_token = data.get('token')
            print(f"✅ Got auth token: {auth_token[:20]}...")
            
            # Step 2: Try to register IPN
            register_url = f"{base_url}/api/URLSetup/RegisterIPN"
            
            ipn_payload = {
                "url": "https://denncathy.co.ke/payment/ipn",
                "ipn_notification_type": "GET"
            }
            
            ipn_headers = {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {auth_token}'
            }
            
            print("\n📡 Registering IPN URL...")
            ipn_response = requests.post(register_url, json=ipn_payload, headers=ipn_headers)
            print(f"IPN Response Status: {ipn_response.status_code}")
            print(f"IPN Response: {ipn_response.text}")
            
            if ipn_response.status_code == 200:
                ipn_data = ipn_response.json()
                print(f"✅ IPN registered successfully!")
                print(f"IPN ID: {ipn_data.get('ipn_id')}")
            else:
                print(f"❌ IPN registration failed")
        else:
            print("❌ Authentication failed")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_pesapal_connection()
