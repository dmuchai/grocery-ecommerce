# Denncathy Fresh Basket - AI Coding Instructions

## Project Overview
Flask-based grocery e-commerce platform with PesaPal payment integration, deployed on Host Africa. Supports both guest shopping (session-based) and authenticated users with optional profile completion.

## Architecture & Key Components

### Blueprint-Based Routing
All routes organized as Flask Blueprints in `routes/`:
- `user_bp` (`/user`) - Registration, login, profile management
- `product_bp` (`/products`) - Product listing and details
- `cart_bp` (`/cart`) - Session-based cart operations
- `checkout_bp` (`/checkout`) - Multi-step checkout with delivery details
- `payment_bp` (`/payment`) - PesaPal API v3 integration
- `order_bp` (`/order`) - Order history and management
- `admin_bp` (`/admin`) - Admin dashboard with `@admin_required` decorator
- `search_bp` (`/search`) - Product search and suggestions

### Database Architecture (SQLAlchemy 2.0)
**Critical:** Use `db.session.get(Model, id)` instead of deprecated `Model.query.get(id)`.

Models in `models/`:
- `User` - Extended with optional profile fields (`first_name`, `last_name`, `phone`, `address`, `city`, etc.)
- `Product` - Linked to `Category` via relationship
- `Cart` - Session-backed for guests, DB-backed for authenticated users
- `Order` - Has `merchant_reference` and `pesapal_tracking_id` for payment tracking
- `OrderItem` - Cascade delete with orders

### Session Management Pattern
**Dual cart system:**
- Guest users: `session['cart']` dictionary keyed by product_id (string)
- Authenticated users: Database `Cart` model
- Session initialization in `@cart_bp.before_request` generates `session['session_id']` UUID for guests

Example from `routes/cart.py`:
```python
@cart_bp.before_request
def initialize_cart():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'cart' not in session:
        session['cart'] = {}
```

## Critical Workflows

### Local Development Setup
```bash
# Use automated script (recommended)
./setup_local.sh

# Or manual setup
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_db;"
flask db upgrade
python3 app.py
```

Default admin: `admin@denncathy.com` / `Admin123!`

### Production Deployment (Host Africa)
- Entry point: `passenger_wsgi.py` (not `wsgi.py`)
- Environment: Production config via `.env` (never commit credentials)
- Database: MySQL with PyMySQL connector (`mysql+pymysql://`)
- Required: `PESAPAL_IPN_ID` must be pre-registered (see `setup_ipn.py`)

### Testing
Tests split between root-level integration tests (`test_*.py`) and unit tests (`tests/`):
```bash
# Run specific test
python3 test_checkout.py

# Run all tests in tests/ directory
python -m pytest tests/
```

## Project-Specific Patterns

### URL Encoding for Product Images
**Known issue:** Cart URLs can become double-encoded. Always use raw URLs:
```python
# CORRECT in routes/cart.py
'image_url': product.image_url  # Not url_for() or encoded paths
```

### PesaPal Integration
Uses class-based API wrapper in `routes/payment.py`:
- `PesaPalAPI.get_auth_token()` - Must be called before any API operations
- `PesaPalAPI.submit_order_request()` - Creates payment, returns redirect URL
- IPN registration is **one-time setup** via `setup_ipn.py`, not per-transaction

**Environment variables required:**
```bash
PESAPAL_CONSUMER_KEY=xxx
PESAPAL_CONSUMER_SECRET=xxx
PESAPAL_IPN_ID=xxx  # Pre-registered
PESAPAL_BASE_URL=https://pay.pesapal.com/v3  # Production
```

### User Model Enhancements
User has optional profile completion tracking:
```python
user.has_complete_profile()  # Checks first_name, last_name, phone, address, city
user.update_profile_completion()  # Sets profile_completed boolean
user.get_full_name()  # Returns formatted name or username fallback
```

### Admin Authentication Pattern
Use decorators from `routes/admin.py`:
```python
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Only admin role users can access
```

### Error Handling
Global error handlers in `utils/error_handlers.py`:
- Renders custom templates from `templates/errors/`
- Always `db.session.rollback()` on 500 errors
- Logging configured with rotation in `setup_logging()`

### Configuration Management
`config.py` uses environment variables with **no defaults** for sensitive values:
```python
SECRET_KEY = os.getenv("SECRET_KEY")  # Raises ValueError if missing
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")  # Required
```

Password encoding for MySQL special characters:
```python
DB_PASSWORD_ENCODED = urllib.parse.quote_plus(DATABASE_PASSWORD)
```

## Common Gotchas

1. **SQLAlchemy 2.0 Migration**: All code updated to use `db.session.get()` - do not revert to `.query.get()`
2. **Session Configuration**: Flask-Session uses SQLAlchemy backend (`SESSION_TYPE = "sqlalchemy"`)
3. **Image URL Issues**: Never apply `url_for()` to product image URLs in cart operations
4. **Profile Optional Fields**: User model has nullable profile fields - always check before display
5. **Guest vs Authenticated Cart**: Always check `session.get('user_id')` to determine cart source

## Documentation References
- Local setup: `RUN_LOCALLY.md`
- Deployment: `DEPLOYMENT_GUIDE.md`
- PesaPal integration: `PESAPAL_SETUP.md`, `IPN_SETUP_GUIDE.md`
- Known issues: `ERROR_FIXES_SUMMARY.md`, `CREDENTIAL_ISSUES.md`

## When Making Changes
- Always update both session-based and DB-based cart logic if modifying cart behavior
- Test PesaPal integration in sandbox before production deployment
- Run database migrations before deploying model changes
- Check `test_production_deployment.py` for production readiness checks
