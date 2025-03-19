from models import db

class Product(db.Model):
    """Product Model representing an item in the grocery e-commerce store."""
    __tablename__ = "product"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, nullable=False)
    image_url = db.Column(db.String(255), nullable=True)
    
    # Foreign Key linking to category
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

    def to_dict(self):
        """Converts Product object to dictionary format."""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": float(self.price),
            "stock": self.stock,
            "image_url": f"/static/images/{self.image_url}" if self.image_url else "/static/images/default.jpg",
            "category_id": self.category_id,
            "category_name": self.category.name if self.category else "Unknown"
        }

    @staticmethod
    def get_related_products(product_id, limit=5):
        """
        Fetch related products based on category.

        - Excludes the current product.
        - Limits the number of related products returned.
        """
        product = Product.query.get(product_id)
        if not product or not product.category_id:
            return []

        return Product.query.filter(
            Product.category_id == product.category_id,
            Product.id != product.id
        ).limit(limit).all()
