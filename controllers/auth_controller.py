"""Authentication Controller - handles login, register, logout"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from utils.helpers import get_language
from translations import get_translation

# This will be initialized in app factory
auth_bp = None
db = None
User = None

def init_auth_controller(app_instance, db_instance, user_model):
    """Initialize auth controller with app and models"""
    global auth_bp, db, User
    auth_bp = Blueprint('auth', __name__)
    db = db_instance
    User = user_model
    
    @auth_bp.route('/register', methods=['GET', 'POST'])
    def register():
        """User registration"""
        if current_user.is_authenticated:
            return redirect(url_for('home.index'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            email = request.form.get('email')
            password = request.form.get('password')
            confirm_password = request.form.get('confirm_password')
            role = request.form.get('role', 'end-user')
            
            lang = get_language()
            
            # Validation
            if not username or not email or not password:
                flash(get_translation('all_fields_required', lang), 'danger')
                return redirect(url_for('auth.register'))
            
            if password != confirm_password:
                flash(get_translation('passwords_not_match', lang), 'danger')
                return redirect(url_for('auth.register'))
            
            if User.query.filter_by(username=username).first():
                flash(get_translation('username_exists', lang), 'danger')
                return redirect(url_for('auth.register'))
            
            if User.query.filter_by(email=email).first():
                flash(get_translation('email_exists', lang), 'danger')
                return redirect(url_for('auth.register'))
            
            # Only allow admin role if current user is admin
            if role == 'admin' and (not current_user.is_authenticated or not current_user.is_admin()):
                role = 'end-user'
            
            # Create new user
            new_user = User(
                username=username,
                email=email,
                password_hash=generate_password_hash(password),
                role=role
            )
            db.session.add(new_user)
            db.session.commit()
            
            # Auto-login after registration
            login_user(new_user)
            flash(get_translation('registration_success', lang, username=new_user.username), 'success')
            return redirect(url_for('home.index'))
        
        return render_template('register.html')
    
    @auth_bp.route('/login', methods=['GET', 'POST'])
    def login():
        """User login"""
        if current_user.is_authenticated:
            return redirect(url_for('home.index'))
        
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            
            lang = get_language()
            
            if not username or not password:
                flash(get_translation('all_fields_required', lang), 'warning')
                return redirect(url_for('auth.login'))
            
            user = User.query.filter_by(username=username).first()
            
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                next_page = request.args.get('next')
                flash(get_translation('login_success', lang, username=user.username), 'success')
                return redirect(next_page) if next_page else redirect(url_for('home.index'))
            else:
                flash(get_translation('invalid_credentials', lang), 'danger')
                return redirect(url_for('auth.login'))
        
        return render_template('login.html')
    
    @auth_bp.route('/logout')
    @login_required
    def logout():
        """User logout"""
        logout_user()
        lang = get_language()
        flash(get_translation('logout_success', lang), 'info')
        return redirect(url_for('welcome.welcome'))
    
    app_instance.register_blueprint(auth_bp, url_prefix='/auth')



