from flask import Blueprint, request, jsonify
from models.product import Product
from models import db

search_bp = Blueprint('search', __name__)

@search_bp.route('/search', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not query:
        return jsonify({"error": "No search query provided"}), 400

    try:
        results = Product.query.filter(Product.name.ilike(f"%{query}%")).paginate(page=page, per_page=per_page, error_out=False)
        
        products = [{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "image_url": f"/static/images/{p.image_url}" if p.image_url else "/static/images/default.jpg"
        } for p in results.items]

        return jsonify({
            "products": products,
            "total": results.total,
            "pages": results.pages,
            "current_page": results.page
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500
