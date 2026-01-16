# Authentication & Authorization Guide

## Overview

The Rice Disease Expert System now includes a complete authentication and authorization system with role-based access control.

## User Roles

### Admin
- **Full Access**: Can manage all aspects of the system
- **Capabilities**:
  - View and manage diseases (add, delete)
  - View and manage symptoms (add, delete)
  - View and manage users
  - Access admin dashboard
  - Create new admin users

### End User
- **Read-Only Access**: Can view and use diagnosis features
- **Capabilities**:
  - View diseases and symptoms
  - Use diagnosis feature
  - View disease details
  - Cannot modify any data

## Default Accounts

After first run, the following accounts are automatically created:

1. **Admin Account**
   - Username: `admin`
   - Password: `admin123`
   - Role: Admin

2. **End User Account**
   - Username: `user`
   - Password: `user123`
   - Role: End User

## Authentication Routes

### Public Routes (No Login Required)
- `/` - Home page
- `/login` - Login page
- `/register` - Registration page
- `/diseases` - View all diseases
- `/disease/<id>` - View disease details

### Protected Routes (Login Required)
- `/diagnosis` - Disease diagnosis (available to all logged-in users)
- `/logout` - Logout

### Admin Only Routes
- `/admin/dashboard` - Admin dashboard
- `/admin/diseases` - Manage diseases
- `/admin/symptoms` - Manage symptoms
- `/admin/users` - Manage users
- `/admin/disease/add` - Add new disease
- `/admin/symptom/add` - Add new symptom
- `/admin/disease/<id>/delete` - Delete disease
- `/admin/symptom/<id>/delete` - Delete symptom

## Registration

### For Regular Users
- Navigate to `/register`
- Fill in username, email, and password
- Role is automatically set to "end-user"
- After registration, login to access features

### For Admins (Creating New Admin)
- Admin users can create new admin accounts
- Login as admin
- Go to Admin → Manage Users → Add New User
- Select "Admin" role when creating the user

## Security Features

1. **Password Hashing**: All passwords are hashed using Werkzeug's password hashing
2. **Session Management**: Flask-Login handles user sessions
3. **Role-Based Access Control**: Decorators protect admin routes
4. **CSRF Protection**: Forms include CSRF protection (Flask default)

## Usage Examples

### Login
```python
# Navigate to /login
# Enter username and password
# Redirected to home page after successful login
```

### Admin Access
```python
# Login as admin
# Access Admin menu in navigation
# Use dashboard to manage system
```

### End User Access
```python
# Login as end-user
# Can view diseases and use diagnosis
# Cannot access admin features
```

## Implementation Details

### Models
- `User` model with username, email, password_hash, and role
- Roles: 'admin' or 'end-user'

### Decorators
- `@login_required`: Requires user to be logged in
- `@admin_required`: Requires admin role

### Templates
- Login and register forms
- Admin dashboard and management pages
- Updated navigation with user menu

## Notes

- Change default passwords after first login
- Admin accounts should be created carefully
- End users cannot escalate their privileges
- All admin actions require authentication



