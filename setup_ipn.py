#!/usr/bin/env python3
"""
PesaPal IPN Setup Script
Run this script once to register your IPN URL with PesaPal and get the IPN ID.
Store the returned IPN ID in your environment variables.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class PesaPalIPNSetup:
    def __init__(self):
        self.consumer_key = os.getenv('PESAPAL_CONSUMER_KEY')
        self.consumer_secret = os.getenv('PESAPAL_CONSUMER_SECRET')
        
        # Use sandbox for testing, production for live
        self.base_url = 'https://cybqa.pesapal.com/pesapalv3'  # Sandbox
        # self.base_url = 'https://pay.pesapal.com/pesapalv3'  # Production
        
        self.auth_token = None
        
    def get_auth_token(self):
        """Get authentication token from PesaPal"""
        auth_url = f"{self.base_url}/api/Auth/RequestToken"
        
        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        try:
            print("🔐 Getting authentication token...")
            response = requests.post(auth_url, json=payload, headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                print("✅ Authentication successful!")
                return self.auth_token
            else:
                print(f"❌ Authentication failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting auth token: {e}")
            return None
    
    def register_ipn_url(self, ipn_url, notification_type="GET"):
        """Register IPN URL with PesaPal - Run this once"""
        if not self.auth_token:
            if not self.get_auth_token():
                return None
                
        register_url = f"{self.base_url}/api/URLSetup/RegisterIPN"
        
        payload = {
            "url": ipn_url,
            "ipn_notification_type": notification_type
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }
        
        try:
            print(f"📡 Registering IPN URL: {ipn_url}")
            response = requests.post(register_url, json=payload, headers=headers)
            
            print(f"🔍 Response Status: {response.status_code}")
            print(f"🔍 Response Text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                ipn_id = data.get('ipn_id')
                print(f"✅ IPN URL registered successfully!")
                print(f"🆔 IPN ID: {ipn_id}")
                return data
            else:
                print(f"❌ IPN registration failed: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error registering IPN: {e}")
            return None
    
    def list_registered_ipns(self):
        """List all registered IPN URLs"""
        if not self.auth_token:
            if not self.get_auth_token():
                return None
                
        list_url = f"{self.base_url}/api/URLSetup/GetIpnList"
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }
        
        try:
            print("📋 Getting list of registered IPNs...")
            response = requests.get(list_url, headers=headers)
            
            print(f"🔍 List Response Status: {response.status_code}")
            print(f"🔍 List Response Text: {response.text}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ IPN list retrieved successfully!")
                return data
            else:
                print(f"❌ Failed to get IPN list: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error getting IPN list: {e}")
            return None

def main():
    """Main setup function"""
    print("🚀 PesaPal IPN Setup for Denncathy Fresh Basket")
    print("=" * 50)
    
    # Check for credentials
    if not os.getenv('PESAPAL_CONSUMER_KEY') or not os.getenv('PESAPAL_CONSUMER_SECRET'):
        print("❌ Missing PesaPal credentials!")
        print("Please set PESAPAL_CONSUMER_KEY and PESAPAL_CONSUMER_SECRET in your .env file")
        return
    
    setup = PesaPalIPNSetup()
    
    # Your IPN URL (update this to match your domain)
    ipn_url = "https://denncathy.co.ke/payment/ipn"
    
    print(f"📍 Domain: {ipn_url}")
    print()
    
    # Option 1: List existing IPNs (commented out for now to focus on registration)
    # print("1️⃣  Checking existing IPN registrations...")
    # existing_ipns = setup.list_registered_ipns()
    
    # if existing_ipns:
    #     print("📋 Existing IPN registrations:")
    #     for ipn in existing_ipns:
    #         print(f"   🆔 ID: {ipn.get('ipn_id')}")
    #         print(f"   🔗 URL: {ipn.get('url')}")
    #         print(f"   📄 Type: {ipn.get('ipn_notification_type')}")
    #         print(f"   📅 Created: {ipn.get('created_date')}")
    #         print()
    
    # Option 2: Register new IPN
    print("1️⃣  Registering new IPN URL...")
    result = setup.register_ipn_url(ipn_url)
    
    if result:
        ipn_id = result.get('ipn_id')
        print()
        print("🎉 SUCCESS! Your IPN has been registered.")
        print("=" * 50)
        print(f"📝 Add this to your .env file:")
        print(f"PESAPAL_IPN_ID={ipn_id}")
        print()
        print("📁 Or update your config_pesapal.py:")
        print(f"'ipn_id': '{ipn_id}',")
        print()
        print("⚠️  IMPORTANT: Save this IPN ID! You'll need it for all transactions.")
    else:
        print("❌ Failed to register IPN URL")

if __name__ == "__main__":
    main()
