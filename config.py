import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'super-secret-key-please-change-in-prod'
    
    # Render sometimes passes "postgres://" instead of "postgresql://" which SQLAlchemy requires.
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = database_url or 'sqlite:///' + os.path.join(basedir, 'ecommerce.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    