# IPN Registration Setup Guide

## 🎯 **Problem Solved**
✅ **Before:** IPN URL was registered on every payment (inefficient)  
✅ **After:** IPN URL registered once during setup (recommended)

## 📋 **Setup Steps**

### **1. Install Dependencies**
```bash
pip install python-dotenv requests
```

### **2. Create .env File**
```bash
# Copy the example and fill in your credentials
cp .env.example .env
```

Edit `.env` with your PesaPal credentials:
```bash
PESAPAL_CONSUMER_KEY=your_actual_consumer_key
PESAPAL_CONSUMER_SECRET=your_actual_consumer_secret
# Leave PESAPAL_IPN_ID empty for now
```

### **3. Run IPN Setup Script**
```bash
python setup_ipn.py
```

This script will:
- ✅ Connect to PesaPal API
- ✅ Register your IPN URL: `https://denncathy.co.ke/payment/ipn`
- ✅ Return an IPN ID (save this!)

### **4. Update .env with IPN ID**
Add the returned IPN ID to your `.env` file:
```bash
PESAPAL_IPN_ID=your_returned_ipn_id
```

### **5. Test the Setup**
```bash
# Test that config loads correctly
python -c "from config_pesapal import PESAPAL_CONFIG; print('IPN ID:', PESAPAL_CONFIG['ipn_id'])"
```

## 🔄 **What Changed in Payment Flow**

### **Before (❌ Inefficient):**
```python
# This was called on EVERY payment
"notification_id": pesapal_api.register_ipn_url().get('ipn_id')
```

### **After (✅ Efficient):**
```python
# This uses the pre-registered IPN ID
"notification_id": PESAPAL_CONFIG['ipn_id']
```

## 🛠️ **Files Modified:**

1. **`config_pesapal.py`** - Added IPN ID from environment
2. **`routes/payment.py`** - Uses stored IPN ID instead of registering each time
3. **`setup_ipn.py`** - New script for one-time IPN registration
4. **`.env.example`** - Added PesaPal environment variables
5. **`requirements.txt`** - Added python-dotenv dependency

## 🏃‍♂️ **Quick Start**

```bash
# 1. Install new dependency
pip install python-dotenv

# 2. Set up your credentials
cp .env.example .env
# Edit .env with your PesaPal credentials

# 3. Register IPN URL
python setup_ipn.py

# 4. Add returned IPN ID to .env file
echo "PESAPAL_IPN_ID=your_ipn_id_here" >> .env

# 5. Test your setup
python -c "from config_pesapal import PESAPAL_CONFIG; print('Setup OK!' if PESAPAL_CONFIG['ipn_id'] else 'IPN ID missing')"
```

## 📝 **Benefits of This Approach:**

1. **🚀 Faster Payments** - No API call to register IPN on each transaction
2. **💰 Cost Efficient** - Fewer API calls = better rate limits
3. **🔒 More Reliable** - Pre-registered IPN won't fail during payment
4. **📊 Better Tracking** - Single IPN ID for all transactions
5. **🎯 PesaPal Recommended** - Follows official best practices

## 🔍 **Troubleshooting:**

### **"IPN ID is None"**
- Run `python setup_ipn.py` to register IPN URL
- Check your PesaPal credentials in `.env`
- Ensure your domain is accessible from internet

### **"Authentication failed"**
- Verify PESAPAL_CONSUMER_KEY and PESAPAL_CONSUMER_SECRET
- Check if you're using sandbox vs production credentials
- Ensure .env file is in the correct location

### **"IPN registration failed"**
- Verify your domain/URL is accessible
- Check firewall settings
- Ensure HTTPS is working on your domain

## 🎉 **You're All Set!**

Your PesaPal integration now follows best practices with efficient IPN handling! 🚀
