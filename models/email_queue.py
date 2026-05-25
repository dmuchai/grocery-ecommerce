from . import db
from datetime import datetime

class EmailQueue(db.Model):
    __tablename__ = 'email_queue'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    email_type = db.Column(db.String(50), nullable=False)  # 'confirmation', 'admin_alert', 'payment_received'
    recipient = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(20), default='pending')  # 'pending', 'processing', 'sent', 'failed'
    attempts = db.Column(db.Integer, default=0)
    last_error = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    sent_at = db.Column(db.DateTime)

    # Relationships
    order = db.relationship('Order', backref='email_jobs')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'email_type': self.email_type,
            'recipient': self.recipient,
            'status': self.status,
            'attempts': self.attempts,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
