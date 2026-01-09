# Quick Implementation Guide: Order Management + Email Notifications

## Part 1: Order Status Recovery (Immediate)

### 1. Add Order Status Page Route

```python
# Add to routes/order.py

@order_bp.route('/status/<order_ref>', methods=['GET'])
def order_status(order_ref):
    """
    Public order status page - no login required
    Shows order details, status, estimated delivery
    """
    order = Order.query.filter_by(merchant_reference=order_ref).first()
    
    if not order:
        flash('Order not found', 'warning')
        return redirect(url_for('home'))
    
    # Calculate estimated delivery (add 2-3 days to order date)
    estimated_delivery = order.created_at + timedelta(days=3)
    
    return render_template('order_status.html', 
                         order=order, 
                         estimated_delivery=estimated_delivery)


@order_bp.route('/<order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """
    Allow cancellation if order is still payment_initiated or pending
    Refund will be manual (admin processes it)
    """
    if 'user_id' not in session:
        return jsonify({'error': 'Login required'}), 401
    
    order = db.session.get(Order, order_id)
    if not order or order.user_id != session['user_id']:
        return jsonify({'error': 'Order not found'}), 404
    
    # Only allow cancellation if not yet completed
    if order.status in ['payment_initiated', 'pending']:
        order.status = 'cancelled'
        db.session.commit()
        
        # Send cancellation email
        send_order_email(order, 'order_cancelled')
        
        return jsonify({'success': True, 'message': 'Order cancelled. You will receive a refund within 3-5 days.'})
    
    return jsonify({'error': 'Order cannot be cancelled at this stage'}), 400


@order_bp.route('/<order_id>/retry-payment', methods=['POST'])
def retry_payment(order_id):
    """
    Allow customer to retry payment for failed orders
    """
    order = db.session.get(Order, order_id)
    
    if not order or (order.user_id and order.user_id != session.get('user_id')):
        return jsonify({'error': 'Order not found'}), 404
    
    if order.status not in ['pending', 'failed']:
        return jsonify({'error': 'This order cannot be retried'}), 400
    
    # Prepare to retry payment - set status back to payment_initiated
    order.status = 'payment_initiated'
    db.session.commit()
    
    # Redirect to payment initiation
    return jsonify({
        'success': True,
        'redirect_url': url_for('payment.initiate_payment')
    })
```

### 2. Create Order Status Template

```html
<!-- templates/order_status.html -->
{% extends "base.html" %}

{% block content %}
<div class="container mt-5">
    <div class="row">
        <div class="col-md-8">
            <!-- Order Header -->
            <div class="card mb-4">
                <div class="card-header bg-primary text-white">
                    <h4>Order #{{ order.merchant_reference }}</h4>
                    <small>Placed {{ order.created_at.strftime('%Y-%m-%d %H:%M') }}</small>
                </div>
                <div class="card-body">
                    <div class="row">
                        <div class="col-md-6">
                            <strong>Status:</strong>
                            <span class="badge bg-{{ status_color(order.status) }}">{{ order.status|upper }}</span>
                            <br><br>
                            <strong>Estimated Delivery:</strong> 
                            {{ estimated_delivery.strftime('%Y-%m-%d') }}
                        </div>
                        <div class="col-md-6">
                            <strong>Total Amount:</strong> KES {{ order.total_price|round(2) }}
                            <br><br>
                            <strong>Tracking ID:</strong> 
                            <code>{{ order.pesapal_tracking_id or 'N/A' }}</code>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Order Items -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Items</h5>
                </div>
                <div class="card-body">
                    <table class="table table-sm">
                        <thead>
                            <tr>
                                <th>Product</th>
                                <th>Qty</th>
                                <th>Price</th>
                                <th>Total</th>
                            </tr>
                        </thead>
                        <tbody>
                            {% for item in order.items %}
                            <tr>
                                <td>{{ item.product.name }}</td>
                                <td>{{ item.quantity }}</td>
                                <td>KES {{ item.price|round(2) }}</td>
                                <td>KES {{ (item.quantity * item.price)|round(2) }}</td>
                            </tr>
                            {% endfor %}
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Delivery Address -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Delivery Address</h5>
                </div>
                <div class="card-body">
                    <strong>{{ order.customer_name }}</strong><br>
                    {{ order.address }}<br>
                    <strong>Phone:</strong> {{ order.phone or 'N/A' }}
                </div>
            </div>

            <!-- Status Timeline -->
            <div class="card mb-4">
                <div class="card-header">
                    <h5>Status Timeline</h5>
                </div>
                <div class="card-body">
                    <div class="timeline">
                        <div class="timeline-item">
                            <span class="timeline-marker">✓</span>
                            <h6>Order Placed</h6>
                            <small>{{ order.created_at.strftime('%Y-%m-%d %H:%M') }}</small>
                        </div>
                        {% if order.status != 'pending' %}
                        <div class="timeline-item">
                            <span class="timeline-marker">✓</span>
                            <h6>Payment Received</h6>
                            <small>Status: {{ order.status|upper }}</small>
                        </div>
                        {% endif %}
                        {% if order.status == 'shipped' or order.status == 'delivered' %}
                        <div class="timeline-item">
                            <span class="timeline-marker">✓</span>
                            <h6>Shipped</h6>
                            <small>On its way!</small>
                        </div>
                        {% endif %}
                        {% if order.status == 'delivered' %}
                        <div class="timeline-item">
                            <span class="timeline-marker">✓</span>
                            <h6>Delivered</h6>
                            <small>Order delivered</small>
                        </div>
                        {% endif %}
                    </div>
                </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-4">
                {% if order.status in ['pending', 'payment_initiated'] %}
                <button class="btn btn-warning" onclick="retryPayment()">
                    Retry Payment
                </button>
                {% endif %}
                
                {% if order.status in ['pending', 'payment_initiated'] %}
                <button class="btn btn-danger" onclick="cancelOrder()">
                    Cancel Order
                </button>
                {% endif %}
                
                <a href="/" class="btn btn-secondary">Back to Home</a>
            </div>
        </div>
    </div>
</div>

<style>
.timeline {
    position: relative;
    padding: 20px 0;
}

.timeline-item {
    padding-left: 40px;
    margin-bottom: 20px;
    position: relative;
}

.timeline-marker {
    position: absolute;
    left: 0;
    width: 24px;
    height: 24px;
    background-color: #28a745;
    border-radius: 50%;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
}

.timeline-item h6 {
    margin: 0 0 5px 0;
    font-weight: bold;
}

.timeline-item small {
    color: #666;
}
</style>

<script>
function retryPayment() {
    fetch(`/order/{{ order.id }}/retry-payment`, {
        method: 'POST'
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            window.location.href = data.redirect_url;
        } else {
            alert('Error: ' + data.error);
        }
    });
}

function cancelOrder() {
    if (!confirm('Are you sure? This will cancel your order and initiate a refund.')) return;
    
    fetch(`/order/{{ order.id }}/cancel`, {
        method: 'POST'
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert(data.message);
            location.reload();
        } else {
            alert('Error: ' + data.error);
        }
    });
}
</script>
{% endblock %}
```

---

## Part 2: Email Notifications (Quick Setup)

### 1. Install Flask-Mail

```bash
pip install Flask-Mail
```

### 2. Update config.py

```python
# config.py

# Email configuration
MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', True)
MAIL_USERNAME = os.getenv('MAIL_USERNAME')  # your@denncathy.co.ke
MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')  # Gmail app password
MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@denncathy.co.ke')
ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@denncathy.co.ke')
```

### 3. Create Email Service

```python
# utils/email_service.py

from flask_mail import Mail, Message
from flask import render_template, current_app
import logging

mail = Mail()
logger = logging.getLogger(__name__)

def send_order_confirmation_email(order, customer_email):
    """Send order confirmation to customer"""
    try:
        subject = f"Order Confirmation - {order.merchant_reference}"
        
        msg = Message(
            subject=subject,
            recipients=[customer_email],
            html=render_template('emails/order_confirmation.html', 
                               order=order),
            reply_to=current_app.config['ADMIN_EMAIL']
        )
        mail.send(msg)
        logger.info(f"Order confirmation sent to {customer_email} for order {order.id}")
    except Exception as e:
        logger.error(f"Failed to send order confirmation: {e}")


def send_new_order_alert_to_admin(order):
    """Alert admin of new order"""
    try:
        subject = f"New Order Received - {order.merchant_reference}"
        
        msg = Message(
            subject=subject,
            recipients=[current_app.config['ADMIN_EMAIL']],
            html=render_template('emails/admin_new_order.html', 
                               order=order)
        )
        mail.send(msg)
        logger.info(f"New order alert sent to admin for order {order.id}")
    except Exception as e:
        logger.error(f"Failed to send admin alert: {e}")


def send_payment_received_email(order):
    """Confirm payment received"""
    try:
        subject = f"Payment Received - {order.merchant_reference}"
        
        msg = Message(
            subject=subject,
            recipients=[order.email],
            html=render_template('emails/payment_received.html', 
                               order=order)
        )
        mail.send(msg)
        logger.info(f"Payment confirmation sent for order {order.id}")
    except Exception as e:
        logger.error(f"Failed to send payment confirmation: {e}")


def send_order_shipped_email(order):
    """Notify customer order has shipped"""
    try:
        subject = f"Your Order Has Shipped - {order.merchant_reference}"
        
        msg = Message(
            subject=subject,
            recipients=[order.email],
            html=render_template('emails/order_shipped.html', 
                               order=order)
        )
        mail.send(msg)
        logger.info(f"Shipment notification sent for order {order.id}")
    except Exception as e:
        logger.error(f"Failed to send shipment email: {e}")
```

### 4. Update app.py to initialize mail

```python
# app.py

from utils.email_service import mail

# After creating app:
mail.init_app(app)
```

### 5. Create Email Templates

```html
<!-- templates/emails/order_confirmation.html -->
<!DOCTYPE html>
<html>
<head>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: 0 auto; }
        .header { background-color: #28a745; color: white; padding: 20px; }
        .content { padding: 20px; }
        .items-table { width: 100%; border-collapse: collapse; }
        .items-table th { background-color: #f5f5f5; padding: 10px; text-align: left; }
        .items-table td { padding: 10px; border-bottom: 1px solid #ddd; }
        .footer { background-color: #f5f5f5; padding: 10px; text-align: center; color: #666; font-size: 12px; }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h2>Order Confirmation</h2>
        </div>
        
        <div class="content">
            <p>Hi {{ order.customer_name }},</p>
            <p>Thank you for your order! We're excited to deliver fresh groceries to your doorstep.</p>
            
            <h4>Order Details</h4>
            <p><strong>Order Reference:</strong> {{ order.merchant_reference }}</p>
            <p><strong>Order Date:</strong> {{ order.created_at.strftime('%Y-%m-%d %H:%M') }}</p>
            <p><strong>Total Amount:</strong> KES {{ order.total_price|round(2) }}</p>
            
            <h4>Items Ordered</h4>
            <table class="items-table">
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Qty</th>
                        <th>Price</th>
                        <th>Total</th>
                    </tr>
                </thead>
                <tbody>
                    {% for item in order.items %}
                    <tr>
                        <td>{{ item.product.name }}</td>
                        <td>{{ item.quantity }}</td>
                        <td>KES {{ item.price|round(2) }}</td>
                        <td>KES {{ (item.quantity * item.price)|round(2) }}</td>
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
            
            <h4>Delivery Address</h4>
            <p>{{ order.address }}</p>
            
            <p><a href="https://denncathy.co.ke/order/track/{{ order.merchant_reference }}" 
                  style="display: inline-block; background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">
                Track Your Order
            </a></p>
            
            <p>If you have any questions, please reply to this email or contact us at +254 710 583 101</p>
            
            <p>Best regards,<br>Denncathy Fresh Basket Team</p>
        </div>
        
        <div class="footer">
            <p>© 2026 Denncathy Fresh Basket. All rights reserved.</p>
        </div>
    </div>
</body>
</html>
```

### 6. Call Email Functions in routes/payment.py

```python
# At end of initiate_payment, after successful redirect_url received:

from utils.email_service import send_order_confirmation_email, send_new_order_alert_to_admin

# ... after order creation ...

# Send emails
send_order_confirmation_email(new_order, customer_email)
send_new_order_alert_to_admin(new_order)

return redirect(pesapal_response.get('redirect_url'))
```

---

## Part 3: .env Updates Needed

```bash
# Email Configuration
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password  # Generate from Google Account Security
MAIL_DEFAULT_SENDER=noreply@denncathy.co.ke
ADMIN_EMAIL=admin@denncathy.co.ke
```

**Note**: For Gmail, you need to:
1. Enable 2FA on your Google account
2. Generate an "App Password" at https://myaccount.google.com/apppasswords
3. Use that password in MAIL_PASSWORD

---

## Testing the Setup

```bash
# In production:
python3 -c "
from app import app, mail
from utils.email_service import send_order_confirmation_email
from models import Order

with app.app_context():
    order = Order.query.first()
    send_order_confirmation_email(order, 'test@example.com')
    print('Test email sent!')
"
```

This gives you:
✅ Order status pages customers can access
✅ Order cancellation/retry payment
✅ Email notifications to customers and admin
✅ Public order tracking (no login required)

Next steps would be: refund management, admin dashboard, inventory tracking, reviews.

