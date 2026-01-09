# Email & Order Status Setup Instructions

## Overview
You now have:
- ✅ Order status tracking page (public access via order reference)
- ✅ Email notifications (order confirmation, payment received, shipment, cancellation)
- ✅ Cancel order & retry payment functionality
- ✅ Admin alerts on new orders

## Setup Required

### Email Provider Comparison

| Feature | Gmail | Brevo | SendGrid | Mailgun |
|---------|-------|-------|----------|---------|
| **Free Tier** | 500/day | 300/day | 100/day | 100/day |
| **Paid Plan Cost** | Free | $20/mo | $19.95/mo | $0.50 per 1K emails |
| **Setup Complexity** | Easy | Very Easy | Easy | Moderate |
| **Best For** | Testing | **Kenya/Africa** | Enterprise | High volume |
| **Rate Limits** | Aggressive | None | High | High |
| **SPF/DKIM** | Auto | Auto | Manual | Manual |
| **Support** | None | 24/7 Chat | 24/7 | Community |

**Recommendation**: Use **Brevo** for production (optimized for Africa, no rate limits, affordable).

### 1. Email Configuration in .env

Add these to your `.env` file:

```bash
# Gmail SMTP Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-specific-password
MAIL_DEFAULT_SENDER=noreply@denncathy.co.ke
ADMIN_EMAIL=admin@denncathy.co.ke
```

### 2. How to Generate Gmail App Password

1. Go to https://myaccount.google.com/apppasswords
2. Select "Mail" and "Windows Computer" (or your device)
3. Google will generate a 16-character password
4. Use this password in `MAIL_PASSWORD` above
5. **Important**: Remove spaces from the password if any

### 3. Alternative Email Services (Optional)

**Brevo** (recommended for Africa/Kenya - best value):
```bash
MAIL_SERVER=smtp-relay.brevo.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=sales@denncathy.co.ke
MAIL_PASSWORD=your-brevo-smtp-key
MAIL_DEFAULT_SENDER=noreply@denncathy.co.ke
ADMIN_EMAIL=sales@denncathy.co.ke
```

Get Brevo SMTP key:
1. Sign up free at https://www.brevo.com with your business email (`sales@denncathy.co.ke`)
2. Go to Settings → SMTP & API
3. Click "Generate SMTP key"
4. Use the generated key as `MAIL_PASSWORD` above
5. Note: `MAIL_USERNAME` = your Brevo registration email, `MAIL_PASSWORD` = the generated SMTP key (not your email password)

**SendGrid** (recommended for enterprise):
```bash
MAIL_SERVER=smtp.sendgrid.net
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=apikey
MAIL_PASSWORD=SG.your-sendgrid-api-key
MAIL_DEFAULT_SENDER=noreply@denncathy.co.ke
ADMIN_EMAIL=your-admin-email@gmail.com
```

Get SendGrid API key at: https://app.sendgrid.com/settings/api_keys

**Mailgun** (also good):
```bash
MAIL_SERVER=smtp.mailgun.org
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=postmaster@your-domain.mailgun.org
MAIL_PASSWORD=your-mailgun-password
MAIL_DEFAULT_SENDER=noreply@denncathy.co.ke
ADMIN_EMAIL=your-admin-email@gmail.com
```

## Installation

### Local Development
```bash
pip install Flask-Mail
pip install -r requirements.txt
```

### Production (Host Africa)
```bash
cd ~/domains/denncathy.co.ke/public_html
pip install Flask-Mail
python3 -m pip install --upgrade -r requirements.txt
touch tmp/restart.txt
```

## Features Overview

### 1. Order Status Page
**URL**: `/orders/track/<order-reference>`
- **Public access** (no login required)
- Shows order details, items, delivery address
- Displays status timeline with estimated delivery
- Allows customer to cancel or retry payment

**Example**: `https://denncathy.co.ke/orders/track/ORDER_A1B2C3D4_1704825600`

### 2. Email Notifications Sent

#### To Customer:
- ✅ **Order Confirmation** - When order is placed (sent after successful payment submission)
- ✅ **Payment Received** - When payment is confirmed
- ✅ **Order Shipped** - When admin marks order as shipped (manual trigger needed)
- ✅ **Payment Failed** - If payment doesn't go through
- ✅ **Order Cancelled** - If customer cancels order

#### To Admin:
- ✅ **New Order Alert** - Immediately when order is placed (includes customer details and items)

### 3. API Endpoints

**View Order Status** (GET)
```
GET /orders/track/<order-reference>
```
Returns HTML page with order details

**Cancel Order** (POST)
```
POST /orders/<order-id>/cancel
Requires: Order owner or admin
Response: JSON with success message
```

**Retry Payment** (POST)
```
POST /orders/<order-id>/retry-payment
Requires: Order owner or admin
Response: JSON with redirect_url to payment page
```

## Testing Email Setup

### 1. Test Send Email Script
```bash
python3 -c "
from app import app, mail
from flask_mail import Message

with app.app_context():
    msg = Message(
        subject='Test Email',
        recipients=['your-test-email@gmail.com'],
        body='This is a test email from Denncathy Fresh Basket!'
    )
    mail.send(msg)
    print('✓ Test email sent successfully!')
"
```

### 2. Verify in Production
1. Complete a checkout and payment on production
2. Check `/order/track/<order-reference>` loads correctly
3. Check your admin email received the new order alert
4. Check customer email received order confirmation + payment received

### 3. Test Cancel Order
1. Place an order (while in payment_initiated status)
2. Visit `/order/track/<order-reference>`
3. Click "Cancel Order" button
4. Verify cancellation email was sent to customer

## Email Template Customization

All email templates are in `templates/emails/`:
- `order_confirmation.html` - First email sent to customer
- `payment_received.html` - Confirmation of payment
- `order_shipped.html` - Shipping notification
- `payment_failed.html` - Payment retry prompt
- `order_cancelled.html` - Cancellation confirmation
- `admin_new_order.html` - Alert to admin

To customize, edit these HTML files and restart:
```bash
touch ~/domains/denncathy.co.ke/public_html/tmp/restart.txt
```

## Database Note

No database migration needed. The Order model already has:
- `merchant_reference` - Used for public order tracking
- `pesapal_tracking_id` - For payment tracking
- `status` - For order lifecycle
- `email` - For sending notifications
- `items` relationship - To list order contents

## Troubleshooting

### Emails Not Sending?

1. **Check logs**:
   ```bash
   tail -50 logs/grocery_ecommerce.log | grep -i email
   ```

2. **Verify Gmail settings**:
   - Is 2FA enabled on Gmail account?
   - Did you generate an app-specific password?
   - Is the password correct in .env?

3. **Test SMTP connection**:
   ```bash
   python3 -c "
   import smtplib
   try:
       server = smtplib.SMTP('smtp.gmail.com', 587)
       server.starttls()
       server.login('your-email@gmail.com', 'your-app-password')
       print('✓ SMTP connection successful!')
       server.quit()
   except Exception as e:
       print(f'✗ Error: {e}')
   "
   ```

4. **Check firewall**:
   - Host Africa may block certain SMTP ports
   - Try different email service if Gmail fails
   - Contact Host Africa support if needed

### Order Status Page Shows 404?

1. Verify order reference is correct
2. Check if order exists in database:
   ```bash
   mysql -u root -p grocery_db -e "SELECT * FROM orders WHERE merchant_reference='ORDER_XXXXX';"
   ```

### Emails sent but not received?

1. Check spam/junk folder
2. Verify customer email is correct in order
3. Check email provider's spam filters
4. Review email logs: `tail logs/grocery_ecommerce.log`

## Production Checklist

- [ ] Flask-Mail installed in production
- [ ] .env updated with email credentials
- [ ] App restarted: `touch tmp/restart.txt`
- [ ] Test order placed and confirmation email received
- [ ] Test admin alert email received
- [ ] Order status page loads: `/orders/track/ORDER_XXXXX`
- [ ] Cancel order button works
- [ ] Cancellation email sent to customer

## Next Steps

1. **Refund Management** - Add refund request form and admin approval
2. **Inventory Tracking** - Reduce stock on order completion
3. **Order History** - Customer dashboard showing their orders
4. **SMS Notifications** - Add Twilio for SMS alerts
5. **Analytics Dashboard** - Admin dashboard with sales metrics
6. **Live Chat** - Add customer support chat

See `MARKET_READY_FEATURES.md` for full roadmap.

---

**Questions?** Review the templates in `templates/emails/` or check `utils/email_service.py` for implementation details.
