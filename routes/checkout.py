from flask import Blueprint, request, jsonify, session
from models import db
from models.order import Order, OrderItem
from models.product import Product

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/', methods=['POST'])
def place_order():
    cart = session.get('cart', {})
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400

    data = request.get_json()
    customer_name = data.get('customer_name')
    address = data.get('address')

    if not customer_name or not address:
        return jsonify({'error': 'Missing customer details'}), 400

    try:
        # Create a new order
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())
        new_order = Order(customer_name=customer_name, address=address, total_price=total_price)

        db.session.add(new_order)
        db.session.commit()  # Commit order first to generate an ID

        # Add order items
        order_items = []
        for product_id, item in cart.items():
            order_item = OrderItem(order_id=new_order.id, product_id=int(product_id), quantity=item['quantity'], price=item['price'])
            order_items.append(order_item)

        db.session.add_all(order_items)
        db.session.commit()

        session.pop('cart', None)  # Clear cart after checkout
        session.modified = True

        return jsonify({'message': 'Order placed successfully', 'order_id': new_order.id}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to place order: {str(e)}'}), 500
