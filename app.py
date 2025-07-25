import json
from flask import Flask, render_template, session, jsonify, redirect, url_for, flash
from flask_migrate import Migrate
from flask_session import Session
from models import db, User, Product, Category, Cart
from config import Config

# Initialize Flask app
app = Flask(__name__)

# Apply configuration from Config class
app.config.from_object(Config)

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Configure Flask-Session
app.config['SESSION_SQLALCHEMY'] = db
Session(app)

# Create the sessions table (run only once)
with app.app_context():
    db.create_all()

# Register Blueprints
from routes.product import product_bp
from routes.order import order_bp
from routes.user import user_bp
from routes.search import search_bp
from routes.cart import cart_bp
from routes.checkout import checkout_bp
from routes.admin import admin_bp

app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(order_bp, url_prefix="/order")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(search_bp, url_prefix="/search")
app.register_blueprint(cart_bp, url_prefix="/cart")
app.register_blueprint(checkout_bp, url_prefix="/checkout")
app.register_blueprint(admin_bp, url_prefix="/admin")

@app.route("/")
def home():
    user_email = None
    if 'user_id' in session:
        from models.user import User
        user = User.query.get(session['user_id'])
        if user:
            user_email = user.email
    return render_template("index.html", is_logged_in=bool(user_email), user_email=user_email)

@app.route('/category/<category_name>')
def category_page(category_name):
    # Map URL-friendly names to database names
    category_mapping = {
        'eggs-and-dairy': 'Eggs and Dairy',
        'vegetables': 'Vegetables',
        'fruits': 'Fruits'
    }
    
    # Get the actual category name for database lookup
    actual_category_name = category_mapping.get(category_name.lower(), category_name.title())
    
    # Query products based on category
    products = Product.query.filter(Product.category.has(name=actual_category_name)).all()    
    if not products:
        flash(f'No products found in {actual_category_name} category.', 'warning')

    return render_template('category.html', products=products, category_name=actual_category_name)

@app.route('/category/<category>/products')
def get_category_products(category):
    products = Product.query.filter_by(category=category).all()
    return jsonify([{
        "id": p.id,
        "name": p.name,
        "price": p.price,
        "image_url": p.image_url
    } for p in products])

def get_cart_from_session_or_db(user_id=None):
    """Fetch the cart from session (guest users) or database (logged-in users)."""
    if user_id:
        # Fetch cart from database for logged-in users
        cart = Cart.query.filter_by(user_id=user_id).first()
        return cart.items if cart else []
    else:
        # Fetch cart from session for guest users
        return session.get("cart", [])

@app.route('/cart-data')
def get_cart_data():
    cart = get_cart_from_session_or_db()
    for item in cart.values():
        item["image_url"] = url_for('static', filename=f'images/{item["image_url"]}', _external=True)
    return jsonify({"items": list(cart.values())})

@app.context_processor
def inject_user():
    user_id = session.get('user_id')
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            return {
                'is_logged_in': True,
                'user_email': user.email,
                'username': user.username  # <-- added
            }
    return {
        'is_logged_in': False,
        'user_email': None,
        'username': None
    }

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.context_processor
def inject_cart_count():
    """
    Make `cart_count` available in every template,
    based on the `session['cart']` quantities.
    """
    cart = session.get('cart', {})  # e.g. { "1": { "quantity": 2 }, ... }
    total = sum(item['quantity'] for item in cart.values())
    return dict(cart_count=total)

if __name__ == '__main__':
    with app.app_context():
        try:
            db.create_all()
            print("✓ Database tables created successfully")
            
            # Create default admin user if none exists
            from models.user import User
            from werkzeug.security import generate_password_hash
            
            admin_exists = User.query.filter_by(role='admin').first()
            if not admin_exists:
                try:
                    admin = User(
                        username='admin',
                        email='admin@denncathy.com',
                        password=generate_password_hash('Admin123!'),
                        role='admin',
                        is_active=True
                    )
                    db.session.add(admin)
                    db.session.commit()
                    print("✓ Default admin user created")
                    print("  📧 Email: admin@denncathy.com")
                    print("  🔑 Password: Admin123!")
                except Exception as e:
                    print(f"⚠️ Could not create admin user: {e}")
            else:
                print("✓ Admin user already exists")
                
        except Exception as e:
            print(f"Database setup error: {e}")
    
    print("Starting Grocery Ecommerce App...")
    print("Access the app at: http://127.0.0.1:5000")
    print("Access admin panel at: http://127.0.0.1:5000/admin/login")
    app.run(debug=True, host='0.0.0.0', port=5000)
