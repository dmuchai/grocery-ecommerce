from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Define models inside a function to avoid circular imports
from models.user import User
from models.product import Product
from models.category import Category
from models.order import Order
from models.order_item import OrderItem
from models.cart import Cart
