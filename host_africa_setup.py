#!/usr/bin/env python3
"""
Host Africa Deployment Setup Script
Handles the deployment process step by step
"""

import os
import subprocess
import sys

def check_python_version():
    """Check Python version"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    print(f"  Python {version.major}.{version.minor}.{version.micro}")
    if version.major >= 3 and version.minor >= 6:
        print("  ✅ Python version is compatible")
        return True
    else:
        print("  ❌ Python 3.6+ required")
        return False

def check_virtual_environment():
    """Check if virtual environment is activated"""
    print("\n🔧 Checking virtual environment...")
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("  ✅ Virtual environment is activated")
        return True
    else:
        print("  ⚠️  Virtual environment not detected")
        print("  Please activate your virtual environment first:")
        print("  source /home/denncath/virtualenv/domains/denncathy.co.ke/public_html/3.9/bin/activate")
        return False

def install_missing_packages():
    """Install any missing packages"""
    print("\n📦 Checking required packages...")
    
    required_packages = [
        'flask',
        'pymysql',
        'python-dotenv',
        'requests'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"  ✅ {package} is installed")
        except ImportError:
            missing.append(package)
            print(f"  ❌ {package} is missing")
    
    if missing:
        print(f"\n📥 Installing missing packages: {', '.join(missing)}")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install'] + missing)
            print("  ✅ All packages installed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"  ❌ Failed to install packages: {e}")
            return False
    else:
        print("  ✅ All required packages are installed")
        return True

def check_database_migration():
    """Check if database migration is needed"""
    print("\n🗄️  Database Migration Check...")
    print("Please run the database migration manually:")
    print("  python migrate_database_pymysql.py")
    print("")
    response = input("Have you run the database migration? (yes/no): ").lower()
    return response in ['yes', 'y']

def check_environment_file():
    """Check if .env file exists and has production settings"""
    print("\n⚙️  Checking environment configuration...")
    
    if os.path.exists('.env'):
        print("  ✅ .env file exists")
        
        # Read and check critical settings
        with open('.env', 'r') as f:
            content = f.read()
        
        critical_settings = [
            'PESAPAL_CONSUMER_KEY',
            'PESAPAL_CONSUMER_SECRET',
            'DATABASE_HOST',
            'DATABASE_USER',
            'DATABASE_PASSWORD',
            'DATABASE_NAME'
        ]
        
        missing_settings = []
        for setting in critical_settings:
            if setting not in content or f'{setting}=' not in content:
                missing_settings.append(setting)
        
        if missing_settings:
            print(f"  ⚠️  Missing settings in .env: {', '.join(missing_settings)}")
            print("  Please update your .env file with production values")
            return False
        else:
            print("  ✅ All critical settings found in .env")
            
            # Check if it's set to production
            if 'FLASK_ENV=production' in content:
                print("  ✅ Set to production mode")
                return True
            else:
                print("  ⚠️  Not set to production mode")
                print("  Please set FLASK_ENV=production in your .env file")
                return False
    else:
        print("  ❌ .env file not found")
        print("  Please create .env file with production settings")
        print("  Use .env.production as a template")
        return False

def test_basic_import():
    """Test if the app can be imported"""
    print("\n🧪 Testing app import...")
    try:
        from app import app
        print("  ✅ App imports successfully")
        return True
    except Exception as e:
        print(f"  ❌ App import failed: {e}")
        return False

def run_deployment_checks():
    """Run all deployment checks"""
    print("🚀 Host Africa Deployment Checker")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Virtual Environment", check_virtual_environment),
        ("Required Packages", install_missing_packages),
        ("Environment Config", check_environment_file),
        ("App Import Test", test_basic_import),
        ("Database Migration", check_database_migration),
    ]
    
    all_passed = True
    results = {}
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results[check_name] = result
            all_passed = all_passed and result
        except Exception as e:
            print(f"❌ {check_name} failed with error: {e}")
            results[check_name] = False
            all_passed = False
    
    # Print summary
    print("\n" + "=" * 50)
    print("📊 DEPLOYMENT READINESS SUMMARY")
    print("=" * 50)
    
    for check_name, result in results.items():
        status = "✅ READY" if result else "❌ NEEDS ATTENTION"
        print(f"{check_name:.<30} {status}")
    
    print("\n" + "=" * 50)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Your denncathy.co.ke deployment is ready!")
        print("\nNext steps:")
        print("1. Restart your web server if needed")
        print("2. Test the website functionality")
        print("3. Run: python test_production_deployment.py")
    else:
        print("⚠️  SOME CHECKS FAILED!")
        print("❌ Please fix the issues above before deployment")
        print("\nCommon fixes:")
        print("• Activate virtual environment")
        print("• Update .env file with production values")
        print("• Run database migration")
        print("• Install missing packages")
    print("=" * 50)
    
    return all_passed

if __name__ == "__main__":
    success = run_deployment_checks()
    sys.exit(0 if success else 1)
