import os
import urllib.parse
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Remove dangerous defaults - require environment variables
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is required")

    # Database Config
    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_USER = os.getenv("DATABASE_USER", "root")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "grocery_db")
    
    if not DATABASE_PASSWORD:
        raise ValueError("DATABASE_PASSWORD environment variable is required")

    # Encode password to handle special characters
    DB_PASSWORD_ENCODED = urllib.parse.quote_plus(DATABASE_PASSWORD)

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"mysql+pymysql://{DATABASE_USER}:{DB_PASSWORD_ENCODED}@{DATABASE_HOST}/{DATABASE_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLAlchemy Engine Options - Prevent "MySQL server has gone away"
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,      # Verify connections before using
        'pool_recycle': 280,         # Recycle connections before MySQL timeout (default 300s)
        'pool_size': 10,             # Maximum number of connections
        'max_overflow': 20           # Maximum overflow connections
    }

    # Flask-Session Config (SQLAlchemy)
    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_PERMANENT = False
    
    # Email Configuration (Flask-Mail)
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'noreply@denncathy.co.ke')
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@denncathy.co.ke')
    
    # PesaPal Config
    PESAPAL_BASE_URL = os.getenv('PESAPAL_BASE_URL', 'https://pay.pesapal.com/v3')
    PESAPAL_CONSUMER_KEY = os.getenv('PESAPAL_CONSUMER_KEY')
    PESAPAL_CONSUMER_SECRET = os.getenv('PESAPAL_CONSUMER_SECRET')
    PESAPAL_IPN_ID = os.getenv('PESAPAL_IPN_ID')
    PESAPAL_CALLBACK_URL = os.getenv('PESAPAL_CALLBACK_URL')
