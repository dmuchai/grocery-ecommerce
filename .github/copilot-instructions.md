# Denncathy Fresh Basket - AI Coding Instructions

## Project Overview
This is a Flask-based grocery e-commerce platform integrated with PesaPal payments, deployed on Host Africa. It supports both guest shopping (session-based cart) and authenticated users with optional profile completion.

## Architecture & Key Components

### Blueprint-Based Routing
Routes are organized into Flask Blueprints in the `routes/` directory. Key blueprints include:
- `user_bp` (`/user`): User authentication and profile.
- `product_bp` (`/products`): Product listings.
- `cart_bp` (`/cart`): Session and DB-backed cart operations.
- `checkout_bp` (`/checkout`): Multi-step checkout.
- `payment_bp` (`/payment`): PesaPal API integration.
- `admin_bp` (`/admin`): Admin dashboard, protected by `@admin_required`.

### Database Architecture (SQLAlchemy 2.0)
Models are defined in `models/`. **Critical:** Always use `db.session.get(Model, id)` for fetching objects by primary key, *not* `Model.query.get(id)`.
- `User`: Extended with nullable profile fields and `profile_completed` flag.
- `Product`: Linked to `Category`.
- `Cart`: Dual system (session-backed for guests, DB-backed for authenticated users).
- `Order`: Includes `merchant_reference` and `pesapal_tracking_id`.
- `OrderItem`: Configured for cascade deletion with `Order`.

### Session Management Pattern (Dual Cart System)
- **Guest users:** Cart data stored in `session['cart']` as a dictionary, keyed by product ID.
- **Authenticated users:** Cart data stored in the database via the `Cart` model.
- A `session['session_id']` (UUID) is generated in `@cart_bp.before_request` for guest sessions.
```grocery-ecommerce/routes/cart.py#L9-13
@cart_bp.before_request
def initialize_cart():
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    if 'cart' not in session:
        session['cart'] = {}
```

## Critical Workflows

### Local Development Setup
Use the provided script or manual steps:
```bash
./setup_local.sh
# OR
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
mysql -u root -p -e "CREATE DATABASE IF NOT EXISTS grocery_db;"
flask db upgrade
python3 app.py
```
Default admin credentials: `admin@denncathy.com` / `Admin123!`

### Testing
- Run specific integration tests: `python3 test_checkout.py` (e.g., `test_*.py` at root).
- Run all unit tests: `python -m pytest tests/` (tests within the `tests/` directory).

## Project-Specific Patterns

### URL Handling for Product Images
Avoid `url_for()` for product image URLs within cart contexts to prevent double-encoding issues. Always use the raw `product.image_url`.
```grocery-ecommerce/routes/cart.py#L123-124
# CORRECT:
'image_url': product.image_url
```

### PesaPal Integration
The `PesaPalAPI` class in `routes/payment.py` handles PesaPal interactions.
- `PesaPalAPI.get_auth_token()`: Must be called before other API operations.
- `PesaPalAPI.submit_order_request()`: Initiates payment and returns a redirect URL.
- IPN registration (`PESAPAL_IPN_ID`) is a one-time setup via `setup_ipn.py`.
Required environment variables: `PESAPAL_CONSUMER_KEY`, `PESAPAL_CONSUMER_SECRET`, `PESAPAL_IPN_ID`, `PESAPAL_BASE_URL`.

### Admin Authentication
Use the `@admin_required` decorator from `routes/admin.py` to protect admin-only routes.
```grocery-ecommerce/routes/admin.py#L18-21
@admin_bp.route('/dashboard')
@admin_required
def dashboard():
    # Admin-only logic
```

### Configuration Management
`config.py` uses `os.getenv()` without defaults for sensitive settings, raising `ValueError` if missing.
MySQL passwords with special characters must be URL-encoded using `urllib.parse.quote_plus()`.
```grocery-ecommerce/config.py#L10-11
SECRET_KEY = os.getenv("SECRET_KEY") # Will raise ValueError if missing
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
```

## Common Gotchas
1.  **SQLAlchemy 2.0 Migration**: Use `db.session.get()` for fetching by ID.
2.  **Image URL Issues**: Never apply `url_for()` to `product.image_url` in cart operations.
3.  **Guest vs. Authenticated Cart**: Always check `session.get('user_id')` to determine the active cart mechanism.
4.  **Profile Fields**: User profile fields are nullable; check for `None` before displaying.

## Documentation References
- Local setup: `RUN_LOCALLY.md`
- Deployment: `DEPLOYMENT_GUIDE.md`
- PesaPal: `PESAPAL_SETUP.md`, `IPN_SETUP_GUIDE.md`
- Known issues: `ERROR_FIXES_SUMMARY.md`, `CREDENTIAL_ISSUES.md`

## When Making Changes
- Any modifications to cart behavior must address both session-based (guest) and DB-based (authenticated) logic.
- Run `flask db upgrade` after model changes.
- Verify PesaPal integration in a sandbox environment before production.