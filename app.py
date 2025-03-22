import json
from flask import Flask, render_template, session, jsonify, url_for
from flask_migrate import Migrate
from flask_session import Session
from models import db
from config import Config
from flask_sqlalchemy import SQLAlchemy
from models import Product, Category

# Initialize Flask app
app = Flask(__name__)

# Apply configuration from Config class
app.config.from_object(Config)

#Configure Flask-Session
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

#Ensure sessions work with the database
app.config['SESSION_SQLALCHEMY'] = db

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

app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(order_bp, url_prefix="/order")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(search_bp)
app.register_blueprint(cart_bp, url_prefix="/cart")
app.register_blueprint(checkout_bp, url_prefix="/checkout")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/category/<category_name>')
def category_page(category_name):
    # Query products based on category
    products = Product.query.filter(Product.category.has(name=category_name)).all()    
    if not products:
        flash(f'No products found in {category_name} category.', 'warning')

    return render_template('category.html', products=products, category_name=category_name)

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
