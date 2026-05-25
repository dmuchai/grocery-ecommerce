from flask import Blueprint, render_template, session
from models import db, User # Import necessary modules for context processor

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    "\"\"\"Renders the home page.\"\"\"
    # This route is typically handled by app.py for root, but can be defined here if needed
    # For now, assuming app.py handles the root and passes user data
    # We can refine this later if app.py is refactored to use this blueprint for home
    return render_template("index.html")

@main_bp.route('/about')
def about():
    "\"\"\"Renders the about us page.\"\"\"
    return render_template('about.html')

@main_bp.route('/contact')
def contact():
    "\"\"\"Renders the contact us page.\"\"\"
    return render_template('contact.html')

@main_bp.route('/return-policy')
def return_policy():
    "\"\"\"Renders the return policy page.\"\"\"
    # Assuming you have a 'return_policy.html' template
    return render_template('return_policy.html')

# Other static pages can be added here

@main_bp.context_processor
def inject_common_data():
    """Injects data common to multiple templates."""
    user_id = session.get('user_id')
    user_email = None
    username = None
    if user_id:
        user = db.session.get(User, user_id)
        if user:
            user_email = user.email
            username = user.username

    # Cart count injection moved to app.py's context processor
    # to avoid duplication and ensure consistency.

    return {
        'is_logged_in': bool(user_id and user),
        'user_email': user_email,
        'username': username,
    }
