# 🚨 PesaPal Credential Issues Found

## **Current Issues:**

### ❌ **Issue 1: Invalid Credentials**
```
Error: "invalid_consumer_key_or_secret_provided"
```
Your current credentials are not working with PesaPal sandbox.

### ❌ **Issue 2: Wrong API URLs**
Production URL returned 404, indicating incorrect endpoint.

## **🔧 How to Fix:**

### **Step 1: Get Valid PesaPal Credentials**

1. **Visit PesaPal Developer Portal:**
   - Go to: https://developer.pesapal.com/
   - Sign up or log in to your account

2. **Create a New Application:**
   - Click "Create App" or "New Application"
   - Fill in your app details:
     - Name: "Denncathy Fresh Basket"
     - Description: "Grocery ecommerce payment system"
     - Website: "https://denncathy.co.ke"

3. **Get API Credentials:**
   - After creating the app, you'll get:
     - Consumer Key
     - Consumer Secret
   - Make sure to copy these exactly!

4. **Activate Your Account:**
   - Some accounts need manual activation
   - Check your email for activation links
   - Contact PesaPal support if needed

### **Step 2: Update Your .env File**

Replace your current credentials with the new ones:

```bash
# Old credentials (not working)
# PESAPAL_CONSUMER_KEY=EUhWl3sqfn0SvLhSxyejGh1Vt/3LAg3s
# PESAPAL_CONSUMER_SECRET=aa3mvsfopr5kHr/gUIhjw7d8H5c=

# New credentials (get these from developer portal)
PESAPAL_CONSUMER_KEY=your_new_consumer_key_here
PESAPAL_CONSUMER_SECRET=your_new_consumer_secret_here
```

### **Step 3: Test New Credentials**

```bash
# Test your new credentials
python check_credentials.py
```

### **Step 4: Register IPN URL**

Once credentials work:
```bash
# Register your IPN URL
python setup_ipn.py
```

## **🆘 Alternative: Test with Demo Credentials**

If you want to test immediately, PesaPal sometimes provides demo credentials in their documentation. Check:
- https://developer.pesapal.com/how-to-integrate/api-30-overview

## **📞 Need Help?**

### **PesaPal Support:**
- Email: developers@pesapal.com
- Phone: +254 20 3286265
- Developer Portal: https://developer.pesapal.com/

### **Common Questions:**
1. **"How do I activate my account?"** - Check email or contact support
2. **"Are these sandbox or production keys?"** - Check in your developer portal
3. **"How long does activation take?"** - Usually instant, sometimes up to 24 hours

## **🎯 Quick Action Items:**

1. ✅ Visit https://developer.pesapal.com/
2. ✅ Create/login to your account  
3. ✅ Create a new application
4. ✅ Copy the Consumer Key & Secret
5. ✅ Update your .env file
6. ✅ Run: `python check_credentials.py`
7. ✅ Run: `python setup_ipn.py`

Your current credentials appear to be either:
- From an old/deactivated account
- Sample/demo credentials
- Incorrectly copied

Getting fresh credentials from the developer portal should resolve this! 🚀
