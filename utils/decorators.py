"""Decorators for authentication and authorization"""
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import login_required, current_user

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin():
            from utils.helpers import get_language
            from translations import get_translation
            lang = get_language()
            flash(get_translation('access_denied', lang), 'danger')
            return redirect(url_for('home.index'))
        return f(*args, **kwargs)
    return decorated_function

