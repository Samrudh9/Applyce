"""
Feedback model for storing user feedback on predictions.
"""

from datetime import datetime
from models import db


class Feedback(db.Model):
    """Feedback model for storing user feedback on career predictions."""
    
    __tablename__ = 'feedbacks'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=True, index=True)
    
    # Feedback details
    feedback_type = db.Column(db.String(20), nullable=False)  # 'positive', 'negative'
    predicted_career = db.Column(db.String(100))
    correct_career = db.Column(db.String(100))  # User correction if negative
    skills = db.Column(db.Text)  # JSON string of skills at time of prediction
    
    # Additional context
    comments = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Feedback {self.id} - {self.feedback_type}>'
    
    def is_positive(self):
        """Check if feedback is positive."""
        return self.feedback_type == 'positive'
    
    def has_correction(self):
        """Check if feedback includes a correction."""
        return self.correct_career is not None and self.correct_career != self.predicted_career
