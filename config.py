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

    # Flask-Session Config (SQLAlchemy)
    SESSION_TYPE = "sqlalchemy"
    SESSION_SQLALCHEMY_TABLE = 'sessions'
    SESSION_PERMANENT = False
