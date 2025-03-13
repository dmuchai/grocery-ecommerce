from flask import Blueprint, request, jsonify
from models.product import Product
from models import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    query = request.args.get('q')
    if not query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        results = db.session.query(Product).filter(Product.name.ilike(f"%{query}%")).all()
        product = [p.to_dict() for p in results]
        return jsonify(product)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
