from flask import Blueprint, jsonify
from app.models import Order, OrderItem

mock_api = Blueprint('mock_api', __name__)

@mock_api.route('/latest-order/<int:user_id>', methods=['GET'])
def get_latest_order(user_id):
    # Fetch the latest order for this user
    order = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).first()
    
    if not order:
        return jsonify({"error": "No orders found for this user"}), 404
        
    # Get all product names from this order
    product_name = "N/A"
    if order.items:
        product_name = ", ".join([f"{item.quantity}x {item.product.name}" for item in order.items])
        
    return jsonify({
        "user_id": user_id,
        "user_name": order.customer.name,
        "order_id": order.id,
        "product": product_name,
        "status": order.status
    }), 200

@mock_api.route('/order-items/<int:order_id>', methods=['GET'])
def get_order_items(order_id):
    items = OrderItem.query.filter_by(order_id=order_id).all()
    
    if not items:
        return jsonify({"error": "No items found for this order"}), 404
        
    return jsonify([{
        "order_item_id": item.id,
        "product_id": item.product_id,
        "product_name": item.product.name,
        "quantity": item.quantity,
        "price_per_unit": item.product.price,
        "subtotal": round(item.quantity * item.product.price, 2),
        "user_name": item.order.customer.name
    } for item in items]), 200
