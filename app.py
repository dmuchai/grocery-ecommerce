from flask import Flask, render_template, session
from flask_migrate import Migrate
from flask_session import Session
from models import db
from config import Config
from flask_sqlalchemy import SQLAlchemy

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

if __name__ == "__main__":
    app.run(debug=True)
