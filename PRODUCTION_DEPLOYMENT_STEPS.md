# Production Deployment Steps for Host Africa

## Issue Identified
The production site is failing at checkout with JavaScript errors, specifically:
- `Uncaught TypeError: Cannot read properties of null (reading 'addEventListener')`
- Missing static assets (logo image 404 error)

## Files That Need to be Updated in Production

### 1. **Critical Fix: templates/checkout.html**
The checkout.html template has been updated with null-safety checks for form elements.

**Action Required:**
```bash
# Upload the updated templates/checkout.html to production
```

### 2. **Verify Static Files**
The error shows: `GET https://denncathy.co.ke/static/images/denncathy-logo.png 404 (Not Found)`

**Action Required:**
- Verify the `static/` folder structure exists in production
- Ensure all files from `static/images/`, `static/css/`, `static/js/` are uploaded
- Check file permissions (should be readable: 644 for files, 755 for directories)

```bash
# On Host Africa server
cd /path/to/your/app
ls -la static/images/
# Should show denncathy-logo.png
```

### 3. **Database Migration (SQLAlchemy 2.0 Fixes)**
Recent commits fixed all deprecated `.query.get()` calls.

**Action Required:**
```bash
# Upload these updated route files:
- routes/admin.py
- routes/product.py
- routes/cart.py
- routes/payment.py
- models/product.py
```

### 4. **New Template File**
Created `templates/return_policy.html` to fix BuildError.

**Action Required:**
```bash
# Upload to production:
- templates/return_policy.html
```

### 5. **Environment Variables**
Ensure production `.env` file has all required variables:

```bash
# Required variables
SECRET_KEY=<your-production-secret-key>
DATABASE_HOST=localhost
DATABASE_USER=<your-mysql-username>
DATABASE_PASSWORD=<your-mysql-password>
DATABASE_NAME=<your-db-name>

# PesaPal Production Credentials
PESAPAL_CONSUMER_KEY=<production-key>
PESAPAL_CONSUMER_SECRET=<production-secret>
PESAPAL_IPN_ID=<production-ipn-id>
PESAPAL_BASE_URL=https://pay.pesapal.com/v3

# Flask Environment
FLASK_ENV=production
```

### 6. **Restart Application**
After uploading files, restart the application.

**Action Required:**
```bash
# On Host Africa cPanel or via SSH:
touch tmp/restart.txt
# Or restart via cPanel Python App Manager
```

## Quick Upload Commands (via FTP/SSH)

### Using SCP (if you have SSH access):
```bash
# From your local machine:
cd /home/dennis-muchai/grocery-ecommerce

# Upload specific files
scp templates/checkout.html username@denncathy.co.ke:/path/to/app/templates/
scp templates/return_policy.html username@denncathy.co.ke:/path/to/app/templates/
scp routes/admin.py username@denncathy.co.ke:/path/to/app/routes/
scp routes/product.py username@denncathy.co.ke:/path/to/app/routes/
scp routes/cart.py username@denncathy.co.ke:/path/to/app/routes/
scp routes/payment.py username@denncathy.co.ke:/path/to/app/routes/
scp models/product.py username@denncathy.co.ke:/path/to/app/models/

# Upload entire static folder (if missing files)
scp -r static/ username@denncathy.co.ke:/path/to/app/
```

### Using FTP/FileZilla:
1. Connect to `ftp.denncathy.co.ke`
2. Navigate to your application directory
3. Upload the following directories (maintaining structure):
   - `templates/` (checkout.html, return_policy.html)
   - `routes/` (admin.py, product.py, cart.py, payment.py)
   - `models/` (product.py)
   - `static/` (entire folder if assets are missing)

## Verification Steps After Deployment

### 1. Check Application Logs
```bash
# On Host Africa
tail -f /path/to/logs/error.log
```

### 2. Test Critical Endpoints
```bash
# From your local terminal
curl -I https://denncathy.co.ke/
curl -I https://denncathy.co.ke/static/images/denncathy-logo.png
curl -I https://denncathy.co.ke/checkout
```

### 3. Browser Testing
- Visit: https://denncathy.co.ke
- Add items to cart
- Proceed to checkout
- Check browser console (F12) for any JavaScript errors
- Verify checkout form submits to PesaPal

### 4. Database Verification
```bash
# On production MySQL
mysql -u <user> -p <database>
# Run:
SELECT * FROM sessions LIMIT 5;
SELECT * FROM products LIMIT 5;
SELECT * FROM users WHERE role='admin';
```

## Common Host Africa Issues & Fixes

### Issue: "MySQL server has gone away"
**Fix:** Add to config.py:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_pre_ping': True,
    'pool_recycle': 280
}
```

### Issue: Static files 404
**Fix:** 
- Check `.htaccess` file exists with proper rewrite rules
- Verify static folder permissions: `chmod -R 755 static/`

### Issue: Import errors
**Fix:**
- Ensure all dependencies in requirements.txt are installed
- Run: `pip install -r requirements.txt --user` (on production)

### Issue: Session not persisting
**Fix:**
- Verify `sessions` table exists in database
- Check `SESSION_SQLALCHEMY` is properly configured in config.py

## Post-Deployment Checklist

- [ ] All modified files uploaded to production
- [ ] Static files accessible (check logo loads)
- [ ] Database migrations applied (if any)
- [ ] Environment variables properly set
- [ ] Application restarted
- [ ] Homepage loads without errors
- [ ] Checkout page loads without JavaScript errors
- [ ] Can add items to cart
- [ ] Checkout form submits successfully
- [ ] PesaPal payment page opens
- [ ] Error logs clear of BuildError and TypeError

## Rollback Plan (if issues persist)

1. Keep a backup of working production files
2. If deployment fails, restore from backup:
   ```bash
   cp backup/templates/checkout.html templates/
   # Restart application
   touch tmp/restart.txt
   ```

## Support

If issues persist after deployment:
1. Check production error logs: `tail -100 /path/to/logs/error.log`
2. Compare local vs production .env files
3. Verify all Python packages installed: `pip freeze > production_packages.txt`
4. Contact Host Africa support if server configuration issues
