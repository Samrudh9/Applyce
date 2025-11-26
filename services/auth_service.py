"""
Authentication service for user management.
"""

import re
from flask import current_app
from flask_login import login_user, logout_user
from models import db
from models.user import User


class AuthService:
    """Service for handling user authentication."""
    
    # Password requirements
    MIN_PASSWORD_LENGTH = 8
    
    @staticmethod
    def validate_email(email):
        """Validate email format."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def validate_username(username):
        """Validate username format."""
        if not username or len(username) < 3 or len(username) > 80:
            return False, "Username must be between 3 and 80 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        return True, None
    
    @staticmethod
    def validate_password(password):
        """Validate password strength."""
        if not password or len(password) < AuthService.MIN_PASSWORD_LENGTH:
            return False, f"Password must be at least {AuthService.MIN_PASSWORD_LENGTH} characters"
        return True, None
    
    @classmethod
    def register_user(cls, username, email, password):
        """
        Register a new user.
        
        Returns:
            tuple: (success: bool, user_or_error: User or str)
        """
        # Validate input
        valid, error = cls.validate_username(username)
        if not valid:
            return False, error
        
        if not cls.validate_email(email):
            return False, "Invalid email format"
        
        valid, error = cls.validate_password(password)
        if not valid:
            return False, error
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return False, "Username already taken"
        
        if User.query.filter_by(email=email).first():
            return False, "Email already registered"
        
        # Create new user
        try:
            user = User(username=username, email=email)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            return True, user
        except Exception as e:
            db.session.rollback()
            return False, f"Registration failed: {str(e)}"
    
    @staticmethod
    def authenticate_user(username_or_email, password):
        """
        Authenticate a user by username/email and password.
        
        Returns:
            tuple: (success: bool, user_or_error: User or str)
        """
        # Try to find user by username or email
        user = User.query.filter(
            (User.username == username_or_email) | 
            (User.email == username_or_email)
        ).first()
        
        if not user:
            return False, "Invalid username/email or password"
        
        if not user.is_active:
            return False, "Account is disabled"
        
        if not user.check_password(password):
            return False, "Invalid username/email or password"
        
        return True, user
    
    @staticmethod
    def login(user, remember=False):
        """
        Log in a user using Flask-Login.
        
        Args:
            user: User object
            remember: Whether to remember the user
            
        Returns:
            bool: Success status
        """
        try:
            login_user(user, remember=remember)
            user.update_last_login()
            return True
        except Exception:
            return False
    
    @staticmethod
    def logout():
        """Log out the current user."""
        logout_user()
        return True
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user by ID (for Flask-Login loader)."""
        return User.query.get(int(user_id))
