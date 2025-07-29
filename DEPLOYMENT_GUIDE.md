# 🚀 Deployment Guide for denncathy.co.ke
## Host Africa Deployment - All PesaPal Integration Changes

### 📋 Changes to Deploy (Since "Eggs and Dairy" Enhancement)

#### 1. **Enhanced Registration Form** (Latest - ca0bff9)
✅ **Features:**
- Three-section registration (Required, Profile, Address)
- Optional profile completion during registration
- Real-time password validation
- Collapsible sections with animations
- Mobile-responsive design

✅ **Files Changed:**
- `templates/register.html` - Complete UI overhaul
- `routes/user.py` - Enhanced registration handling
- New: `test_enhanced_registration.py` - Test suite

#### 2. **SQLAlchemy 2.0 Compatibility & Cart URL Fixes** (2d32a5d)
✅ **Critical Fixes:**
- Updated all deprecated `query.get()` to `db.session.get()`
- Fixed cart image URL corruption issues
- Resolved recursive URL problems in cart system

✅ **Files Changed:**
- `app.py` - SQLAlchemy 2.0 updates
- `routes/payment.py` - Database query fixes
- `routes/checkout.py` - Cart URL cleanup

#### 3. **Profile Navigation & Cart Data Fixes** (d353816)
✅ **Bug Fixes:**
- Fixed profile page navigation errors
- Resolved cart-data endpoint image URL issues
- Improved error handling

#### 4. **Enhanced Checkout Process with PesaPal** (e353015)
✅ **Major Features:**
- Multi-step checkout with delivery details capture
- Enhanced PesaPal API v3 integration
- Production-ready payment processing
- Order summary and confirmation system

✅ **Files Changed:**
- `routes/checkout.py` - Complete checkout flow
- `routes/payment.py` - PesaPal integration
- `templates/checkout.html` - New checkout UI
- `models/user.py` - Enhanced User model

---

### 🔧 Pre-Deployment Checklist

#### Step 1: Environment Configuration
```bash
# Create production .env file on server
PESAPAL_CONSUMER_KEY=your_production_key
PESAPAL_CONSUMER_SECRET=your_production_secret
PESAPAL_IPN_ID=your_registered_ipn_id
PESAPAL_BASE_URL=https://pay.pesapal.com/v3
SECRET_KEY=your-very-secure-production-secret
DATABASE_HOST=localhost
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_secure_db_password
DATABASE_NAME=grocery_db
FLASK_ENV=production
FLASK_DEBUG=False
```

#### Step 2: Database Updates Required
```sql
-- Enhanced User model requires these columns
ALTER TABLE user ADD COLUMN first_name VARCHAR(100);
ALTER TABLE user ADD COLUMN last_name VARCHAR(100);
ALTER TABLE user ADD COLUMN phone VARCHAR(20);
ALTER TABLE user ADD COLUMN address TEXT;
ALTER TABLE user ADD COLUMN city VARCHAR(100);
ALTER TABLE user ADD COLUMN state VARCHAR(100);
ALTER TABLE user ADD COLUMN postal_code VARCHAR(20);
ALTER TABLE user ADD COLUMN country VARCHAR(100);
ALTER TABLE user ADD COLUMN profile_completed BOOLEAN DEFAULT FALSE;
ALTER TABLE user ADD COLUMN updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP;
```

#### Step 3: Required Files to Upload
```
✅ Core Application Files:
- app.py
- config.py
- wsgi.py
- requirements.txt

✅ Routes (Updated):
- routes/user.py
- routes/checkout.py
- routes/payment.py
- routes/main.py

✅ Templates (Enhanced):
- templates/register.html (NEW DESIGN)
- templates/checkout.html (NEW CHECKOUT)
- templates/base.html
- All other template files

✅ Models:
- models/user.py (ENHANCED)
- models/product.py
- models/order.py

✅ Static Files:
- static/css/
- static/js/
- static/images/

✅ Configuration:
- .env (production values)
- schema.sql (if needed for fresh install)
```

---

### 🌐 Host Africa Deployment Steps

#### Method 1: File Manager Upload (Recommended for Host Africa)
1. **Backup Current Site:**
   ```bash
   # On your Host Africa cPanel
   # 1. Go to File Manager
   # 2. Create backup of current public_html
   # 3. Download backup to local
   ```

2. **Upload New Files:**
   ```bash
   # 1. Select all updated files from your local project
   # 2. Upload to public_html directory
   # 3. Ensure correct file permissions (644 for files, 755 for directories)
   ```

3. **Database Migration:**
   ```bash
   # In Host Africa cPanel -> phpMyAdmin
   # 1. Select your database
   # 2. Run the ALTER TABLE statements above
   # 3. Verify all columns are added correctly
   ```

#### Method 2: Git Deployment (If Available)
```bash
# If you have SSH access to Host Africa
cd /path/to/your/website
git pull origin master
pip install -r requirements.txt --user
```

---

### ⚙️ Post-Deployment Configuration

#### 1. PesaPal IPN Setup (CRITICAL)
```bash
# On your server, run:
python setup_ipn.py
# This will register your IPN endpoint with PesaPal
# Update .env with the returned IPN_ID
```

#### 2. Test Critical Features
```bash
# Test these features after deployment:
✅ User registration (new enhanced form)
✅ User login and profile management
✅ Product browsing and cart functionality
✅ Checkout process (delivery details)
✅ PesaPal payment integration
✅ Order confirmation and history
```

#### 3. Production Settings Verification
```python
# Verify in your production .env:
FLASK_ENV=production
FLASK_DEBUG=False
PESAPAL_BASE_URL=https://pay.pesapal.com/pesapalv3  # PRODUCTION URL
```

---

### 🚨 Critical Production Notes

#### PesaPal Production Requirements:
1. **Business Verification:** Ensure your PesaPal account is verified for production
2. **Domain Whitelisting:** Add denncathy.co.ke to PesaPal allowed domains
3. **SSL Certificate:** Ensure HTTPS is enabled (required by PesaPal)
4. **IPN Endpoint:** Must be accessible at https://denncathy.co.ke/payment/ipn

#### Security Checklist:
✅ All secret keys are production-safe
✅ Debug mode is disabled
✅ Database credentials are secure
✅ File permissions are correct (not 777)
✅ .env file is not accessible via web

---

### 🧪 Post-Deployment Testing Script

```python
# Save this as test_production.py and run after deployment
import requests

base_url = "https://denncathy.co.ke"

def test_deployment():
    print("🧪 Testing Production Deployment...")
    
    # Test homepage
    response = requests.get(base_url)
    print(f"Homepage: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
    
    # Test registration page
    response = requests.get(f"{base_url}/user/register")
    print(f"Registration: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
    
    # Test products page
    response = requests.get(f"{base_url}/products")
    print(f"Products: {response.status_code} {'✅' if response.status_code == 200 else '❌'}")
    
    print("✅ Basic deployment test complete!")

if __name__ == "__main__":
    test_deployment()
```

---

### 📞 Support Contacts
- **Host Africa Support:** Check your hosting panel for support tickets
- **PesaPal Support:** developer@pesapal.com
- **Domain Issues:** Your domain registrar

### 🎯 Success Indicators
✅ Website loads without errors
✅ Registration form shows new 3-section design
✅ Checkout process captures delivery details
✅ PesaPal payments process successfully
✅ User profiles save all new fields
✅ Cart functionality works correctly

---

*Last Updated: July 29, 2025*
*Deployment Target: denncathy.co.ke via Host Africa*
