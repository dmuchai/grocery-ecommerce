import unittest
import tempfile
import os
from app import app
from models import db
from config import Config

class TestConfig(Config):
    """Configuration for testing."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    SECRET_KEY = 'testing-secret-key'

class BaseTestCase(unittest.TestCase):
    """Base test case for the grocery ecommerce application."""
    
    def setUp(self):
        """Set up test fixtures."""
        app.config.from_object(TestConfig)
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        db.create_all()
    
    def tearDown(self):
        """Tear down test fixtures."""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()
    
    def create_user(self, username='testuser', email='test@example.com', password='TestPass123'):
        """Helper method to create a test user."""
        from models.user import User
        from werkzeug.security import generate_password_hash
        
        user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()
        return user
    
    def create_product(self, name='Test Product', price=10.99, stock=100):
        """Helper method to create a test product."""
        from models.product import Product
        from models.category import Category
        
        # Create a test category first
        category = Category(name='Test Category')
        db.session.add(category)
        db.session.commit()
        
        product = Product(
            name=name,
            price=price,
            stock=stock,
            category_id=category.id
        )
        db.session.add(product)
        db.session.commit()
        return product
