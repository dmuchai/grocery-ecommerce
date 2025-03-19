from flask import Blueprint, request, jsonify, session, render_template
from models import db
from models.cart import Cart
from models.order import Order
from models.product import Product
from routes.order import place_order as order_placement

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/', methods=['GET'])
def checkout_page():
    """Render the checkout page"""
    cart = session.get('cart', {})  # Get cart items
    return render_template('checkout.html', cart=cart)

@checkout_bp.route('/', methods=['POST'])
def checkout_process():
    """Handle checkout and place order"""
    cart = session.get('cart', {})
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400

    data = request.get_json()
    customer_name = data.get('customer_name')
    email = data.get('email')

    if not customer_name or not email:
        return jsonify({'error': 'Customer name and email are required'}), 400

    # Redirect order placement to `routes/order.py`
    response = order_placement()

    if response[1] == 201:  # If order placement is successful
        session.pop('cart', None)  # Clear cart
        session.modified = True

    return response

@checkout_bp.route('/success', methods=['GET'])
def checkout_success():
    """Render the order success page."""
    return render_template('checkout_success.html')
