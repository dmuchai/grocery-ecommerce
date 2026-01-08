# Payment 500 Error - Root Cause and Complete Fix

## Root Cause Analysis

The 500 error was caused by **fundamental architectural flaws** in the payment callback design:

### 1. **Session Dependency (CRITICAL)**
**Problem:** The `/payment/callback` endpoint relied on Flask session data that **does NOT exist** when Pesapal calls it.

**Why it fails:**
- Pesapal does NOT guarantee a logged-in user
- Pesapal does NOT send browser session cookies
- Pesapal does NOT maintain Flask session state
- Flask creates a new empty session for Pesapal's callback

**Result:** `session['db_order_id']` is missing → Order lookup fails → 500 error

### 2. **Missing Merchant Reference in Database (CRITICAL)**
**Problem:** Two different order identifiers were generated but never linked:
1. Database order ID: `new_order.id` (primary key)
2. Pesapal merchant reference: `ORDER_XXXXXX_TIMESTAMP`

The merchant reference was **never stored in the database**, making it impossible to find the order when Pesapal calls back with `OrderMerchantReference`.

**Result:** Cannot find order in database → 500 error

### 3. **Template Rendering in Callback (CRITICAL)**
**Problem:** The callback was rendering HTML templates, which Pesapal doesn't expect.

**Why it fails:**
- Pesapal expects a fast, non-interactive HTTP 200 response
- Template rendering can fail (missing templates, Jinja errors, flash messages require session)
- This violates Pesapal's callback requirements

**Result:** Template errors → 500 error

## Complete Fix Implementation

### ✅ 1. Added Database Fields
**Added to Order model:**
- `merchant_reference` - Stores Pesapal order reference (unique, indexed)
- `pesapal_tracking_id` - Stores Pesapal tracking ID (indexed)

**Migration created:** `a1b2c3d4e5f6_add_merchant_reference_to_orders.py`

### ✅ 2. Store Merchant Reference During Order Creation
**Updated `initiate_payment`:**
```python
new_order = Order(
    ...
    merchant_reference=order_id,  # Now stored in DB
    pesapal_tracking_id=pesapal_response.get('order_tracking_id')
)
```

### ✅ 3. Rewrote Callback to be Stateless
**New `/payment/callback` design:**
- ✅ No session dependency - finds order by `merchant_reference`
- ✅ No template rendering - returns plain text "OK" with 200 status
- ✅ Idempotent - safe to call multiple times
- ✅ Handles both server-to-server (Pesapal IPN) and browser redirects
- ✅ Comprehensive error handling and logging

**Key changes:**
- Finds order: `Order.query.filter_by(merchant_reference=merchant_ref).first()`
- Updates order status only if not already completed
- Returns "OK", 200 for server requests
- Redirects browsers to `/payment/complete` for user-facing page

### ✅ 4. Created Separate User-Facing Route
**New `/payment/complete` route:**
- Uses session/browser state safely (called by user's browser)
- Renders success/failed/processing templates
- Clears cart after successful payment
- Shows order details to user

### ✅ 5. Fixed Template URL Errors
**Changed:** `url_for('main.index')` → `url_for('home')` in all payment templates

### ✅ 6. Registered Error Handlers
- Error handlers now registered in `app.py`
- Error templates created (`404.html`, `500.html`, `403.html`)
- Logging configured

## Architecture Overview

### Payment Flow (Fixed)

1. **User initiates payment** (`/payment/initiate`)
   - Creates order in database with `merchant_reference`
   - Submits to Pesapal
   - Redirects user to Pesapal payment page

2. **Pesapal processes payment**
   - User completes payment on Pesapal
   - Pesapal calls `/payment/callback` (server-to-server)
   - Callback finds order by `merchant_reference`
   - Updates order status in database
   - Returns "OK", 200 to Pesapal

3. **User redirected back**
   - Pesapal redirects user's browser to `/payment/callback`
   - Callback detects browser request
   - Redirects to `/payment/complete`
   - User sees success/failed page

### Key Principles

✅ **Stateless callbacks** - No session, no templates, just 200 OK  
✅ **Database lookup** - Find orders by `merchant_reference`  
✅ **Idempotent** - Safe to call multiple times  
✅ **Separation of concerns** - Callback for processing, complete for display  

## How to Debug Future Payment Issues

### 1. **Check Application Logs**
```bash
# View logs in real-time
tail -f logs/grocery_ecommerce.log

# Search for payment-related errors
grep -i "payment\|pesapal" logs/grocery_ecommerce.log
```

### 2. **Check Common Issues**

#### Session Expiration
- If `db_order_id` is missing from session, the fallback logic will try to find the order
- Check logs for "Found order via..." messages

#### PesaPal API Errors
- Check logs for "Error querying PesaPal status"
- Verify PesaPal credentials are correct
- Check network connectivity to PesaPal API

#### Database Errors
- Check logs for "Error updating order status"
- Verify database connection is active
- Check for database constraint violations

### 3. **Test Payment Flow**

1. **Initiate Payment:**
   - Add items to cart
   - Go to checkout
   - Click "Pay with PesaPal"
   - Check logs for order creation

2. **Complete Payment:**
   - Complete payment on PesaPal
   - Check callback URL is called
   - Verify order status is updated in database

3. **Verify Success:**
   - Check that success page renders
   - Verify cart is cleared
   - Confirm order appears in order history

### 4. **Monitor Key Points**

- **Order Creation:** Check `initiate_payment` route logs
- **PesaPal Response:** Check for `redirect_url` in response
- **Callback Received:** Check `payment_callback` route logs
- **Order Update:** Verify order status changes in database
- **Template Rendering:** Check for template errors

## Testing Checklist

- [ ] Payment initiation works
- [ ] PesaPal redirect works
- [ ] Payment completion redirects to callback
- [ ] Success page renders without errors
- [ ] Order status is updated in database
- [ ] Cart is cleared after successful payment
- [ ] Error handling works for failed payments
- [ ] Error handling works for cancelled payments
- [ ] Logs are being written correctly

## Testing the Fix

### 1. Run Database Migration
```bash
# Apply the new migration
flask db upgrade
```

### 2. Test Payment Flow
1. Add items to cart
2. Go to checkout
3. Initiate payment
4. Complete payment on Pesapal
5. Verify:
   - ✅ No 500 errors
   - ✅ Order status updated in database
   - ✅ Success page displays correctly
   - ✅ Cart is cleared

### 3. Verify Database
```sql
-- Check that merchant_reference is stored
SELECT id, merchant_reference, pesapal_tracking_id, status 
FROM orders 
ORDER BY created_at DESC 
LIMIT 5;
```

## Additional Improvements Made

1. **Stateless Architecture:** Callback no longer depends on session
2. **Database Integrity:** Merchant reference stored and indexed
3. **Comprehensive Logging:** All payment operations logged
4. **Error Handling:** Proper error handling with rollback
5. **Pesapal Compliance:** Follows Pesapal callback requirements

## Next Steps

1. ✅ Run database migration: `flask db upgrade`
2. ✅ Test payment flow end-to-end
3. ✅ Monitor logs during real transactions
4. Consider adding email notifications for payment status changes
5. Consider adding webhook retry handling for failed callbacks
