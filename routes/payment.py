from flask import Blueprint, request, render_template, redirect, url_for, flash, session, jsonify
import requests
import jwt
import json
import os
from datetime import datetime, timedelta
import uuid
# Use the same database setup as your main app
from models import db
from models.user import User
from models.product import Product
from models.order import Order
from models.order_item import OrderItem

payment_bp = Blueprint('payment', __name__)

class PesaPalAPI:
    def __init__(self):
        self.consumer_key = os.getenv('PESAPAL_CONSUMER_KEY')
        self.consumer_secret = os.getenv('PESAPAL_CONSUMER_SECRET')
        self.base_url = os.getenv('PESAPAL_BASE_URL', 'https://pay.pesapal.com/v3')
        self.ipn_id = os.getenv('PESAPAL_IPN_ID')
        self.callback_url = os.getenv('PESAPAL_CALLBACK_URL')
        self.notification_url = os.getenv('PESAPAL_NOTIFICATION_URL')
        self.auth_token = None
        
    def get_auth_token(self):
        """Get authentication token from PesaPal"""
        auth_url = f"{self.base_url}/api/Auth/RequestToken"
        
        payload = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(auth_url, json=payload, headers=headers)
            if response.status_code == 200:
                data = response.json()
                self.auth_token = data.get('token')
                return self.auth_token
            else:
                return None
        except Exception as e:
            print(f"Error getting auth token: {e}")
            return None
    
    def register_ipn_url(self):
        """Register IPN URL with PesaPal - Use this only during setup"""
        # This method is now only for setup/admin purposes
        # Don't call this during payment transactions
        if not self.auth_token:
            self.get_auth_token()
            
        ipn_url = f"{self.base_url}/api/URLSetup/RegisterIPN"
        
        payload = {
            "url": self.notification_url,
            "ipn_notification_type": "GET"
        }
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }
        
        try:
            response = requests.post(ipn_url, json=payload, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error registering IPN: {e}")
            return None
    
    def get_transaction_status(self, order_tracking_id):
        """Get transaction status from PesaPal"""
        if not self.auth_token:
            self.get_auth_token()
            
        status_url = f"{self.base_url}/api/Transactions/GetTransactionStatus"
        
        params = {
            'orderTrackingId': order_tracking_id
        }
        
        headers = {
            'Accept': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }
        
        try:
            response = requests.get(status_url, params=params, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error getting transaction status: {e}")
            return None
    
    def submit_order_request(self, order_data):
        """Submit order request to PesaPal"""
        if not self.auth_token:
            self.get_auth_token()
            
        submit_url = f"{self.base_url}/api/Transactions/SubmitOrderRequest"
        
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'Authorization': f'Bearer {self.auth_token}'
        }
        
        try:
            response = requests.post(submit_url, json=order_data, headers=headers)
            if response.status_code == 200:
                return response.json()
            else:
                return None
        except Exception as e:
            print(f"Error submitting order: {e}")
            return None

# Initialize PesaPal API
pesapal_api = PesaPalAPI()

@payment_bp.route('/initiate', methods=['POST'])
def initiate_payment():
    """Initiate payment process"""
    
    if 'user_id' not in session:
        flash('Please login to continue with payment', 'warning')
        return redirect(url_for('user.login'))
    
    try:
        # Get cart items from session (as your app currently uses)
        cart = session.get('cart', {})
        print(f"Cart items: {cart}")
        if not cart:
            print("Cart is empty, redirecting to home")
            flash('Your cart is empty', 'warning')
            return redirect(url_for('home'))
        
        # Calculate cart total from session cart
        total_amount = 0
        cart_items = []
        
        # Get products from database to calculate total
        for product_id, cart_item in cart.items():
            product = Product.query.get(int(product_id))
            if product:
                quantity = cart_item['quantity']  # Extract quantity from cart item dict
                item_total = product.price * quantity
                total_amount += item_total
                cart_items.append({
                    'product_id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity,
                    'total': item_total
                })
        
        # Get user details
        user = db.session.get(User, session['user_id'])
        if not user:
            flash('User not found', 'error')
            return redirect(url_for('user.login'))
        
        # Get delivery details from checkout or user profile with intelligent fallbacks
        delivery_details = session.get('delivery_details', {})
        
        # Smart fallback system: checkout > user profile > defaults
        customer_name = (
            delivery_details.get('full_name') or 
            user.get_full_name() or 
            user.username
        )
        
        customer_email = (
            delivery_details.get('email') or 
            user.email
        )
        
        customer_phone = (
            delivery_details.get('phone') or 
            user.phone or 
            ''
        )
        
        customer_address = (
            delivery_details.get('address') or 
            user.address or 
            ''
        )
        
        customer_city = (
            delivery_details.get('city') or 
            user.city or 
            ''
        )
        
        customer_postal_code = (
            delivery_details.get('postal_code') or 
            user.postal_code or 
            ''
        )
        
        customer_state = (
            delivery_details.get('state') or 
            user.state or 
            ''
        )
        
        delivery_instructions = delivery_details.get('delivery_instructions', '')
        
        # Generate unique order ID
        order_id = f"ORDER_{uuid.uuid4().hex[:8].upper()}_{int(datetime.now().timestamp())}"
        
        # Create order in database using your existing Order model with delivery details
        order_address = f"{customer_address}, {customer_city}"
        if customer_postal_code:
            order_address += f", {customer_postal_code}"
        if delivery_instructions:
            order_address += f" (Instructions: {delivery_instructions})"
            
        new_order = Order(
            user_id=session['user_id'],
            customer_name=customer_name,
            email=customer_email,
            address=order_address,
            total_price=total_amount,
            status='pending'
        )
        
        db.session.add(new_order)
        db.session.flush()  # Get the order ID
        
        # Save order items using your existing OrderItem model
        for item in cart_items:
            order_item = OrderItem(
                order_id=new_order.id,
                product_id=item['product_id'],
                quantity=item['quantity'],
                price=item['price']
            )
            db.session.add(order_item)
        
        db.session.commit()
        
        # Prepare PesaPal order data
        # Create PesaPal API instance
        pesapal_api = PesaPalAPI()
        
        order_data = {
            "id": order_id,
            "currency": "KES",
            "amount": float(total_amount),
            "description": f"Denncathy Fresh Basket Order #{order_id}",
            "callback_url": pesapal_api.callback_url,
            "notification_id": pesapal_api.ipn_id,  # Use stored IPN ID
            "billing_address": {
                "email_address": customer_email,
                "phone_number": customer_phone,
                "country_code": "KE",
                "first_name": customer_name.split()[0] if customer_name else "Customer",
                "last_name": customer_name.split()[-1] if len(customer_name.split()) > 1 else "",
                "line_1": customer_address,
                "city": customer_city,
                "state": "",  # Kenya doesn't use states
                "postal_code": customer_postal_code,
                "zip_code": customer_postal_code
            }
        }
        
        # Submit order to PesaPal
        pesapal_response = pesapal_api.submit_order_request(order_data)
        
        if pesapal_response and pesapal_response.get('status') == '200':
            # Store order tracking ID in the database
            new_order.status = 'payment_initiated'
            # Store PesaPal tracking ID if you have a field for it
            db.session.commit()
            
            # Store order info in session
            session['current_order_id'] = order_id
            session['pesapal_tracking_id'] = pesapal_response.get('order_tracking_id')
            session['db_order_id'] = new_order.id
            
            # Redirect to PesaPal payment page
            return redirect(pesapal_response.get('redirect_url'))
        else:
            # If payment fails, delete the order
            db.session.delete(new_order)
            db.session.commit()
            flash('Payment initialization failed. Please try again.', 'danger')
            return redirect(url_for('home'))
            
    except Exception as e:
        db.session.rollback()
        flash(f'An error occurred: {str(e)}', 'danger')
        return redirect(url_for('home'))

@payment_bp.route('/callback')
def payment_callback():
    """Handle payment callback from PesaPal"""
    order_tracking_id = request.args.get('OrderTrackingId')
    order_merchant_reference = request.args.get('OrderMerchantReference')
    
    if order_tracking_id:
        # Query PesaPal for payment status
        status_response = pesapal_api.get_transaction_status(order_tracking_id)
        
        if status_response:
            payment_status = status_response.get('payment_status_description', '').upper()
            
            # Update order status in database using SQLAlchemy
            # Find order by the order reference or session info
            if 'db_order_id' in session:
                order = Order.query.get(session['db_order_id'])
                if order:
                    order.status = payment_status.lower()
                    db.session.commit()
            
            if payment_status == 'COMPLETED':
                # Clear cart and delivery details after successful payment
                session.pop('cart', None)
                session.pop('delivery_details', None)
                session.pop('current_order_id', None)
                session.pop('pesapal_tracking_id', None)
                session.pop('db_order_id', None)
                session.modified = True
                flash('Payment successful! Your order has been confirmed.', 'success')
                return render_template('payment/success.html', 
                                     order_id=order_merchant_reference,
                                     tracking_id=order_tracking_id)
            elif payment_status == 'FAILED':
                flash('Payment failed. Please try again.', 'danger')
                return render_template('payment/failed.html', 
                                     order_id=order_merchant_reference)
            else:
                flash('Payment is being processed. You will be notified once complete.', 'info')
                return render_template('payment/processing.html', 
                                     order_id=order_merchant_reference)
    
    flash('Payment status unknown. Please contact support.', 'warning')
    return redirect(url_for('home'))

@payment_bp.route('/ipn', methods=['GET', 'POST'])
def payment_ipn():
    """Handle Instant Payment Notifications from PesaPal"""
    order_tracking_id = request.args.get('OrderTrackingId')
    order_merchant_reference = request.args.get('OrderMerchantReference')
    
    if order_tracking_id:
        # Query PesaPal for latest payment status
        status_response = pesapal_api.get_transaction_status(order_tracking_id)
        
        if status_response:
            payment_status = status_response.get('payment_status_description', '').upper()
            
            # Update order status in database
            # You might need to find the order by tracking ID if you store it
            # For now, we'll update based on session or implement a lookup
            
            # Log the IPN for debugging
            print(f"IPN received - Order: {order_merchant_reference}, Status: {payment_status}")
    
    return '', 200

@payment_bp.route('/cancelled')
def payment_cancelled():
    """Handle cancelled payments"""
    flash('Payment was cancelled.', 'warning')
    return render_template('payment/cancelled.html')

@payment_bp.route('/status/<order_id>')
def check_payment_status(order_id):
    """Check payment status for an order"""
    if 'user_id' not in session:
        flash('Please login to view order status.', 'warning')
        return redirect(url_for('user.login'))
    
    # Find order by ID and user
    order = Order.query.filter_by(
        user_id=session['user_id']
    ).first()
    
    if order:
        return render_template('payment/status.html', order=order)
    else:
        flash('Order not found.', 'danger')
        return redirect(url_for('home'))
