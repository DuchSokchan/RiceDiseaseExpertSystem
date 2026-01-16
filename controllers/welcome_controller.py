"""Welcome Controller - handles welcome page and language switching"""
from flask import Blueprint, render_template, request, redirect, url_for, session
from flask_login import current_user
from utils.helpers import get_language, set_language

welcome_bp = Blueprint('welcome', __name__)

@welcome_bp.route('/')
def welcome():
    """Welcome page - public, redirects to login/register"""
    if current_user.is_authenticated:
        return redirect(url_for('home.index'))
    return render_template('welcome.html')

@welcome_bp.route('/set_language/<lang>')
def set_language_route(lang):
    """Set language preference"""
    set_language(lang)
    return redirect(request.referrer or url_for('welcome.welcome'))



