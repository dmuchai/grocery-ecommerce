from flask import Blueprint, request, jsonify, render_template
from models.product import Product
from models import db
from utils.image_urls import normalize_image_url

search_bp = Blueprint('search', __name__, url_prefix='/search')

@search_bp.route('/', methods=['GET'])
def search():
    query = request.args.get('q', '').strip()
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    if not query:
        return render_template("search.html", query=query, products=[])

    try:
        results = Product.query.filter(Product.name.ilike(f"%{query}%")).paginate(
                page=page, per_page=per_page, error_out=False)
        
        products = [{
            "id": p.id,
            "name": p.name,
            "description": p.description,
            "price": p.price,
            "image_url": normalize_image_url(p.image_url)
        } for p in results.items]

        # ✅ Proper indentation here
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest' or request.accept_mimetypes.best == 'application/json':
            return jsonify({
                "q": query,
                "products": products,
                "total": results.total,
                "pages": results.pages,
                "current_page": results.page
            })

        return render_template("search.html", query=query, products=products)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@search_bp.route("/suggest")
def suggest_products():
    query = request.args.get("q", "").strip()
    if not query:
        return jsonify([])

    results = Product.query.filter(Product.name.ilike(f"%{query}%")).limit(5).all()
    suggestions = [{
        "id": p.id,
        "name": p.name,
        "image_url": normalize_image_url(p.image_url)
    } for p in results]
    return jsonify(suggestions)
