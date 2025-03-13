from flask import Blueprint, request, jsonify, session
from models import db
from models.product import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

# Ensure session is configured properly in app.py
@cart_bp.route('/', methods=['GET'])
def get_cart():
    cart = session.get('cart', {})
    return jsonify({'cart': cart, 'total_items': sum(item['quantity'] for item in cart.values())}), 200

# ADD item to cart
@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = str(data.get('product_id'))
    quantity = int(data.get('quantity', 1))

    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    cart = session.get('cart', {})

    if product_id in cart:
        cart[product_id]['quantity'] += quantity
    else:
        cart[product_id] = {
            'name': product.name,
            'price': product.price,
            'quantity': quantity,
            'image_url': product.image_url
        }

    session['cart'] = cart
    session.modified = True  # Ensure session updates

    return jsonify({'message': f'{product.name} added to cart', 'cart': cart}), 200

# REMOVE item from cart
@cart_bp.route('/remove/<int:product_id>', methods=['DELETE'])
def remove_from_cart(product_id):
    cart = session.get('cart', {})
    product_id = str(product_id)

    if product_id in cart:
        del cart[product_id]
        session['cart'] = cart
        session.modified = True
        return jsonify({'message': 'Product removed from cart', 'cart': cart}), 200
    
    return jsonify({'error': 'Product not found in cart'}), 404

# CLEAR the cart
@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    session.pop('cart', None)
    session.modified = True
    return jsonify({'message': 'Cart cleared'}), 200
