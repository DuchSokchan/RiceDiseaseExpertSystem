"""Admin Controller - handles admin operations"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from utils.decorators import admin_required
from utils.helpers import get_language
from translations import get_translation

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# These will be injected
Disease = None
Symptom = None
User = None
ExpertRule = None
db = None

def init_admin_controller(db_instance, disease_model, symptom_model, user_model, expert_rule_model):
    """Initialize admin controller with models"""
    global Disease, Symptom, User, ExpertRule, db
    Disease = disease_model
    Symptom = symptom_model
    User = user_model
    ExpertRule = expert_rule_model
    db = db_instance
    
    @admin_bp.route('/dashboard')
    @admin_required
    def dashboard():
        """Admin dashboard"""
        total_diseases = Disease.query.count()
        total_symptoms = Symptom.query.count()
        total_users = User.query.count()
        total_rules = ExpertRule.query.count()
        
        return render_template('admin/dashboard.html',
                             total_diseases=total_diseases,
                             total_symptoms=total_symptoms,
                             total_users=total_users,
                             total_rules=total_rules)
    
    @admin_bp.route('/diseases')
    @admin_required
    def diseases():
        """Admin: Manage diseases"""
        diseases_list = Disease.query.all()
        return render_template('admin/diseases.html', diseases=diseases_list)
    
    @admin_bp.route('/symptoms')
    @admin_required
    def symptoms():
        """Admin: Manage symptoms"""
        symptoms_list = Symptom.query.all()
        return render_template('admin/symptoms.html', symptoms=symptoms_list)
    
    @admin_bp.route('/users')
    @admin_required
    def users():
        """Admin: Manage users"""
        users_list = User.query.all()
        return render_template('admin/users/users.html', users=users_list)
    
    @admin_bp.route('/disease/add', methods=['GET', 'POST'])
    @admin_required
    def add_disease():
        """Admin: Add new disease"""
        lang = get_language()
        
        if request.method == 'POST':
            name = request.form.get('name')
            description = request.form.get('description')
            treatment = request.form.get('treatment')
            
            if not name or not description or not treatment:
                flash(get_translation('all_fields_required', lang), 'danger')
                return redirect(url_for('admin.add_disease'))
            
            if Disease.query.filter_by(name=name).first():
                flash(get_translation('disease_exists', lang), 'danger')
                return redirect(url_for('admin.add_disease'))
            
            disease = Disease(name=name, description=description, treatment=treatment)
            db.session.add(disease)
            db.session.commit()
            
            flash(get_translation('disease_added', lang), 'success')
            return redirect(url_for('admin.diseases'))
        
        symptoms = Symptom.query.all()
        return render_template('admin/add_disease.html', symptoms=symptoms)
    
    @admin_bp.route('/disease/<int:disease_id>/delete', methods=['POST'])
    @admin_required
    def delete_disease(disease_id):
        """Admin: Delete disease"""
        lang = get_language()
        disease = Disease.query.get_or_404(disease_id)
        db.session.delete(disease)
        db.session.commit()
        flash(get_translation('disease_deleted', lang), 'success')
        return redirect(url_for('admin.diseases'))
    
    @admin_bp.route('/symptom/add', methods=['GET', 'POST'])
    @admin_required
    def add_symptom():
        """Admin: Add new symptom"""
        lang = get_language()
        
        if request.method == 'POST':
            name = request.form.get('name')
            
            if not name:
                flash(get_translation('symptom_name_required', lang), 'danger')
                return redirect(url_for('admin.add_symptom'))
            
            if Symptom.query.filter_by(name=name).first():
                flash(get_translation('symptom_exists', lang), 'danger')
                return redirect(url_for('admin.add_symptom'))
            
            symptom = Symptom(name=name)
            db.session.add(symptom)
            db.session.commit()
            
            flash(get_translation('symptom_added', lang), 'success')
            return redirect(url_for('admin.symptoms'))
        
        return render_template('admin/add_symptom.html')
    
    @admin_bp.route('/symptom/<int:symptom_id>/delete', methods=['POST'])
    @admin_required
    def delete_symptom(symptom_id):
        """Admin: Delete symptom"""
        lang = get_language()
        symptom = Symptom.query.get_or_404(symptom_id)
        db.session.delete(symptom)
        db.session.commit()
        flash(get_translation('symptom_deleted', lang), 'success')
        return redirect(url_for('admin.symptoms'))



