import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    # SQLite database - no server required (change back to MySQL if needed)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///rice_expert_system.db'
    # For MySQL: 'mysql+pymysql://root:@localhost/rice_expert_system'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

