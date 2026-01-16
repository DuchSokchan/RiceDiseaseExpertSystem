"""Home Controller - handles home page"""
from flask import Blueprint, render_template
from flask_login import login_required

home_bp = Blueprint('home', __name__)

# These will be injected
Disease = None

def init_home_controller(disease_model):
    """Initialize home controller with models"""
    global Disease
    Disease = disease_model
    
    @home_bp.route('/home')
    @login_required
    def index():
        """Home page - requires login"""
        diseases = Disease.query.all()
        return render_template('index.html', diseases=diseases)



