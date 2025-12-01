"""
User Preferences model for storing career preferences and settings.
"""

from datetime import datetime
from models import db


class UserPreferences(db.Model):
    """Store user's career preferences and analysis settings."""
    
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    
    # Default analysis settings
    default_experience_level = db.Column(db.String(50))  # beginner, mid-level, senior-level
    default_target_role = db.Column(db.String(100))  # e.g., "Backend Developer"
    preferred_industries = db.Column(db.JSON)  # List of industries
    
    # Career goals
    target_salary_min = db.Column(db.Integer)
    target_salary_max = db.Column(db.Integer)
    preferred_locations = db.Column(db.JSON)  # List of locations
    remote_preference = db.Column(db.String(20))  # remote, hybrid, onsite
    
    # Notification preferences
    email_notifications = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('preferences', uselist=False))
    
    def __repr__(self):
        return f'<UserPreferences for user_id={self.user_id}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'default_experience_level': self.default_experience_level,
            'default_target_role': self.default_target_role,
            'preferred_industries': self.preferred_industries or [],
            'target_salary_min': self.target_salary_min,
            'target_salary_max': self.target_salary_max,
            'preferred_locations': self.preferred_locations or [],
            'remote_preference': self.remote_preference,
            'email_notifications': self.email_notifications,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
    
    @classmethod
    def get_or_create(cls, user_id):
        """Get existing preferences or create new ones for a user."""
        preferences = cls.query.filter_by(user_id=user_id).first()
        if not preferences:
            preferences = cls(user_id=user_id)
            db.session.add(preferences)
            db.session.commit()
        return preferences
