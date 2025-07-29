#!/usr/bin/env python3
"""
Add missing PesaPal URLs to .env file
"""

def add_pesapal_urls():
    print("🔧 Adding missing PesaPal URLs to .env file...")
    
    # Read current .env
    try:
        with open('.env', 'r') as f:
            content = f.read()
    except FileNotFoundError:
        print("❌ .env file not found!")
        return False
    
    # URLs to add
    missing_urls = []
    
    # Check if callback URL exists
    if 'PESAPAL_CALLBACK_URL=' not in content:
        missing_urls.append('PESAPAL_CALLBACK_URL=https://denncathy.co.ke/payment/callback')
    
    # Check if notification URL exists  
    if 'PESAPAL_NOTIFICATION_URL=' not in content:
        missing_urls.append('PESAPAL_NOTIFICATION_URL=https://denncathy.co.ke/payment/ipn')
    
    if missing_urls:
        # Add the missing URLs to the PesaPal section
        pesapal_section = "# 🏦 PesaPal Production Configuration"
        if pesapal_section in content:
            # Find the end of the PesaPal section
            lines = content.split('\n')
            insert_index = -1
            
            for i, line in enumerate(lines):
                if pesapal_section in line:
                    # Find the next empty line or different section
                    for j in range(i + 1, len(lines)):
                        if lines[j].strip() == '' or lines[j].startswith('# '):
                            insert_index = j
                            break
                    break
            
            if insert_index != -1:
                # Insert the missing URLs
                for url in missing_urls:
                    lines.insert(insert_index, url)
                    insert_index += 1
                
                content = '\n'.join(lines)
            else:
                # Append to end of file
                content += '\n' + '\n'.join(missing_urls)
        else:
            # Add PesaPal section
            content += f'\n\n{pesapal_section}\n' + '\n'.join(missing_urls)
        
        # Write back to .env
        with open('.env', 'w') as f:
            f.write(content)
        
        print("✅ Added missing PesaPal URLs:")
        for url in missing_urls:
            print(f"   + {url}")
        return True
    else:
        print("ℹ️  All PesaPal URLs already configured")
        return False

if __name__ == "__main__":
    add_pesapal_urls()
