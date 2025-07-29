#!/usr/bin/env python3
"""
Test PesaPal Configuration on Host Africa Server
"""

import os
from dotenv import load_dotenv

def test_pesapal_config():
    print("🔧 Testing PesaPal Configuration...")
    print("=" * 50)
    
    # Load environment variables
    load_dotenv()
    
    # Check each PesaPal environment variable
    config_items = [
        ('PESAPAL_CONSUMER_KEY', 'Consumer Key'),
        ('PESAPAL_CONSUMER_SECRET', 'Consumer Secret'),
        ('PESAPAL_BASE_URL', 'Base URL'),
        ('PESAPAL_IPN_ID', 'IPN ID'),
        ('PESAPAL_CALLBACK_URL', 'Callback URL'),
        ('PESAPAL_NOTIFICATION_URL', 'Notification URL')
    ]
    
    all_configured = True
    
    for env_var, display_name in config_items:
        value = os.getenv(env_var)
        if value:
            # Mask sensitive values
            if 'KEY' in env_var or 'SECRET' in env_var:
                masked_value = value[:8] + "..." if len(value) > 8 else "***"
                print(f"✅ {display_name}: {masked_value}")
            else:
                print(f"✅ {display_name}: {value}")
        else:
            print(f"❌ {display_name}: Not configured")
            all_configured = False
    
    print("=" * 50)
    
    if all_configured:
        print("🎉 All PesaPal configuration is complete!")
        print("💡 Ready for payment processing")
    else:
        print("⚠️  Some PesaPal configuration is missing")
        print("💡 Add missing values to your .env file")
    
    # Test import from config_pesapal
    try:
        from config_pesapal import PESAPAL_CONFIG
        print("✅ config_pesapal.py imports successfully")
        print(f"✅ PESAPAL_CONFIG base_url: {PESAPAL_CONFIG.get('base_url', 'Not set')}")
    except ImportError as e:
        print(f"❌ config_pesapal.py import error: {e}")
    
    return all_configured

if __name__ == "__main__":
    test_pesapal_config()
