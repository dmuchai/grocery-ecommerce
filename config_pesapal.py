# PesaPal Configuration Settings
# Add these to your config.py or environment variables
import os
from dotenv import load_dotenv
# Load environment variables from .env file
load_dotenv()
PESAPAL_CONFIG = {
    # Test/Sandbox credentials (replace with live credentials for production)
    'consumer_key': os.getenv('PESAPAL_CONSUMER_KEY'),
    'consumer_secret': os.getenv('PESAPAL_CONSUMER_SECRET'),
    
    # IPN ID (Register once using setup_ipn.py script)
    'ipn_id': os.getenv('PESAPAL_IPN_ID'),  # Get this from running setup_ipn.py
    
    # PesaPal URLs - PRODUCTION (your credentials are production!)
    'base_url': 'https://pay.pesapal.com/v3',  # Production URL
    # Sandbox URL: 'https://cybqa.pesapal.com/pesapalv3'
    
    'auth_url': '/api/Auth/RequestToken',
    'register_ipn_url': '/api/URLSetup/RegisterIPN',
    'submit_order_url': '/api/Transactions/SubmitOrderRequest',
    'transaction_status_url': '/api/Transactions/GetTransactionStatus',
    
    # Your website URLs
    'callback_url': 'https://denncathy.co.ke/payment/callback',
    'notification_url': 'https://denncathy.co.ke/payment/ipn',
    'cancellation_url': 'https://denncathy.co.ke/payment/cancelled'
}

# Add to your main config
class Config:
    # ... your existing config ...
    PESAPAL_CONSUMER_KEY = os.environ.get('PESAPAL_CONSUMER_KEY') or PESAPAL_CONFIG['consumer_key']
    PESAPAL_CONSUMER_SECRET = os.environ.get('PESAPAL_CONSUMER_SECRET') or PESAPAL_CONFIG['consumer_secret']
    PESAPAL_BASE_URL = PESAPAL_CONFIG['base_url']
