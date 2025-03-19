from models import db

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False, unique=True)

    # Relationship with Product model
    products = db.relationship('Product', backref='category', lazy=True)
