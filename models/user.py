"""
User model for authentication.
"""

import secrets
from datetime import datetime, timedelta, date
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from models import db


# Freemium tier limits
TIER_LIMITS = {
    'free': {
        'daily_scans': 3,
        'features': ['basic_ats_score', 'skill_gap_analysis', 'career_roadmap']
    },
    'premium': {
        'daily_scans': 50,
        'features': ['basic_ats_score', 'skill_gap_analysis', 'career_roadmap',
                    'detailed_salary_insights', 'job_matching', 'pdf_export',
                    'email_reports', 'priority_support']
    },
    'enterprise': {
        'daily_scans': -1,  # Unlimited
        'features': ['all']
    }
}

# Password reset token configuration
RESET_TOKEN_BYTES = 32  # Length of secure token in bytes
RESET_TOKEN_EXPIRY_HOURS = 1  # Token expires after 1 hour


class User(UserMixin, db.Model):
    """User model for authentication and tracking."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Password reset fields
    reset_token = db.Column(db.String(100), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)
    
    # Freemium fields
    account_type = db.Column(db.String(20), default='free')  # 'free', 'premium', 'enterprise'
    resume_scans_today = db.Column(db.Integer, default=0)
    resume_scans_total = db.Column(db.Integer, default=0)
    last_scan_date = db.Column(db.Date, nullable=True)
    premium_expires_at = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    resumes = db.relationship('Resume', backref='user', lazy='dynamic')
    feedbacks = db.relationship('Feedback', backref='user', lazy='dynamic')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def update_last_login(self):
        """Update the last login timestamp."""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    # ===== Password Reset Methods =====
    
    def generate_reset_token(self) -> str:
        """
        Generate a secure password reset token.
        Token expires based on RESET_TOKEN_EXPIRY_HOURS constant.
        
        Returns:
            str: The generated reset token
        """
        self.reset_token = secrets.token_urlsafe(RESET_TOKEN_BYTES)
        self.reset_token_expiry = datetime.utcnow() + timedelta(hours=RESET_TOKEN_EXPIRY_HOURS)
        db.session.commit()
        return self.reset_token
    
    def verify_reset_token(self, token: str) -> bool:
        """
        Verify if the provided reset token is valid and not expired.
        
        Args:
            token: The reset token to verify
            
        Returns:
            bool: True if token is valid, False otherwise
        """
        if not self.reset_token or not self.reset_token_expiry:
            return False
        
        if self.reset_token != token:
            return False
        
        if datetime.utcnow() > self.reset_token_expiry:
            return False
        
        return True
    
    def clear_reset_token(self):
        """Clear the reset token after successful password reset."""
        self.reset_token = None
        self.reset_token_expiry = None
        db.session.commit()
    
    def reset_password(self, new_password: str) -> bool:
        """
        Reset the user's password and clear the reset token.
        
        Args:
            new_password: The new password to set
            
        Returns:
            bool: True if password was reset successfully
        """
        self.set_password(new_password)
        self.clear_reset_token()
        return True
    
    # ===== Freemium Methods =====
    
    @property
    def is_premium(self) -> bool:
        """Check if user has an active premium subscription."""
        if self.account_type == 'enterprise':
            return True
        
        if self.account_type == 'premium':
            if self.premium_expires_at is None:
                return False
            return datetime.utcnow() < self.premium_expires_at
        
        return False
    
    @property
    def daily_scan_limit(self) -> int:
        """Get the daily scan limit based on account type."""
        tier = TIER_LIMITS.get(self.account_type, TIER_LIMITS['free'])
        return tier['daily_scans']
    
    @property
    def scans_remaining_today(self) -> int:
        """Get the number of scans remaining for today."""
        # Reset count if it's a new day
        today = date.today()
        if self.last_scan_date != today:
            return self.daily_scan_limit
        
        if self.daily_scan_limit == -1:  # Unlimited
            return -1
        
        return max(0, self.daily_scan_limit - self.resume_scans_today)
    
    def can_scan_resume(self) -> bool:
        """
        Check if user can perform a resume scan.
        
        Returns:
            bool: True if user can scan, False if limit reached
        """
        # Enterprise users have unlimited scans
        if self.account_type == 'enterprise':
            return True
        
        # Premium users with valid subscription
        if self.is_premium:
            return self.scans_remaining_today != 0
        
        # Free users
        return self.scans_remaining_today > 0
    
    def record_scan(self):
        """Record a resume scan for the user."""
        today = date.today()
        
        # Reset daily count if it's a new day
        if self.last_scan_date != today:
            self.resume_scans_today = 0
            self.last_scan_date = today
        
        self.resume_scans_today += 1
        self.resume_scans_total += 1
        db.session.commit()
    
    def upgrade_to_premium(self, months: int = 1):
        """
        Upgrade user to premium account.
        
        Args:
            months: Number of months for premium subscription
        """
        self.account_type = 'premium'
        
        # If already premium, extend the expiry
        if self.premium_expires_at and self.premium_expires_at > datetime.utcnow():
            self.premium_expires_at += timedelta(days=30 * months)
        else:
            self.premium_expires_at = datetime.utcnow() + timedelta(days=30 * months)
        
        db.session.commit()
    
    def get_feature_access(self) -> dict:
        """
        Get a dictionary of feature access based on account type.
        
        Returns:
            dict: Feature name to boolean access mapping
        """
        tier = TIER_LIMITS.get(self.account_type, TIER_LIMITS['free'])
        features = tier['features']
        
        # All features for enterprise
        if 'all' in features:
            all_features = set()
            for tier_info in TIER_LIMITS.values():
                all_features.update(tier_info.get('features', []))
            all_features.discard('all')
            features = list(all_features)
        
        return {
            'basic_ats_score': 'basic_ats_score' in features,
            'skill_gap_analysis': 'skill_gap_analysis' in features,
            'career_roadmap': 'career_roadmap' in features,
            'detailed_salary_insights': 'detailed_salary_insights' in features,
            'job_matching': 'job_matching' in features,
            'pdf_export': 'pdf_export' in features,
            'email_reports': 'email_reports' in features,
            'priority_support': 'priority_support' in features,
            'daily_scans_remaining': self.scans_remaining_today,
            'is_premium': self.is_premium,
            'account_type': self.account_type
        }
