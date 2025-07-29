# 📋 Quick Deployment Checklist for denncathy.co.ke

## 🚀 Pre-Deployment
- [ ] Backup current website files
- [ ] Backup current database
- [ ] Test all changes locally
- [ ] Update requirements.txt if needed

## 📁 Files to Upload/Update
- [ ] `app.py` (SQLAlchemy 2.0 updates)
- [ ] `routes/user.py` (Enhanced registration)
- [ ] `routes/checkout.py` (Enhanced checkout with delivery)
- [ ] `routes/payment.py` (PesaPal integration fixes)
- [ ] `templates/register.html` (NEW enhanced form)
- [ ] `templates/checkout.html` (Enhanced checkout UI)
- [ ] `models/user.py` (Enhanced User model)
- [ ] `wsgi.py` (Production entry point)
- [ ] `requirements.txt` (Dependencies)

## 🗄️ Database Migration
- [ ] Run `python migrate_database.py` on server
- [ ] Verify new user table columns added
- [ ] Test user registration with new fields

## ⚙️ Environment Configuration
- [ ] Update `.env` with production values:
  - [ ] `FLASK_ENV=production`
  - [ ] `FLASK_DEBUG=False`
  - [ ] `PESAPAL_BASE_URL=https://pay.pesapal.com/pesapalv3`
  - [ ] Production database credentials
  - [ ] Secure SECRET_KEY

## 🔐 PesaPal Configuration
- [ ] Verify PesaPal account is production-ready
- [ ] Register IPN endpoint: `python setup_ipn.py`
- [ ] Update `.env` with production IPN_ID
- [ ] Test payment flow with small amount

## 🧪 Post-Deployment Testing
- [ ] Run `python test_production_deployment.py`
- [ ] Test enhanced registration form
- [ ] Test checkout with delivery details
- [ ] Test PesaPal payment integration
- [ ] Verify SSL certificate is working
- [ ] Check all static resources load

## ✅ Success Indicators
- [ ] Homepage loads without errors
- [ ] Registration shows 3-section form
- [ ] Checkout captures delivery details
- [ ] Payments process through PesaPal
- [ ] User profiles save all fields
- [ ] No 500 errors in any section

## 🚨 Rollback Plan (If Issues)
- [ ] Restore backed up files
- [ ] Restore backed up database
- [ ] Verify old version works
- [ ] Document issues for later fix

---
**Last Updated:** July 29, 2025  
**Target:** denncathy.co.ke via Host Africa
