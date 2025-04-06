import uuid
from flask import Blueprint, request, jsonify, session, render_template
from models import db
from models.order import Order
from models.order_item import OrderItem

order_bp = Blueprint("order", __name__, url_prefix="/orders")

DEFAULT_GUEST_USER_ID = 0  # Use 0 to identify guest orders

@order_bp.route("/place", methods=["POST"])
def place_order():
    """Handle order placement for logged-in or guest users"""
    cart = session.get('cart', {})
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400

    data = request.get_json()
    customer_name = data.get('customer_name')
    email = data.get('email')
    address = data.get('address')

    if not email or not address or not customer_name:
        return jsonify({'error': 'Missing customer details'}), 400

    try:
        # Determine user_id: if logged in, use it; otherwise use the guest ID.
        user_id = session.get('user_id', DEFAULT_GUEST_USER_ID)

        # If it's a guest user, ensure a unique guest identifier is stored in the session
        guest_identifier = None
        if user_id == DEFAULT_GUEST_USER_ID:
            if 'guest_id' not in session:
                session['guest_id'] = str(uuid.uuid4())
            guest_identifier = session['guest_id']

        # Calculate total price from cart data
        total_price = sum(item['price'] * item['quantity'] for item in cart.values())

        # Create the order
        new_order = Order(
            user_id=user_id,
            guest_identifier=guest_identifier,
            customer_name=customer_name,
            email=email,
            address=address,
            total_price=total_price,
            status="Pending"
        )
        db.session.add(new_order)
        db.session.commit()  # Commit to generate order ID

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

        # Clear cart after successful order
        session.pop('cart', None)
        session.modified = True

        return jsonify({
            'message': 'Order placed successfully',
            'order_id': new_order.id,
            'email': email
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to place order: {str(e)}'}), 500

@order_bp.route('/history', methods=['GET'])
def order_history():
    user_id = session.get('user_id')
    guest_id = session.get('guest_identifier')  # set during guest checkout

    if not user_id and not guest_id:
        return render_template('order_history.html', orders=[])

    if user_id:
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    else:
        orders = Order.query.filter_by(guest_identifier=guest_id).order_by(Order.created_at.desc()).all()

    return render_template('order_history.html', orders=orders)
