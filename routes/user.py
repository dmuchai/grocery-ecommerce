from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from models import db, Cart
from models.user import User
from werkzeug.security import generate_password_hash, check_password_hash
import re

# Users Blueprint
user_bp = Blueprint('user', __name__)

def validate_password(password):
    """Validate password strength."""
    if len(password) < 8:
        return "Password must be at least 8 characters long."
    if not re.search(r"[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search(r"[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search(r"\d", password):
        return "Password must contain at least one number."
    return None

def validate_email(email):
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

# Serve the Register Page
@user_bp.route('/register', methods=['GET'])
def show_register():
    """Display the register page."""
    return render_template('register.html')

# Register a New User
@user_bp.route('/register', methods=['POST'])
def register():
    data = request.form

    # Required fields
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', '')

    # Optional profile fields
    first_name = data.get('first_name', '').strip() or None
    last_name = data.get('last_name', '').strip() or None
    phone = data.get('phone', '').strip() or None
    address = data.get('address', '').strip() or None
    city = data.get('city', '').strip() or None
    state = data.get('state', '').strip() or None
    postal_code = data.get('postal_code', '').strip() or None
    country = data.get('country', '').strip() or None

    # Validate required fields
    if not all([username, email, password]):
        return render_template(
            'register.html',
            error="All required fields must be filled.",
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country
        ), 400

    # Validate email format
    if not validate_email(email):
        return render_template(
            'register.html', 
            error="Invalid email format.",
            username=username,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country
        ), 400

    # Validate password strength
    password_error = validate_password(password)
    if password_error:
        return render_template(
            'register.html', 
            error=password_error,
            username=username, 
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country
        ), 400

    # Check if user already exists
    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        # Redirect to login page with flash message
        flash("An account with this email already exists. Please log in.", "warning")
        return redirect(url_for('user.show_login'))

    # Check if username already exists
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return render_template(
            'register.html',
            error="This username is already taken. Please choose another.",
            email=email,
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            address=address,
            city=city,
            state=state,
            postal_code=postal_code,
            country=country
        ), 400

    # Create and save user with all provided information
    hashed_password = generate_password_hash(password)
    new_user = User(
        username=username, 
        email=email, 
        password=hashed_password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        address=address,
        city=city,
        state=state,
        postal_code=postal_code,
        country=country
    )
    
    # Update profile completion status
    new_user.update_profile_completion()
    
    db.session.add(new_user)
    db.session.commit()

    # Log in the user
    session['user_id'] = new_user.id

    # Welcome message based on profile completion
    if new_user.profile_completed:
        flash(f"Welcome to Denncathy Fresh Basket, {new_user.get_full_name()}! Your profile is complete.", "success")
    else:
        flash(f"Welcome to Denncathy Fresh Basket, {username}! You can complete your profile anytime for faster checkout.", "success")

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

# Profile Routes
@user_bp.route('/profile', methods=['GET'])
def profile():
    """Display user profile page"""
    if 'user_id' not in session:
        flash('Please login to view your profile', 'error')
        return redirect(url_for('user.show_login'))
    
    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('user.show_login'))
    
    return render_template('profile.html', user=user)

@user_bp.route('/profile/update', methods=['POST'])
def update_profile():
    """Update user profile information"""
    if 'user_id' not in session:
        flash('Please login to update your profile', 'error')
        return redirect(url_for('user.show_login'))
    
    user = db.session.get(User, session['user_id'])
    if not user:
        flash('User not found', 'error')
        return redirect(url_for('user.show_login'))
    
    try:
        # Update user information with validation
        email = request.form.get('email', '').strip()
        
        # Validate email
        if not validate_email(email):
            flash('Please enter a valid email address', 'error')
            return redirect(url_for('user.profile'))
        
        # Check if email is already taken by another user
        existing_user = User.query.filter(User.email == email, User.id != user.id).first()
        if existing_user:
            flash('Email address is already in use by another account', 'error')
            return redirect(url_for('user.profile'))
        
        # Update profile fields
        user.email = email
        user.first_name = request.form.get('first_name', '').strip() or None
        user.last_name = request.form.get('last_name', '').strip() or None
        user.phone = request.form.get('phone', '').strip() or None
        user.address = request.form.get('address', '').strip() or None
        user.city = request.form.get('city', '').strip() or None
        user.state = request.form.get('state', '').strip() or None
        user.postal_code = request.form.get('postal_code', '').strip() or None
        user.country = request.form.get('country', 'Kenya')
        
        # Update profile completion status
        user.update_profile_completion()
        
        db.session.commit()
        
        flash('Profile updated successfully!', 'success')
        if user.profile_completed:
            flash('Your profile is now complete! Enjoy faster checkout.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash('An error occurred while updating your profile. Please try again.', 'error')
        print(f"Profile update error: {e}")
    
    return redirect(url_for('user.profile'))
