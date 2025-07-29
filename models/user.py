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
    
    # Profile Information (nullable to maintain compatibility)
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    
    # Address Information (nullable for flexibility)
    address = db.Column(db.String(200), nullable=True)
    city = db.Column(db.String(50), nullable=True)
    state = db.Column(db.String(50), nullable=True)
    postal_code = db.Column(db.String(20), nullable=True)
    country = db.Column(db.String(50), nullable=True, default='Kenya')
    
    # Profile completion tracking
    profile_completed = db.Column(db.Boolean, default=False, nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    def get_full_name(self):
        """Get user's full name or username as fallback"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        elif self.first_name:
            return self.first_name
        else:
            return self.username
    
    def get_full_address(self):
        """Get formatted full address"""
        address_parts = []
        if self.address:
            address_parts.append(self.address)
        if self.city:
            address_parts.append(self.city)
        if self.state:
            address_parts.append(self.state)
        if self.postal_code:
            address_parts.append(self.postal_code)
        if self.country:
            address_parts.append(self.country)
        return ", ".join(address_parts)
    
    def has_complete_profile(self):
        """Check if user has completed their profile"""
        required_fields = [self.first_name, self.last_name, self.phone, self.address, self.city]
        return all(field for field in required_fields)
    
    def update_profile_completion(self):
        """Update profile completion status"""
        self.profile_completed = self.has_complete_profile()
        return self.profile_completed

    def to_dict(self):
        return {
            "id": self.id, 
            "username": self.username, 
            "email": self.email,
            "role": self.role,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "postal_code": self.postal_code,
            "country": self.country,
            "profile_completed": self.profile_completed,
            "full_name": self.get_full_name(),
            "full_address": self.get_full_address()
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
