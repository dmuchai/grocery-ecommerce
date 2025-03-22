from flask import Blueprint, request, jsonify, session
from models import db
from models.order import Order
from models.cart import Cart
from models.order_item import OrderItem

order_bp = Blueprint("order", __name__, url_prefix="/orders")
DEFAULT_GUEST_USER_ID = 0  # Use 0 for guest order

@order_bp.route("/place", methods=["POST"])
def place_order():
    """Handle order placementi for logged-in or guest users"""
    cart = session.get('cart', {})
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400

    data = request.get_json()
    customer_name = data.get('customer_name')
    email = data.get('email')
    address = data.get('address')

    if not email or not address:
        return jsonify({'error': 'Missing customer details'}), 400

    try:
        # Determine user_id: if logged in, use it; otherwise use the default guest ID.
        user_id = session.get('user_id', DEFAULT_GUEST_USER_ID)

        # Calculate total price from cart data
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())

        new_order = Order(
                user_id=user_id,
                customer_name=customer_name,
                email=email,
                address=address,
                total_price=total_price
        )

        db.session.add(new_order)
        db.session.commit()  # Commit order first to generate an order ID

        # Create OrderItem records for each cart item
        order_items = []
        for product_id, item in cart.items():
            order_item = OrderItem(
                    order_id=new_order.id,
                    product_id=int(product_id),
                    quantity=item['quantity'],
                    price=item['price']
            )
            order_items.append(order_item)

        db.session.add_all(order_items)
        db.session.commit()

        session.pop('cart', None)  # Clear cart after checkout
        session.modified = True

        return jsonify({
            'message': 'Order placed successfully',
            'order_id': new_order.id,
            'email': email
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to place order: {str(e)}'}), 500
