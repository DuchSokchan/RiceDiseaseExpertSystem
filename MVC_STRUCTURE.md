# MVC Architecture Documentation

## Project Structure

The project has been refactored to follow MVC (Model-View-Controller) architecture:

```
Assignment/
├── app.py                 # Main entry point
├── app_factory.py         # Application factory (creates Flask app)
├── config.py              # Configuration settings
├── models.py              # Database models (Model layer)
├── translations.py        # Translation dictionaries
├── controllers/           # Controllers (Controller layer)
│   ├── __init__.py
│   ├── auth_controller.py      # Authentication routes
│   ├── welcome_controller.py   # Welcome page & language
│   ├── home_controller.py      # Home page
│   ├── diagnosis_controller.py # Diagnosis routes
│   ├── disease_controller.py   # Disease listing & details
│   └── admin_controller.py     # Admin operations
├── services/              # Business logic (Service layer)
│   ├── __init__.py
│   └── expert_system_service.py # Expert system logic
├── utils/                 # Utilities
│   ├── __init__.py
│   ├── decorators.py      # Custom decorators
│   └── helpers.py         # Helper functions
└── templates/             # Views (View layer)
    ├── base.html
    ├── welcome.html
    ├── login.html
    ├── register.html
    ├── index.html
    ├── diagnosis.html
    ├── results.html
    ├── diseases.html
    ├── disease_detail.html
    └── admin/
        ├── dashboard.html
        ├── diseases.html
        ├── symptoms.html
        ├── users.html
        ├── add_disease.html
        └── add_symptom.html
```

## Architecture Layers

### 1. Model Layer (`models.py`)
- **Purpose**: Database models and data structure
- **Contains**: SQLAlchemy models (Disease, Symptom, User, ExpertRule, etc.)
- **Responsibility**: Define data structure and relationships

### 2. View Layer (`templates/`)
- **Purpose**: Presentation layer (HTML templates)
- **Contains**: Jinja2 templates for rendering HTML
- **Responsibility**: Display data to users

### 3. Controller Layer (`controllers/`)
- **Purpose**: Handle HTTP requests and responses
- **Contains**: Blueprint-based route handlers
- **Responsibility**: 
  - Receive user requests
  - Call services/models
  - Return responses (render templates)

### 4. Service Layer (`services/`)
- **Purpose**: Business logic
- **Contains**: Expert system logic, complex calculations
- **Responsibility**: Process business rules and algorithms

### 5. Utilities (`utils/`)
- **Purpose**: Reusable helper functions
- **Contains**: Decorators, helpers, common functions
- **Responsibility**: Shared functionality across the application

## Controllers

### Auth Controller (`auth_controller.py`)
- Routes:
  - `/auth/login` - User login
  - `/auth/register` - User registration
  - `/auth/logout` - User logout

### Welcome Controller (`welcome_controller.py`)
- Routes:
  - `/` - Welcome page
  - `/set_language/<lang>` - Change language

### Home Controller (`home_controller.py`)
- Routes:
  - `/home` - Home page (requires login)

### Diagnosis Controller (`diagnosis_controller.py`)
- Routes:
  - `/diagnosis` - Disease diagnosis (GET/POST)

### Disease Controller (`disease_controller.py`)
- Routes:
  - `/diseases` - List all diseases
  - `/disease/<id>` - Disease details

### Admin Controller (`admin_controller.py`)
- Routes:
  - `/admin/dashboard` - Admin dashboard
  - `/admin/diseases` - Manage diseases
  - `/admin/symptoms` - Manage symptoms
  - `/admin/users` - Manage users
  - `/admin/disease/add` - Add disease
  - `/admin/disease/<id>/delete` - Delete disease
  - `/admin/symptom/add` - Add symptom
  - `/admin/symptom/<id>/delete` - Delete symptom

## Benefits of MVC Architecture

1. **Separation of Concerns**: Each layer has a specific responsibility
2. **Maintainability**: Easy to locate and modify code
3. **Scalability**: Easy to add new features
4. **Testability**: Each component can be tested independently
5. **Reusability**: Services and utilities can be reused
6. **Organization**: Clear project structure

## How It Works

1. **Request Flow**:
   - User makes HTTP request → Controller receives it
   - Controller calls Service/Model → Processes business logic
   - Controller renders View → Returns HTML response

2. **Application Factory Pattern**:
   - `app_factory.py` creates Flask app instance
   - Initializes all extensions (DB, LoginManager)
   - Registers all blueprints (controllers)
   - Seeds database

3. **Dependency Injection**:
   - Models and services are injected into controllers
   - Controllers initialized with required dependencies
   - Avoids circular imports

## Running the Application

```bash
python app.py
```

The application factory creates the Flask app with all MVC components properly initialized.

