# Rice Disease Expert System

A Flask-based web application that uses an expert system to diagnose rice diseases based on symptoms. The system combines rule-based reasoning with symptom pattern matching to provide accurate disease diagnosis and treatment recommendations.

## Features

- **Expert System Diagnosis**: Rule-based and symptom-matching algorithms for accurate disease identification
- **Comprehensive Disease Database**: Information about 8 common rice diseases with symptoms and treatments
- **Interactive Web Interface**: Modern, responsive UI built with Bootstrap and Jinja2 templates
- **SQLAlchemy Database**: Persistent storage for diseases, symptoms, and expert rules
- **Confidence Scoring**: Each diagnosis includes a confidence percentage
- **User Authentication**: Login and registration system with role-based access control
- **Admin Panel**: Full administrative control for managing diseases, symptoms, and users
- **Role-Based Access**: Admin can manage everything, End-users can only view and diagnose

## Technologies Used

- **Flask 3.0.0**: Web framework
- **SQLAlchemy 2.0.45**: ORM for database operations
- **Flask-Login 0.6.3**: User session management
- **Jinja2 3.1.2**: Template engine
- **Bootstrap 5.3.0**: Frontend framework
- **SQLite**: Database (default, can be changed in config.py)

## Installation

1. **Clone or download the project**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python app.py
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:5000`

## Project Structure

```
Assignment/
├── app.py                 # Main Flask application
├── config.py              # Configuration settings
├── models.py              # SQLAlchemy database models
├── expert_system.py       # Expert system logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/            # Jinja2 templates
│   ├── base.html         # Base template
│   ├── index.html        # Home page
│   ├── diagnosis.html    # Diagnosis form
│   ├── results.html      # Diagnosis results
│   ├── diseases.html     # Disease list
│   └── disease_detail.html # Disease details
└── static/               # Static files (CSS, JS)
```

## Database Models

- **Disease**: Stores disease information (name, description, treatment)
- **Symptom**: Stores symptom descriptions
- **DiseaseSymptom**: Association table linking diseases to symptoms
- **ExpertRule**: Stores expert system rules for diagnosis

## How It Works

1. **Symptom Selection**: Users select symptoms observed in their rice plants
2. **Rule-Based Analysis**: The system evaluates expert rules against selected symptoms
3. **Pattern Matching**: Calculates similarity between selected symptoms and disease symptom patterns
4. **Confidence Scoring**: Combines results from both methods with weighted confidence scores
5. **Results Display**: Shows ranked diagnosis results with treatment recommendations

## Expert System Methods

1. **Rule-Based Diagnosis**: Uses predefined expert rules with conditions like:
   - `has_symptom('Brown spots on leaves') and has_symptom('Dark brown lesions')`

2. **Symptom Matching**: Calculates match ratio between selected symptoms and disease symptoms

3. **Combined Scoring**: Merges results from both methods with weighted confidence

## Included Diseases

1. **Brown Spot** - Caused by Bipolaris oryzae
2. **Blast Disease** - Caused by Magnaporthe oryzae
3. **Sheath Blight** - Caused by Rhizoctonia solani
4. **Bacterial Leaf Blight** - Caused by Xanthomonas oryzae
5. **False Smut** - Caused by Ustilaginoidea virens
6. **Rice Rust** - Caused by Puccinia graminis
7. **Powdery Mildew** - Caused by Erysiphe graminis
8. **Root Rot** - Caused by various fungi

## Configuration

Edit `config.py` to customize:
- Database URI (default: SQLite)
- Secret key for sessions
- Other Flask configuration options

## Usage

### Default Accounts

After first run, default accounts are created:
- **Admin**: username: `admin`, password: `admin123`
- **End User**: username: `user`, password: `user123`

### User Roles

1. **Admin**:
   - Full access to all features
   - Can manage diseases, symptoms, and users
   - Access to admin dashboard
   - Can add/edit/delete content

2. **End User**:
   - Can view diseases and symptoms
   - Can use diagnosis feature
   - Cannot modify any data

### Features

1. **Home Page**: Overview of the system and common diseases
2. **Diagnosis**: Select symptoms and get diagnosis (available to all users)
3. **Diseases**: Browse all diseases in the database (available to all users)
4. **Disease Details**: View detailed information about a specific disease
5. **Admin Dashboard**: Manage system content (admin only)
6. **User Management**: View and manage users (admin only)

## Development

The database is automatically initialized on first run with seed data including:
- 15 common symptoms
- 8 rice diseases
- Expert system rules for diagnosis

## License

This project is created for educational purposes.

## Notes

- The expert system uses `eval()` for rule evaluation. In production, consider using a safer expression evaluator
- The database file (`rice_disease_expert.db`) will be created automatically on first run
- For production deployment, change the secret key in `config.py` and use a proper database like PostgreSQL
