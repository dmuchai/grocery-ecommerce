from flask import Blueprint, request, jsonify, render_template
from models import db
from models.product import Product

# Products Blueprint
product_bp = Blueprint('product', __name__, url_prefix='/products')

# GET all products
@product_bp.route('/', methods=['GET'])
def get_all_products():
    products_data = Product.query.all()
    products_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": float(product.price),
                "image_url": f"/static/images/{product.image_url}"
            } for product in products_data
    ]           
    return render_template('products.html', products=products_list)

# GET a single product by ID
@product_bp.route('/<int:product_id>', methods=['GET'])
def get_product_by_id(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": float(product.price),
            "image_url": f"/static/images/{product.image_url}" if not product.image_url.startswith("/static/") else product.image_url,
            "in_stock": product.stock > 0
    }
    
    return render_template('product_detail.html', product=product_data)

# POST a new product
@product_bp.route('/', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or not all(key in data for key in ['name', 'description', 'price', 'stock']):
        return jsonify({'error': 'Missing required fields'}), 400

    new_product = Product(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            image_url=data.get('image_url')
    )
    db.session.add(new_product)
    db.session.commit()
    return jsonify({'message': 'Product added successfully', 'product': new_product.to_dict()}), 201

# PUT/Update an existing product
@product_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.stock = data.get('stock', product.stock)
    product.image_url = data.get('image_url', product.image_url)

    db.session.commit()
    return jsonify({'message': 'Product updated successfully', 'product': product.to_dict()}), 200

# DELETE a product
@product_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404

    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted successfully'}), 200
