from models import db
from models.order_item import OrderItem

class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=True)  # Removed FK constraint temporarily
    customer_name = db.Column(db.String(128), nullable=False)
    guest_identifier = db.Column(db.String(36), nullable=True)
    email = db.Column(db.String(128), nullable=False)
    address = db.Column(db.String(256), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), default="Pending")  # Pending, Confirmed, Completed
    merchant_reference = db.Column(db.String(128), nullable=True, unique=True, index=True)  # Pesapal order reference
    pesapal_tracking_id = db.Column(db.String(128), nullable=True, index=True)  # Pesapal tracking ID
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Relationship to OrderItem
    items = db.relationship('OrderItem', back_populates='order', lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "customer_name": self.customer_name,
            "guest_identifier": self.guest_identifier,
            "email": self.email,
            "address": self.address,
            "total_price": self.total_price,
            "status": self.status,
            "merchant_reference": self.merchant_reference,
            "pesapal_tracking_id": self.pesapal_tracking_id,
            "created_at": self.created_at,
            "items": [item.to_dict() for item in self.items]
        }

