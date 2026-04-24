from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models import Product, CartItem, Order, OrderItem
from flask_login import current_user, login_required
from app import db
import requests

main = Blueprint('main', __name__)

@main.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    search_query = request.args.get('q', '')
    
    # Simple search
    if search_query:
        products = Product.query.filter(Product.name.ilike(f'%{search_query}%')).paginate(page=page, per_page=6)
    else:
        products = Product.query.paginate(page=page, per_page=6)
        
    return render_template('main/index.html', products=products, search_query=search_query)

@main.route('/product/<int:product_id>')
def product(product_id):
    product = Product.query.get_or_404(product_id)
    return render_template('main/product.html', product=product)

@main.route('/cart/add/<int:product_id>', methods=['POST'])
@login_required
def add_to_cart(product_id):
    product = Product.query.get_or_404(product_id)
    quantity = int(request.form.get('quantity', 1))
    
    if product.stock < quantity:
        flash('Not enough stock available', 'danger')
        return redirect(url_for('main.product', product_id=product.id))
        
    cart_item = CartItem.query.filter_by(user_id=current_user.id, product_id=product_id).first()
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = CartItem(user_id=current_user.id, product_id=product_id, quantity=quantity)
        db.session.add(cart_item)
        
    db.session.commit()
    flash(f'Added {quantity} x {product.name} to cart', 'success')
    return redirect(request.referrer or url_for('main.index'))

@main.route('/cart')
@login_required
def cart():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    total = sum(item.product.price * item.quantity for item in cart_items)
    return render_template('main/cart.html', cart_items=cart_items, total=total)

@main.route('/cart/remove/<int:cart_item_id>', methods=['POST'])
@login_required
def remove_from_cart(cart_item_id):
    cart_item = CartItem.query.get_or_404(cart_item_id)
    if cart_item.user_id != current_user.id:
        return redirect(url_for('main.cart'))
        
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart', 'info')
    return redirect(url_for('main.cart'))

@main.route('/checkout', methods=['POST'])
@login_required
def checkout():
    cart_items = CartItem.query.filter_by(user_id=current_user.id).all()
    if not cart_items:
        flash('Your cart is empty', 'warning')
        return redirect(url_for('main.cart'))
        
    total_price = sum(item.product.price * item.quantity for item in cart_items)
    
    # Create order
    order = Order(user_id=current_user.id, total_price=total_price, status='Pending')
    db.session.add(order)
    db.session.flush() # get order id
    
    for cart_item in cart_items:
        # Update stock
        cart_item.product.stock -= cart_item.quantity
        # Add order item
        order_item = OrderItem(order_id=order.id, product_id=cart_item.product_id, quantity=cart_item.quantity)
        db.session.add(order_item)
        # Clear cart
        db.session.delete(cart_item)
        
    db.session.commit()
    flash('Order placed successfully!', 'success')
    return redirect(url_for('main.orders'))

@main.route('/orders')
@login_required
def orders():
    orders = Order.query.filter_by(user_id=current_user.id).order_by(Order.created_at.desc()).all()
    
    # External API tracking data for exactly the latest order using our own new endpoint
    tracking_data = None
    try:
        # Call the endpoint to get the status (Simulating external API requirement via localhost requests)
        # We need a full URL to do requests.get
        # For a more robust app we would use an absolute URL
        if orders:
            res = requests.get(request.host_url + f'latest-order/{current_user.id}')
            if res.status_code == 200:
                tracking_data = res.json()
    except Exception as e:
        print(f"Error fetching tracking data: {e}")

    return render_template('main/orders.html', orders=orders, tracking_data=tracking_data)
