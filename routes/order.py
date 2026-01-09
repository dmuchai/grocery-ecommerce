import uuid
from flask import Blueprint, request, jsonify, session, render_template
from datetime import timedelta
from models import db
from models.order import Order
from models.order_item import OrderItem
from utils.email_service import send_order_cancelled_email
import logging

logger = logging.getLogger(__name__)
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


@order_bp.route('/track/<order_ref>', methods=['GET'])
def track_order(order_ref):
    """
    Public order tracking page - no login required
    Shows order status, items, and estimated delivery
    """
    order = Order.query.filter_by(merchant_reference=order_ref).first()
    
    if not order:
        return render_template('order_not_found.html', order_ref=order_ref), 404
    
    # Calculate estimated delivery (2-3 days from order date)
    estimated_delivery = order.created_at + timedelta(days=3)
    
    return render_template('order_status.html', 
                         order=order, 
                         estimated_delivery=estimated_delivery)


@order_bp.route('/<int:order_id>/cancel', methods=['POST'])
def cancel_order(order_id):
    """
    Allow cancellation if order is still payment_initiated or pending
    """
    order = db.session.get(Order, order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Check permission: user can only cancel their own orders or guest orders in session
    if order.user_id and order.user_id != session.get('user_id'):
        return jsonify({'error': 'Not authorized'}), 403
    
    # Only allow cancellation if payment not yet completed
    if order.status not in ['pending', 'payment_initiated', 'failed']:
        return jsonify({'error': f'Cannot cancel order with status: {order.status}'}), 400
    
    try:
        order.status = 'cancelled'
        db.session.commit()
        
        # Send cancellation email
        send_order_cancelled_email(order)
        logger.info(f"Order {order_id} cancelled and email sent to {order.email}")
        
        return jsonify({
            'success': True, 
            'message': 'Order cancelled successfully. You will receive a refund within 3-5 business days.'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error cancelling order {order_id}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to cancel order'}), 500


@order_bp.route('/<int:order_id>/retry-payment', methods=['POST'])
def retry_payment(order_id):
    """
    Allow customer to retry payment for failed orders
    """
    order = db.session.get(Order, order_id)
    
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    # Check permission
    if order.user_id and order.user_id != session.get('user_id'):
        return jsonify({'error': 'Not authorized'}), 403
    
    if order.status not in ['pending', 'payment_initiated', 'failed']:
        return jsonify({'error': f'Cannot retry payment for order with status: {order.status}'}), 400
    
    try:
        # Set status back to allow payment retry
        order.status = 'payment_initiated'
        db.session.commit()
        
        logger.info(f"Order {order_id} set to retry payment")
        
        return jsonify({
            'success': True,
            'redirect_url': '/payment/initiate'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error setting up retry payment for {order_id}: {e}", exc_info=True)
        return jsonify({'error': 'Failed to retry payment'}), 500
