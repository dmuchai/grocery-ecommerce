from flask import Blueprint, request, jsonify
from models import db
from models.order import Order
from models.cart import Cart

order_bp = Blueprint("order", __name__, url_prefix="/orders")

@order_bp.route("/place", methods=["POST"])
def place_order():
    data = request.get_json()
    user_id = data["user_id"]

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    total_price = sum(item.quantity * item.product.price for item in cart_items)

    new_order = Order(user_id=user_id, total_price=total_price)
    db.session.add(new_order)
    db.session.commit()

    # Clear cart after placing order
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify({"message": "Order placed successfully", "order": new_order.to_dict()}), 201
