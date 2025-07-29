#!/usr/bin/env python3
"""
Test PesaPal Configuration
"""

from config_pesapal import PESAPAL_CONFIG

print("=" * 50)
print("PESAPAL CONFIGURATION TEST")
print("=" * 50)

print(f"Consumer Key: {PESAPAL_CONFIG['consumer_key'][:10]}...")
print(f"Consumer Secret: {PESAPAL_CONFIG['consumer_secret'][:10]}...")
print(f"IPN ID: {PESAPAL_CONFIG['ipn_id']}")
print(f"Base URL: {PESAPAL_CONFIG['base_url']}")
print(f"Auth URL: {PESAPAL_CONFIG['base_url']}{PESAPAL_CONFIG['auth_url']}")
print(f"Submit Order URL: {PESAPAL_CONFIG['base_url']}{PESAPAL_CONFIG['submit_order_url']}")
print(f"Callback URL: {PESAPAL_CONFIG['callback_url']}")
print(f"Notification URL: {PESAPAL_CONFIG['notification_url']}")

print("\n" + "=" * 50)
if PESAPAL_CONFIG['consumer_key'] and PESAPAL_CONFIG['consumer_secret'] and PESAPAL_CONFIG['ipn_id']:
    print("✅ Configuration is complete and ready!")
    print("✅ You can now process payments through PesaPal!")
else:
    print("❌ Configuration incomplete:")
    if not PESAPAL_CONFIG['consumer_key']:
        print("  - Missing Consumer Key")
    if not PESAPAL_CONFIG['consumer_secret']:
        print("  - Missing Consumer Secret")
    if not PESAPAL_CONFIG['ipn_id']:
        print("  - Missing IPN ID")

print("=" * 50)
