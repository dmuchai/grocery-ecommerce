#!/usr/bin/env python3
"""
Production Environment Checker for Host Africa
Verifies all settings are production-ready
"""

import os
import sys

def check_production_readiness():
    print("🔍 Checking Production Environment...")
    print("="*50)
    
    issues = []
    warnings = []
    
    # Check .env file exists
    if os.path.exists('.env'):
        print("✅ .env file found")
        
        # Read and check key settings
        with open('.env', 'r') as f:
            env_content = f.read()
        
        # Critical production checks
        checks = [
            ('FLASK_ENV=production', 'FLASK_ENV should be production'),
            ('FLASK_DEBUG=False', 'FLASK_DEBUG should be False'),
            ('PESAPAL_BASE_URL=https://pay.pesapal.com/v3', 'PesaPal should use production URL'),
            ('SECRET_KEY=', 'SECRET_KEY should be set'),
            ('DATABASE_', 'Database credentials should be configured')
        ]
        
        for check, message in checks:
            if check.split('=')[0] in env_content:
                if check in env_content:
                    print(f"✅ {message}")
                else:
                    if 'FLASK_DEBUG=True' in env_content:
                        issues.append("❌ FLASK_DEBUG is True (should be False for production)")
                    elif 'FLASK_ENV=development' in env_content:
                        issues.append("❌ FLASK_ENV is development (should be production)")
                    elif 'cybqa.pesapal.com' in env_content:
                        issues.append("❌ Using PesaPal sandbox (should use production URL)")
                    else:
                        warnings.append(f"⚠️  {message} - please verify")
            else:
                warnings.append(f"⚠️  {message} - not found in .env")
    else:
        issues.append("❌ .env file not found")
    
    # Check file permissions (basic)
    if os.path.exists('app.py'):
        stat = os.stat('app.py')
        if oct(stat.st_mode)[-3:] == '644':
            print("✅ File permissions look correct")
        else:
            warnings.append("⚠️  Check file permissions (should be 644 for files)")
    
    # Check if required files exist
    required_files = [
        'app.py', 'config.py', 'wsgi.py', 'requirements.txt',
        'passenger_wsgi.py'  # Host Africa specific
    ]
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file} exists")
        else:
            if file == 'passenger_wsgi.py':
                warnings.append(f"⚠️  {file} missing (may be needed for Host Africa)")
            else:
                issues.append(f"❌ {file} missing")
    
    # Check directory structure
    required_dirs = ['routes', 'templates', 'static', 'models']
    for dir in required_dirs:
        if os.path.exists(dir):
            print(f"✅ {dir}/ directory exists")
        else:
            issues.append(f"❌ {dir}/ directory missing")
    
    print("\n" + "="*50)
    print("📊 PRODUCTION READINESS SUMMARY")
    print("="*50)
    
    if issues:
        print("🚨 CRITICAL ISSUES:")
        for issue in issues:
            print(f"  {issue}")
    
    if warnings:
        print("\n⚠️  WARNINGS:")
        for warning in warnings:
            print(f"  {warning}")
    
    if not issues and not warnings:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Production environment is ready!")
    elif not issues:
        print("✅ No critical issues found")
        print("⚠️  Please review warnings above")
    else:
        print("❌ Critical issues found - please fix before going live")
    
    print("="*50)
    return len(issues) == 0

if __name__ == "__main__":
    success = check_production_readiness()
    sys.exit(0 if success else 1)
