from models import db
from flask import current_app

def create_indexes():
    """Create database indexes for better performance."""
    with current_app.app_context():
        try:
            # Index for product searches
            db.engine.execute('''
                CREATE INDEX IF NOT EXISTS idx_product_name 
                ON product(name)
            ''')
            
            # Index for category filtering
            db.engine.execute('''
                CREATE INDEX IF NOT EXISTS idx_product_category 
                ON product(category_id)
            ''')
            
            # Index for user lookups
            db.engine.execute('''
                CREATE INDEX IF NOT EXISTS idx_user_email 
                ON user(email)
            ''')
            
            # Index for cart queries
            db.engine.execute('''
                CREATE INDEX IF NOT EXISTS idx_cart_user_session 
                ON cart(user_id, session_id)
            ''')
            
            # Index for order queries
            db.engine.execute('''
                CREATE INDEX IF NOT EXISTS idx_order_user_date 
                ON orders(user_id, created_at)
            ''')
            
            print("Database indexes created successfully")
            
        except Exception as e:
            print(f"Error creating indexes: {e}")

def optimize_queries():
    """Provide query optimization utilities."""
    
    @staticmethod
    def get_products_with_categories():
        """Optimized query to get products with their categories."""
        return db.session.query(Product).join(Category).all()
    
    @staticmethod
    def get_user_orders(user_id, limit=10):
        """Optimized query to get user orders with pagination."""
        return Order.query.filter_by(user_id=user_id)\
                         .order_by(Order.created_at.desc())\
                         .limit(limit)\
                         .all()
