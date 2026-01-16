# Models file - db will be imported from app after initialization
# This avoids circular imports

def create_models(db):
    """Create all models with the db instance"""
    
    # Association table for many-to-many relationship between Disease and Symptom
    disease_symptom = db.Table('disease_symptom',
        db.Column('disease_id', db.Integer, db.ForeignKey('disease.id'), primary_key=True),
        db.Column('symptom_id', db.Integer, db.ForeignKey('symptom.id'), primary_key=True),
        db.Column('severity', db.Integer, default=1)
    )
    
    class Disease(db.Model):
        """Model for rice diseases"""
        __tablename__ = 'disease'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), unique=True, nullable=False)
        description = db.Column(db.Text, nullable=False)
        treatment = db.Column(db.Text, nullable=False)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        
        # Relationships
        symptoms = db.relationship('Symptom', secondary=disease_symptom, lazy='subquery',
                                   backref=db.backref('diseases', lazy=True))
        rules = db.relationship('ExpertRule', backref='disease', lazy=True, cascade='all, delete-orphan')
        
        def __repr__(self):
            return f'<Disease {self.name}>'
    
    class Symptom(db.Model):
        """Model for disease symptoms"""
        __tablename__ = 'symptom'
        
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(200), unique=True, nullable=False)
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        
        def __repr__(self):
            return f'<Symptom {self.name}>'
    
    class DiseaseSymptom(db.Model):
        """Association model for disease-symptom relationship with severity"""
        __tablename__ = 'disease_symptom_assoc'
        
        disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), primary_key=True)
        symptom_id = db.Column(db.Integer, db.ForeignKey('symptom.id'), primary_key=True)
        severity = db.Column(db.Integer, default=1)  # 1-5 scale
        
        disease = db.relationship('Disease', backref='disease_symptom_assocs')
        symptom = db.relationship('Symptom', backref='disease_symptom_assocs')
        
        def __repr__(self):
            return f'<DiseaseSymptom disease_id={self.disease_id} symptom_id={self.symptom_id}>'
    
    class ExpertRule(db.Model):
        """Model for expert system rules"""
        __tablename__ = 'expert_rule'
        
        id = db.Column(db.Integer, primary_key=True)
        condition = db.Column(db.Text, nullable=False)  # Rule condition as string
        disease_id = db.Column(db.Integer, db.ForeignKey('disease.id'), nullable=False)
        confidence = db.Column(db.Float, default=0.5)  # Confidence level 0-1
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        
        def __repr__(self):
            return f'<ExpertRule {self.id} -> Disease {self.disease_id}>'
    
    class User(db.Model):
        """Model for user authentication"""
        __tablename__ = 'user'
        
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(80), unique=True, nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(20), default='end-user', nullable=False)  # 'admin' or 'end-user'
        created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
        is_active = db.Column(db.Boolean, default=True)
        
        def __repr__(self):
            return f'<User {self.username}>'
        
        def is_admin(self):
            """Check if user is admin"""
            return self.role == 'admin'
        
        def get_id(self):
            """Required for Flask-Login"""
            return str(self.id)
        
        @property
        def is_authenticated(self):
            """Required for Flask-Login"""
            return True
        
        @property
        def is_anonymous(self):
            """Required for Flask-Login"""
            return False
    
    return Disease, Symptom, DiseaseSymptom, ExpertRule, disease_symptom, User
