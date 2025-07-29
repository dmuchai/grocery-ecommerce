from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from models import db
from models.cart import Cart
from models.order import Order
from models.product import Product
from models.user import User
from routes.order import place_order as order_placement

checkout_bp = Blueprint('checkout', __name__, url_prefix='/checkout')

@checkout_bp.route('/', methods=['GET'])
def checkout_page():
    """Render the enhanced checkout page"""
    # Check if user is logged in
    if 'user_id' not in session:
        flash('Please login to proceed with checkout', 'warning')
        return redirect(url_for('user.login'))
    
    # Check if cart is not empty
    cart = session.get('cart', {})
    if not cart:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('cart.get_cart'))
    
    # Get user details for pre-filling form
    user = User.query.get(session['user_id'])
    
    return render_template('checkout.html', cart=cart, user=user)

@checkout_bp.route('/', methods=['POST'])
def checkout_process():
    """Handle checkout form submission and redirect to PesaPal payment"""
    if 'user_id' not in session:
        return jsonify({'error': 'Please login to continue'}), 401
    
    cart = session.get('cart', {})
    if not cart:
        return jsonify({'error': 'Cart is empty'}), 400

    data = request.get_json()
    
    # Extract and validate delivery details
    delivery_details = {
        'full_name': data.get('full_name', '').strip(),
        'email': data.get('email', '').strip(),
        'phone': data.get('phone', '').strip(),
        'address': data.get('address', '').strip(),
        'city': data.get('city', '').strip(),
        'postal_code': data.get('postal_code', '').strip(),
        'delivery_instructions': data.get('delivery_instructions', '').strip()
    }
    
    # Validate required fields
    required_fields = ['full_name', 'email', 'phone', 'address', 'city']
    missing_fields = [field for field in required_fields if not delivery_details[field]]
    
    if missing_fields:
        return jsonify({
            'error': f'Please fill in all required fields: {", ".join(missing_fields)}'
        }), 400
    
    # Option to save delivery details to user profile
    save_to_profile = data.get('save_to_profile', False)
    if save_to_profile:
        try:
            user = User.query.get(session['user_id'])
            if user:
                # Parse full name into first and last name if not already set
                if not user.first_name and not user.last_name:
                    name_parts = delivery_details['full_name'].split(' ', 1)
                    user.first_name = name_parts[0]
                    if len(name_parts) > 1:
                        user.last_name = name_parts[1]
                
                # Update profile with delivery details (only if user fields are empty)
                if not user.phone:
                    user.phone = delivery_details['phone']
                if not user.address:
                    user.address = delivery_details['address']
                if not user.city:
                    user.city = delivery_details['city']
                if not user.postal_code and delivery_details['postal_code']:
                    user.postal_code = delivery_details['postal_code']
                
                user.update_profile_completion()
                db.session.commit()
        except Exception as e:
            print(f"Error saving to profile: {e}")
            # Don't fail checkout if profile save fails
    
    # Store delivery details in session for PesaPal payment processing
    session['delivery_details'] = delivery_details
    session.modified = True
    
    # Return success response - frontend will redirect to payment
    return jsonify({
        'success': True,
        'message': 'Delivery details saved. Redirecting to payment...',
        'redirect_url': url_for('payment.initiate_payment')
    }), 200

@checkout_bp.route('/success', methods=['GET'])
def checkout_success():
    """Render the order success page."""
    return render_template('checkout_success.html')
