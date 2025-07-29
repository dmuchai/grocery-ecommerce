#!/usr/bin/env python3
"""
Fix PesaPal URL in .env file for production
"""

def fix_pesapal_url():
    print("🔧 Fixing PesaPal URL in .env file...")
    
    # Read current .env
    with open('.env', 'r') as f:
        content = f.read()
    
    # Replace the URL - Actually, v3 is the correct production URL format
    old_url = "PESAPAL_BASE_URL=https://pay.pesapal.com/pesapalv3"
    new_url = "PESAPAL_BASE_URL=https://pay.pesapal.com/v3"
    
    if old_url in content:
        content = content.replace(old_url, new_url)
        
        # Write back to .env
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Updated PesaPal URL to correct production format")
        print("   Changed: https://pay.pesapal.com/pesapalv3")
        print("   To:      https://pay.pesapal.com/v3")
        return True
    else:
        print("ℹ️  PesaPal URL already in correct format or not found")
        return False

if __name__ == "__main__":
    fix_pesapal_url()
