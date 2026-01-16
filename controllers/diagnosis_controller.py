"""Diagnosis Controller - handles disease diagnosis"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from utils.helpers import get_language
from translations import get_translation

diagnosis_bp = Blueprint('diagnosis', __name__)

# These will be injected
Symptom = None
ExpertSystem = None

def init_diagnosis_controller(symptom_model, expert_system):
    """Initialize diagnosis controller with models and services"""
    global Symptom, ExpertSystem
    Symptom = symptom_model
    ExpertSystem = expert_system
    
    @diagnosis_bp.route('/diagnosis', methods=['GET', 'POST'])
    @login_required
    def diagnosis():
        """Diagnosis page"""
        if request.method == 'POST':
            selected_symptoms = request.form.getlist('symptoms')
            lang = get_language()
            
            if not selected_symptoms:
                flash(get_translation('please_select_symptom', lang), 'warning')
                return redirect(url_for('diagnosis.diagnosis'))
            
            # Get symptom IDs
            symptom_ids = [int(sid) for sid in selected_symptoms]
            symptoms = Symptom.query.filter(Symptom.id.in_(symptom_ids)).all()
            
            # Run expert system
            results = ExpertSystem.diagnose(symptom_ids)
            
            return render_template('results.html', 
                                 symptoms=symptoms, 
                                 results=results,
                                 selected_symptom_ids=symptom_ids)
        
        # GET request - show diagnosis form
        symptoms = Symptom.query.order_by(Symptom.name).all()
        return render_template('diagnosis.html', symptoms=symptoms)



