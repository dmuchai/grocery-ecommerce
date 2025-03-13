import os
import urllib.parse
from flask import Flask, render_template, session
from routes.product import product_bp
from routes.order import order_bp
from routes.user import user_bp
from routes.search import search_bp
from routes.cart import cart_bp
from routes.checkout import checkout_bp
from models import db
from flask_migrate import Migrate
from flask_session import Session
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Encode password to handle special characters
db_password = urllib.parse.quote_plus(os.getenv("DATABASE_PASSWORD", "password"))

# Database URI (This is to avoid hardcoding credentials)
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    f"mysql+pymysql://{os.getenv('DATABASE_USER', 'root')}:{db_password}@{os.getenv('DATABASE_HOST', 'localhost')}/grocery_db"
)

# Initialize Flask app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URL
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "your_secret_key")
app.config["SESSION_TYPE"] = "filesystem"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_FILE_DIR"] = "flask_session"

Session(app)

# Initialize database and migrations
db.init_app(app)
migrate = Migrate(app, db)

# Register Blueprints
app.register_blueprint(product_bp, url_prefix="/products")
app.register_blueprint(order_bp, url_prefix="/order")
app.register_blueprint(user_bp, url_prefix="/user")
app.register_blueprint(search_bp)
app.register_blueprint(cart_bp, url_prefix="/cart")
app.register_blueprint(checkout_bp, url_prefix="/checkout")

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/products-page')
def product_list_page():
    return render_template('products.html')

@app.route('/product/<int:product_id>')
def product_detail_page(product_id):
    return render_template('product.html')

if __name__ == "__main__":
    app.run(debug=True)
