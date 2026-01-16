"""Disease Controller - handles disease listing and details"""
from flask import Blueprint, render_template
from flask_login import login_required

disease_bp = Blueprint('disease', __name__)

# These will be injected
Disease = None

def init_disease_controller(disease_model):
    """Initialize disease controller with models"""
    global Disease
    Disease = disease_model
    
    @disease_bp.route('/disease/<int:disease_id>')
    @login_required
    def disease_detail(disease_id):
        """Disease detail page - requires login"""
        disease = Disease.query.get_or_404(disease_id)
        return render_template('disease_detail.html', disease=disease)
    
    @disease_bp.route('/diseases')
    @login_required
    def diseases():
        """List all diseases - requires login"""
        diseases_list = Disease.query.all()
        return render_template('diseases.html', diseases=diseases_list)



