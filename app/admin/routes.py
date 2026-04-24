from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import Product, Order
from app import db
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    products = Product.query.all()
    orders = Order.query.all()
    return render_template('admin/dashboard.html', products=products, orders=orders)

@admin.route('/product/add', methods=['POST'])
@login_required
@admin_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        price = float(request.form.get('price'))
        stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url') or 'default.jpg'
        
        product = Product(name=name, description=description, price=price, stock=stock, image_url=image_url)
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/product/edit/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.description = request.form.get('description')
        product.price = float(request.form.get('price'))
        product.stock = int(request.form.get('stock'))
        image_url = request.form.get('image_url')
        if image_url:
            product.image_url = image_url
            
        db.session.commit()
        flash('Product updated successfully', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/product/delete/<int:product_id>', methods=['POST'])
@login_required
@admin_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted', 'success')
    return redirect(url_for('admin.dashboard'))

@admin.route('/order/update/<int:order_id>', methods=['POST'])
@login_required
@admin_required
def update_order(order_id):
    order = Order.query.get_or_404(order_id)
    status = request.form.get('status')
    if status:
        order.status = status
        db.session.commit()
        flash(f'Order {order.id} status updated to {status}', 'success')
    return redirect(url_for('admin.dashboard'))
