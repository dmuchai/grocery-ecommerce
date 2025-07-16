from models import db

class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='customer', nullable=False)  # customer, admin, seller
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def to_dict(self):
        return {
            "id": self.id, 
            "username": self.username, 
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }

    def is_admin(self):
        """Check if user has admin privileges"""
        return self.role in ['admin', 'seller']
    
    def is_seller(self):
        """Check if user is a seller"""
        return self.role == 'seller'
    
    def is_customer(self):
        """Check if user is a customer"""
        return self.role == 'customer'

    def __repr__(self):
        return f'<User {self.username}>'
