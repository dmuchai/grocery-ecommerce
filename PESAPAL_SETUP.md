# PesaPal Integration Setup Guide for Denncathy Fresh Basket

## Overview
This guide will help you complete the PesaPal payment integration for your grocery ecommerce website.

## 🔧 **Setup Steps**

### 1. **PesaPal Account Setup**
- Visit [PesaPal Developer Portal](https://developer.pesapal.com/)
- Create a developer account
- Get your API credentials:
  - Consumer Key
  - Consumer Secret
- Note the environment URLs:
  - **Sandbox:** `https://cybqa.pesapal.com/pesapalv3`
  - **Production:** `https://pay.pesapal.com/pesapalv3`

### 2. **Update Configuration**
Edit `config_pesapal.py` with your actual credentials:

```python
PESAPAL_CONFIG = {
    'consumer_key': 'YOUR_ACTUAL_CONSUMER_KEY',
    'consumer_secret': 'YOUR_ACTUAL_CONSUMER_SECRET',
    
    # Update URLs to match your domain
    'callback_url': 'https://denncathy.co.ke/payment/callback',
    'notification_url': 'https://denncathy.co.ke/payment/ipn',
    'cancellation_url': 'https://denncathy.co.ke/payment/cancelled'
}
```

### 3. **Database Setup**
Run the payment schema updates:

```bash
# Navigate to your project directory
cd /home/dennis-muchai/Desktop/grocery-ecommerce

# Apply the new schema
sqlite3 instance/grocery.db < schema_payments.sql
```

### 4. **Install Dependencies**
```bash
pip install requests
# Or update all dependencies
pip install -r requirements.txt
```

### 5. **Test the Integration**

#### **Sandbox Testing:**
1. Use test credentials from PesaPal
2. Test with these scenarios:
   - Successful payment
   - Failed payment
   - Cancelled payment
   - Network timeout

#### **Test Flow:**
1. Add items to cart
2. Click "Pay with PesaPal"
3. Complete payment on PesaPal page
4. Verify callback handling
5. Check order status updates

### 6. **Production Deployment**

#### **Before Going Live:**
- [ ] Replace sandbox credentials with production credentials
- [ ] Update base URL to production: `https://pay.pesapal.com/pesapalv3`
- [ ] Test all payment flows in production environment
- [ ] Set up monitoring for payment failures
- [ ] Configure proper SSL certificates

#### **Post-Deployment Checklist:**
- [ ] Test M-Pesa payments
- [ ] Test card payments
- [ ] Verify IPN notifications
- [ ] Check order status updates
- [ ] Test email notifications

## 🚀 **Files Created/Modified**

### **New Files:**
- `config_pesapal.py` - PesaPal configuration
- `routes/payment.py` - Payment handling routes
- `schema_payments.sql` - Database schema updates
- `templates/payment/success.html` - Success page
- `templates/payment/failed.html` - Failed payment page
- `templates/payment/processing.html` - Processing page

### **Modified Files:**
- `app.py` - Added payment blueprint
- `templates/cart.html` - Added PesaPal payment button
- `requirements.txt` - Added requests dependency

## 💡 **Key Features Implemented**

### **Payment Flow:**
1. **Cart → Payment:** Seamless transition from cart to PesaPal
2. **Order Tracking:** Unique order IDs and tracking
3. **Status Updates:** Real-time payment status updates
4. **Multi-Payment Support:** M-Pesa, Cards, Bank transfers

### **Security Features:**
- JWT token authentication with PesaPal
- Secure callback handling
- IPN notification verification
- Order validation and tracking

### **User Experience:**
- Clear payment status pages
- Auto-refresh for processing payments
- Mobile-responsive payment flow
- Cart integration with payment

## 🔍 **Troubleshooting**

### **Common Issues:**

#### **"Payment initialization failed"**
- Check API credentials
- Verify network connectivity
- Ensure PesaPal service is active

#### **"Order not found"**
- Check database connection
- Verify order creation in initiate_payment
- Check session management

#### **IPN not working**
- Verify notification URL is accessible
- Check firewall settings
- Ensure proper HTTP response codes

### **Debug Commands:**
```bash
# Check database
sqlite3 instance/grocery.db ".tables"
sqlite3 instance/grocery.db "SELECT * FROM orders LIMIT 5;"

# Check logs
tail -f app.log

# Test API connectivity
python -c "import requests; print(requests.get('https://cybqa.pesapal.com/pesapalv3/health').status_code)"
```

## 📞 **Support**

### **PesaPal Documentation:**
- [API Reference](https://developer.pesapal.com/how-to-integrate/api-30-overview)
- [Integration Guide](https://developer.pesapal.com/how-to-integrate/integration-overview)

### **Contact PesaPal:**
- Email: developers@pesapal.com
- Phone: +254 20 3286265

## 🎯 **Next Steps**

1. **Get PesaPal credentials** from developer portal
2. **Update configuration** with real credentials
3. **Run database updates** using schema_payments.sql
4. **Test in sandbox** environment
5. **Deploy to production** with production credentials
6. **Monitor and optimize** payment success rates

---

**Ready to accept payments!** 🚀 Your Denncathy Fresh Basket is now equipped with secure PesaPal payment processing.
