from flask import Blueprint, request, jsonify, session, render_template
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
    # Check for JSON request
    if request.content_type == 'application/json':
        data = request.get_json()
    else:
        data = request.form  # Handle form data

    if not data:
        return jsonify({"error": "Invalid request format"}), 400

    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "All fields are required"}), 400
    
    existing_user = User.query.filter((User.email == data['email'])).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409
    
    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    new_user = User(email=data['email'], password=hashed_password)
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify({'message': 'User registered successfully'}), 201

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
        return jsonify({"error": "Invalid credentials"}), 401

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

    response = jsonify({'message': 'Login successful'})
    response.set_cookie('guest_cart', '', expires=0)  # Clear guest cart

    return response

@user_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user and clear session."""
    session.pop('user_id', None)
    return jsonify({'message': 'Logged out successfully'}), 200
