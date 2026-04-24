from app import create_app, db, bcrypt
from app.models import User, Product

app = create_app()

def init_db():
    with app.app_context():
        db.create_all()
        
        # Check if admin user exists
        if not User.query.filter_by(email='admin@elevastore.com').first():
            hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
            admin = User(name='Admin', email='admin@elevastore.com', password_hash=hashed_password, is_admin=True)
            db.session.add(admin)
            
        # Check if test user exists
        if not User.query.filter_by(email='user@test.com').first():
            hashed_password = bcrypt.generate_password_hash('password123').decode('utf-8')
            user = User(name='Test User', email='user@test.com', password_hash=hashed_password, is_admin=False)
            db.session.add(user)
            
        # Add basic products if table is empty
        if not Product.query.first():
            products = [
                Product(name='Premium Wireless Headphones', description='High-fidelity sound, noise cancellation, and all-day comfort. Experience music like never before with 40-hour battery life.', price=299.99, stock=50, image_url='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=600&q=80'),
                Product(name='Smart Watch Series X', description='Track your fitness, receive notifications, and stay connected on the go. Features a vibrant AMOLED display and waterproof design.', price=199.50, stock=100, image_url='https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=600&q=80'),
                Product(name='Professional DSLR Camera', description='Capture stunning photos and 4K video. Includes a versatile 18-55mm lens perfect for any situation.', price=899.00, stock=15, image_url='https://images.unsplash.com/photo-1516035069371-29a1b244cc32?auto=format&fit=crop&w=600&q=80'),
                Product(name='Ergonomic Office Chair', description='Designed for all-day support with adjustable lumbar, armrests, and headrest. Stay comfortable and productive.', price=349.99, stock=25, image_url='https://images.unsplash.com/photo-1592078615290-07fdef52970b?auto=format&fit=crop&w=600&q=80'),
                Product(name='Minimalist Desk Lamp', description='Adjustable brightness and color temperature. Features an integrated wireless charging pad for your devices.', price=59.99, stock=200, image_url='https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&w=600&q=80'),
                Product(name='Mechanical Keyboard', description='Tactile switches, customizable RGB backlighting, and a premium aluminum frame. Enhance your typing experience.', price=129.99, stock=75, image_url='https://images.unsplash.com/photo-1595225476474-87563907a212?auto=format&fit=crop&w=600&q=80'),
            ]
            db.session.bulk_save_objects(products)
            
        db.session.commit()
        print("Database initialized successfully!")

if __name__ == '__main__':
    init_db()
