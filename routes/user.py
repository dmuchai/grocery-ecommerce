from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from models import db, Cart
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash

# Users Blueprint
user_bp = Blueprint('user', __name__)

# Serve the Register Page
@user_bp.route('/register', methods=['GET'])
def show_register():
    """Display the register page."""
    return render_template('register.html')

# Register a New User
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.form

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    # Validate form input
    if not all([username, email, password]):
        return render_template(
            'register.html',
            error="All fields are required.",
            username=username,
            email=email
        ), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        # Redirect to login page with flash message
        flash("An account with this email already exists. Please log in.", "warning")
        return redirect(url_for('user.show_login'))

    # Create and save user
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    # Log in the user
    session['user_id'] = new_user.id

    return redirect(url_for('home'))

# Serve the Login Page
@user_bp.route('/login', methods=['GET'])
def show_login():
    """Display the login page."""
    return render_template('login.html')

# Login User
@user_bp.route('/login', methods=['POST'])
def login():
    """Authenticate user and merge guest cart into the database."""
    if request.is_json:
        data = request.get_json()
    else:
        data = request.form

    email = data.get("email")
    password = data.get("password")

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return render_template('login.html', error='Invalid credentials', email=email), 401

    session['user_id'] = user.id

    # Merge guest cart with user cart
    session_id = session.get('session_id')
    guest_cart = Cart.query.filter_by(session_id=session_id).all()

    for item in guest_cart:
        existing_item = Cart.query.filter_by(user_id=user.id, product_id=item.product_id).first()
        if existing_item:
            existing_item.quantity += item.quantity
        else:
            item.user_id = user.id
            item.session_id = None  # Remove session ID

    db.session.commit()  # Commit after processing all items

    response = redirect(url_for('home'))
    response.set_cookie('guest_cart', '', expires=0)  # Clear guest cart

    return response

# Logout Route
@user_bp.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

# Forgot Password Route
@user_bp.route('/forgot-password', methods=['GET'])
def forgot_password():
    """Display the forgot password page (placeholder)."""
    return render_template('forgot_password.html')
