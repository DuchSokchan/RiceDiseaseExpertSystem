"""Application Factory - Creates Flask app with MVC structure"""
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
from translations import get_translation
from utils.helpers import get_language, translate_symptom

# Initialize extensions (will be initialized in create_app)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    """Application factory function"""
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'welcome.welcome'
    login_manager.login_message = 'Please log in or register to access this page.'
    login_manager.login_message_category = 'info'
    
    # Initialize models
    from models import create_models
    Disease, Symptom, DiseaseSymptom, ExpertRule, disease_symptom, User = create_models(db)
    
    # Initialize Flask-Login user loader
    @login_manager.user_loader
    def load_user(user_id):
        """Load user for Flask-Login"""
        return User.query.get(int(user_id))
    
    # Context processor for translations
    @app.context_processor
    def inject_language():
        """Make translation function available to all templates"""
        lang = get_language()
        return dict(
            t=lambda key, **kwargs: get_translation(key, lang, **kwargs),
            tsym=lambda name: translate_symptom(name, lang),
            current_lang=lang
        )
    
    # Initialize Expert System Service
    from services.expert_system_service import ExpertSystem
    expert_system = ExpertSystem(db, Disease, Symptom, DiseaseSymptom, ExpertRule)
    
    # Register blueprints (controllers)
    from controllers.welcome_controller import welcome_bp
    app.register_blueprint(welcome_bp)
    
    from controllers.home_controller import init_home_controller
    init_home_controller(Disease)
    from controllers.home_controller import home_bp
    app.register_blueprint(home_bp)
    
    from controllers.auth_controller import init_auth_controller
    init_auth_controller(app, db, User)
    
    from controllers.diagnosis_controller import init_diagnosis_controller
    init_diagnosis_controller(Symptom, expert_system)
    from controllers.diagnosis_controller import diagnosis_bp
    app.register_blueprint(diagnosis_bp)
    
    from controllers.disease_controller import init_disease_controller
    init_disease_controller(Disease)
    from controllers.disease_controller import disease_bp
    app.register_blueprint(disease_bp)
    
    from controllers.admin_controller import init_admin_controller
    init_admin_controller(db, Disease, Symptom, User, ExpertRule)
    from controllers.admin_controller import admin_bp
    app.register_blueprint(admin_bp)
    
    # Database initialization
    with app.app_context():
        db.create_all()
        seed_database(db, Disease, Symptom, DiseaseSymptom, ExpertRule, disease_symptom)
        seed_users(db, User)
    
    return app

def seed_database(db, Disease, Symptom, DiseaseSymptom, ExpertRule, disease_symptom):
    """Seed the database with initial rice disease data"""
    from werkzeug.security import generate_password_hash
    
    # Check if data already exists
    if Disease.query.first():
        return
    
    # Create symptoms
    symptoms_data = [
        'Brown spots on leaves',
        'Yellowing of leaves',
        'White powdery growth',
        'Water-soaked lesions',
        'Dark brown lesions',
        'Leaf blight',
        'Stem rot',
        'Root rot',
        'Grain discoloration',
        'Stunted growth',
        'Wilting',
        'Leaf spots with yellow halo',
        'Orange pustules',
        'Black spots on grains',
        'Leaf curling'
    ]
    
    symptoms = {}
    for symptom_name in symptoms_data:
        symptom = Symptom(name=symptom_name)
        db.session.add(symptom)
        symptoms[symptom_name] = symptom
    
    # Create diseases
    diseases_data = [
        {
            'name': 'Brown Spot',
            'description': 'Caused by Bipolaris oryzae, affects leaves and grains',
            'treatment': 'Use resistant varieties, apply fungicides like propiconazole',
            'symptoms': ['Brown spots on leaves', 'Dark brown lesions', 'Grain discoloration']
        },
        {
            'name': 'Blast Disease',
            'description': 'Caused by Magnaporthe oryzae, most destructive rice disease',
            'treatment': 'Use resistant varieties, avoid excessive nitrogen, apply tricyclazole',
            'symptoms': ['Brown spots on leaves', 'Water-soaked lesions', 'Leaf blight', 'Stem rot']
        },
        {
            'name': 'Sheath Blight',
            'description': 'Caused by Rhizoctonia solani, affects sheaths and leaves',
            'treatment': 'Use resistant varieties, proper spacing, apply validamycin',
            'symptoms': ['Water-soaked lesions', 'Leaf blight', 'Stem rot', 'Wilting']
        },
        {
            'name': 'Bacterial Leaf Blight',
            'description': 'Caused by Xanthomonas oryzae, affects leaves',
            'treatment': 'Use resistant varieties, avoid overhead irrigation, apply copper-based bactericides',
            'symptoms': ['Yellowing of leaves', 'Water-soaked lesions', 'Leaf blight', 'Wilting']
        },
        {
            'name': 'False Smut',
            'description': 'Caused by Ustilaginoidea virens, affects grains',
            'treatment': 'Use resistant varieties, proper field drainage, apply propiconazole',
            'symptoms': ['Grain discoloration', 'Black spots on grains', 'Stunted growth']
        },
        {
            'name': 'Rice Rust',
            'description': 'Caused by Puccinia graminis, affects leaves',
            'treatment': 'Use resistant varieties, apply fungicides like tebuconazole',
            'symptoms': ['Orange pustules', 'Yellowing of leaves', 'Leaf spots with yellow halo']
        },
        {
            'name': 'Powdery Mildew',
            'description': 'Caused by Erysiphe graminis, affects leaves',
            'treatment': 'Use resistant varieties, improve air circulation, apply sulfur-based fungicides',
            'symptoms': ['White powdery growth', 'Yellowing of leaves', 'Leaf curling']
        },
        {
            'name': 'Root Rot',
            'description': 'Caused by various fungi, affects roots',
            'treatment': 'Improve drainage, use healthy seeds, apply fungicides to soil',
            'symptoms': ['Root rot', 'Stunted growth', 'Wilting', 'Yellowing of leaves']
        }
    ]
    
    for disease_info in diseases_data:
        disease = Disease(
            name=disease_info['name'],
            description=disease_info['description'],
            treatment=disease_info['treatment']
        )
        db.session.add(disease)
        db.session.flush()
        
        # Link symptoms to disease
        for symptom_name in disease_info['symptoms']:
            if symptom_name in symptoms:
                disease_symptom_assoc = DiseaseSymptom(
                    disease_id=disease.id,
                    symptom_id=symptoms[symptom_name].id,
                    severity=1
                )
                db.session.add(disease_symptom_assoc)
    
    # Create expert rules
    expert_rules = [
        {
            'condition': "has_symptom('Brown spots on leaves') and has_symptom('Dark brown lesions')",
            'disease_name': 'Brown Spot',
            'confidence': 0.9
        },
        {
            'condition': "has_symptom('Water-soaked lesions') and has_symptom('Leaf blight')",
            'disease_name': 'Blast Disease',
            'confidence': 0.85
        },
        {
            'condition': "has_symptom('Water-soaked lesions') and has_symptom('Stem rot')",
            'disease_name': 'Sheath Blight',
            'confidence': 0.8
        },
        {
            'condition': "has_symptom('Yellowing of leaves') and has_symptom('Water-soaked lesions')",
            'disease_name': 'Bacterial Leaf Blight',
            'confidence': 0.85
        },
        {
            'condition': "has_symptom('Grain discoloration') and has_symptom('Black spots on grains')",
            'disease_name': 'False Smut',
            'confidence': 0.9
        },
        {
            'condition': "has_symptom('Orange pustules') and has_symptom('Yellowing of leaves')",
            'disease_name': 'Rice Rust',
            'confidence': 0.88
        },
        {
            'condition': "has_symptom('White powdery growth') and has_symptom('Yellowing of leaves')",
            'disease_name': 'Powdery Mildew',
            'confidence': 0.87
        },
        {
            'condition': "has_symptom('Root rot') and has_symptom('Stunted growth')",
            'disease_name': 'Root Rot',
            'confidence': 0.82
        }
    ]
    
    for rule_info in expert_rules:
        disease = Disease.query.filter_by(name=rule_info['disease_name']).first()
        if disease:
            rule = ExpertRule(
                condition=rule_info['condition'],
                disease_id=disease.id,
                confidence=rule_info['confidence']
            )
            db.session.add(rule)
    
    db.session.commit()

def seed_users(db, User):
    """Seed default admin and test users"""
    from werkzeug.security import generate_password_hash
    
    if User.query.first():
        return
    
    # Create default admin user
    admin = User(
        username='admin',
        email='admin@riceexpert.com',
        password_hash=generate_password_hash('admin123'),
        role='admin'
    )
    db.session.add(admin)
    
    # Create test end-user
    enduser = User(
        username='user',
        email='user@riceexpert.com',
        password_hash=generate_password_hash('user123'),
        role='end-user'
    )
    db.session.add(enduser)
    
    db.session.commit()

