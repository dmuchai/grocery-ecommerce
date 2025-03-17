from flask import Blueprint, request, jsonify, session, render_template
from models import db
from models.product import Product

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.before_request
def initialize_cart():
    if 'cart' not in session:
        session['cart'] = []

@cart_bp.route('/', methods=['GET'])
def get_cart():
    cart = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart)
    for item in cart:
        product = Product.query.get(item["id"])
        item["image_url"] = product.image_url if product else "default.jpg"

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'cart': cart, 'total': total})
    return render_template('cart.html')

@cart_bp.route('/add', methods=['POST'])
def add_to_cart():
    data = request.get_json()
    product_id = data.get('product_id')
    quantity = data.get('quantity', 1)

    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    # Get cart from session
    cart = session.get('cart', [])

    # Check if product is already in cart
    for item in cart:
        if item['id'] == product.id:
            item['quantity'] += quantity
            item['subtotal'] = item['quantity'] * item['price']
            break
    else:
        cart.append({
            'id': product.id,
            'name': product.name,
            'image_url': product.image_url,
            'price': float(product.price),
            'quantity': quantity,
            'subtotal': float(product.price) * quantity
        })

    session['cart'] = cart
    session.modified = True

    return jsonify({'message': 'Product added to cart', 'cart': cart})

@cart_bp.route('/remove/<int:product_id>', methods=['POST'])
def remove_from_cart(product_id):
    cart = session.get('cart', [])
    cart = [item for item in cart if item['id'] != product_id]
    session['cart'] = cart
    session.modified = True
    return jsonify({'message': 'Product removed', 'cart': cart})

@cart_bp.route('/clear', methods=['POST'])
def clear_cart():
    session['cart'] = []
    session.modified = True
    return jsonify({'message': 'Cart cleared'})
