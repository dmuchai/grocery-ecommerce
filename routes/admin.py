from flask import Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash, generate_password_hash
import os
from models import db
from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order

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

# Product Management Routes
@admin_bp.route('/products')
@admin_required
def admin_products():
    """Admin products management page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '', type=str)
    category_filter = request.args.get('category', '', type=str)
    
    # Build query
    query = Product.query
    
    if search:
        query = query.filter(Product.name.contains(search))
    
    if category_filter:
        query = query.filter(Product.category_id == category_filter)
    
    # Paginate results
    products = query.paginate(
        page=page, per_page=10, error_out=False
    )
    
    # Get all categories for filter dropdown
    categories = Category.query.all()
    current_user = User.query.get(session['user_id'])
    
    return render_template('admin/products.html', 
                         products=products, 
                         categories=categories,
                         search=search,
                         category_filter=category_filter,
                         current_user=current_user)

@admin_bp.route('/products/add', methods=['GET', 'POST'])
@admin_required
def admin_add_product():
    """Add new product."""
    if request.method == 'POST':
        try:
            # Get form data
            name = request.form.get('name')
            description = request.form.get('description')
            price = float(request.form.get('price'))
            stock = int(request.form.get('stock'))
            category_id = int(request.form.get('category_id'))
            
            # Handle image upload
            image_url = None
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    # Create upload directory if it doesn't exist
                    upload_dir = os.path.join('static', 'images', 'products')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Save file
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    image_url = f"products/{filename}"
            
            # Create new product
            new_product = Product(
                name=name,
                description=description,
                price=price,
                stock=stock,
                category_id=category_id,
                image_url=image_url
            )
            
            db.session.add(new_product)
            db.session.commit()
            
            flash('Product added successfully!', 'success')
            return redirect(url_for('admin.admin_products'))
            
        except Exception as e:
            flash(f'Error adding product: {str(e)}', 'error')
            db.session.rollback()
    
    # Get categories for form
    categories = Category.query.all()
    current_user = User.query.get(session['user_id'])
    return render_template('admin/add_product.html', categories=categories, current_user=current_user)

@admin_bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_product(product_id):
    """Edit existing product."""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        try:
            # Update product data
            product.name = request.form.get('name')
            product.description = request.form.get('description')
            product.price = float(request.form.get('price'))
            product.stock = int(request.form.get('stock'))
            product.category_id = int(request.form.get('category_id'))
            
            # Handle image upload
            if 'image' in request.files:
                file = request.files['image']
                if file and file.filename != '':
                    filename = secure_filename(file.filename)
                    # Create upload directory if it doesn't exist
                    upload_dir = os.path.join('static', 'images', 'products')
                    os.makedirs(upload_dir, exist_ok=True)
                    
                    # Save file
                    file_path = os.path.join(upload_dir, filename)
                    file.save(file_path)
                    product.image_url = f"products/{filename}"
            
            db.session.commit()
            flash('Product updated successfully!', 'success')
            return redirect(url_for('admin.admin_products'))
            
        except Exception as e:
            flash(f'Error updating product: {str(e)}', 'error')
            db.session.rollback()
    
    # Get categories for form
    categories = Category.query.all()
    current_user = User.query.get(session['user_id'])
    return render_template('admin/edit_product.html', product=product, categories=categories, current_user=current_user)

@admin_bp.route('/products/delete/<int:product_id>', methods=['POST'])
@admin_required
def admin_delete_product(product_id):
    """Delete product."""
    try:
        product = Product.query.get_or_404(product_id)
        
        # Delete image file if exists
        if product.image_url:
            image_path = os.path.join('static', 'images', product.image_url)
            if os.path.exists(image_path):
                os.remove(image_path)
        
        db.session.delete(product)
        db.session.commit()
        
        flash('Product deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting product: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('admin.admin_products'))

@admin_bp.route('/products/bulk-update', methods=['POST'])
@admin_required
def admin_bulk_update_products():
    """Bulk update product stock."""
    try:
        updates = request.get_json()
        
        for update in updates:
            product = Product.query.get(update['id'])
            if product:
                product.stock = update['stock']
        
        db.session.commit()
        return jsonify({'success': True, 'message': 'Products updated successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'message': str(e)}), 400

# Categories Management
@admin_bp.route('/categories')
@admin_required
def admin_categories():
    """Admin categories management page."""
    categories = Category.query.all()
    current_user = User.query.get(session['user_id'])
    return render_template('admin/categories.html', categories=categories, current_user=current_user)

@admin_bp.route('/categories/add', methods=['POST'])
@admin_required
def admin_add_category():
    """Add new category."""
    try:
        name = request.form.get('name')
        
        # Check if category already exists
        existing = Category.query.filter_by(name=name).first()
        if existing:
            flash('Category already exists!', 'error')
            return redirect(url_for('admin.admin_categories'))
        
        new_category = Category(name=name)
        db.session.add(new_category)
        db.session.commit()
        
        flash('Category added successfully!', 'success')
    except Exception as e:
        flash(f'Error adding category: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('admin.admin_categories'))

@admin_bp.route('/categories/delete/<int:category_id>', methods=['POST'])
@admin_required
def admin_delete_category(category_id):
    """Delete category."""
    try:
        category = Category.query.get_or_404(category_id)
        
        # Check if category has products
        if category.products:
            flash('Cannot delete category with existing products!', 'error')
            return redirect(url_for('admin.admin_categories'))
        
        db.session.delete(category)
        db.session.commit()
        
        flash('Category deleted successfully!', 'success')
    except Exception as e:
        flash(f'Error deleting category: {str(e)}', 'error')
        db.session.rollback()
    
    return redirect(url_for('admin.admin_categories'))
