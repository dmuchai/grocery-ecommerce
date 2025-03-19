import json
import logging
import uuid
from flask import Blueprint, request, jsonify, session, render_template
from models import db
from models.product import Product

logging.basicConfig(level=logging.DEBUG)

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.before_request
def initialize_cart():
    """
    Ensure the session has a unique session_id for guests.
    This is optional if you only use session['cart'].
    """
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())  # Unique ID for guests

@cart_bp.route('/', methods=['GET'])
def get_cart():
    """
    Retrieve cart items from the session-based dictionary.
    """
    user_id = session.get('user_id')
    session_id = session.get('session_id')

    logging.debug(f"Fetching cart for: user_id={user_id}, session_id={session_id}")

    # cart_dict is a dictionary keyed by product_id (string)
    cart_dict = session.get('cart', {})

    cart_items = []
    total = 0

    # Build a list of items by looking up each product in the DB
    for product_id_str, item_data in cart_dict.items():
        product_id = int(product_id_str)
        product = Product.query.get(product_id)
        if not product:
            logging.warning(f"Product with ID {product_id} not found in the database!")
            continue

        subtotal = product.price * item_data['quantity']
        cart_items.append({
            "id": product.id,
            "name": product.name,
            "image_url": product.image_url,
            "price": float(product.price),
            "quantity": item_data['quantity'],
            "subtotal": subtotal
        })
        total += subtotal

    logging.debug(f"Cart contents: {cart_items}, Total: {total}")

    response_data = {
        'cart': cart_items,
        'total': total,
        'is_logged_in': bool(user_id)
    }

    # If this is an AJAX request, return JSON
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify(response_data)

    # Otherwise, render an HTML template
    return render_template('cart.html', **response_data)

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    """
    Add a product to the session-based cart.
    Expects JSON: { "product_id": <int>, "quantity": <int> }
    """
    data = request.json or {}
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Retrieve or create the cart dictionary in session
    cart_dict = session.get('cart', {})
    product_id_str = str(product_id)

    if product_id_str in cart_dict:
        # Increase quantity if product is already in cart
        cart_dict[product_id_str]['quantity'] += quantity
    else:
        # Create a new cart item in the session
        cart_dict[product_id_str] = {
            'id': product.id,
            'name': product.name,
            'image_url': product.image_url,
            'price': float(product.price),
            'quantity': quantity
        }

    # Save the updated cart back to session
    session['cart'] = cart_dict
    session.modified = True

    return jsonify({'message': 'Item added to cart'}), 201
