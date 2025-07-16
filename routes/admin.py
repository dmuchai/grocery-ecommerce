from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from functools import wraps
from models import db
from models.user import User
from models.product import Product
from models.order import Order
from werkzeug.security import check_password_hash
import re

# Admin Blueprint
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    """Decorator to require admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access the admin area.', 'warning')
            return redirect(url_for('admin.login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin():
            flash('Access denied. Admin privileges required.', 'danger')
            return redirect(url_for('admin.login'))
        
        return f(*args, **kwargs)
    return decorated_function

def seller_required(f):
    """Decorator to require seller/admin authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this area.', 'warning')
            return redirect(url_for('admin.login'))
        
        user = User.query.get(session['user_id'])
        if not user or not user.is_admin():
            flash('Access denied. Seller privileges required.', 'danger')
            return redirect(url_for('admin.login'))
        
        return f(*args, **kwargs)
    return decorated_function

# Admin Login Page
@admin_bp.route('/login', methods=['GET'])
def login():
    """Display admin login page"""
    return render_template('admin/login.html')

# Admin Login Handler
@admin_bp.route('/login', methods=['POST'])
def login_post():
    """Handle admin login"""
    data = request.form
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        flash('Email and password are required.', 'danger')
        return render_template('admin/login.html', email=email)
    
    user = User.query.filter_by(email=email).first()
    
    if not user:
        flash('Invalid email or password.', 'danger')
        return render_template('admin/login.html', email=email)
    
    if not user.is_active:
        flash('Account is deactivated. Contact administrator.', 'danger')
        return render_template('admin/login.html', email=email)
    
    if not check_password_hash(user.password, password):
        flash('Invalid email or password.', 'danger')
        return render_template('admin/login.html', email=email)
    
    if not user.is_admin():
        flash('Access denied. Admin privileges required.', 'danger')
        return render_template('admin/login.html', email=email)
    
    # Login successful
    session['user_id'] = user.id
    session['user_role'] = user.role
    flash(f'Welcome back, {user.username}!', 'success')
    return redirect(url_for('admin.dashboard'))

# Admin Logout
@admin_bp.route('/logout')
def logout():
    """Handle admin logout"""
    session.pop('user_id', None)
    session.pop('user_role', None)
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('admin.login'))

# Admin Dashboard
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    """Admin dashboard with overview statistics"""
    # Get statistics
    total_products = Product.query.count()
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='Pending').count()
    total_customers = User.query.filter_by(role='customer').count()
    
    # Recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Low stock products (assuming stock < 10 is low)
    low_stock_products = Product.query.filter(Product.stock < 10).limit(5).all()
    
    stats = {
        'total_products': total_products,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'total_customers': total_customers
    }
    
    current_user = User.query.get(session['user_id'])
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_orders=recent_orders,
                         low_stock_products=low_stock_products,
                         current_user=current_user)

# Admin Profile
@admin_bp.route('/profile')
@admin_required
def profile():
    """Admin profile page"""
    current_user = User.query.get(session['user_id'])
    return render_template('admin/profile.html', current_user=current_user)

# Create Default Admin (Development utility)
@admin_bp.route('/create-default-admin', methods=['POST'])
def create_default_admin():
    """Create a default admin user (for development)"""
    from werkzeug.security import generate_password_hash
    
    # Check if admin already exists
    admin_exists = User.query.filter_by(role='admin').first()
    if admin_exists:
        return jsonify({'error': 'Admin user already exists'}), 400
    
    # Create default admin
    default_admin = User(
        username='admin',
        email='admin@denncathy.com',
        password=generate_password_hash('admin123'),
        role='admin',
        is_active=True
    )
    
    try:
        db.session.add(default_admin)
        db.session.commit()
        return jsonify({'message': 'Default admin created successfully. Email: admin@denncathy.com, Password: admin123'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to create admin: {str(e)}'}), 500
