"""
Resume model for storing uploaded resume data.
"""

from datetime import datetime
from models import db


class Resume(db.Model):
    """Resume model for storing parsed resume information."""
    
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    filename = db.Column(db.String(255))
    extracted_text = db.Column(db.Text)
    skills = db.Column(db.Text)  # JSON string of detected skills
    education = db.Column(db.Text)
    experience = db.Column(db.Text)
    predicted_career = db.Column(db.String(100))
    confidence_score = db.Column(db.Float)
    quality_score = db.Column(db.Integer)
    salary_estimate = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    feedbacks = db.relationship('Feedback', backref='resume', lazy='dynamic')
    
    def __repr__(self):
        return f'<Resume {self.id} - {self.predicted_career}>'
    
    def get_skills_list(self):
        """Return skills as a Python list."""
        import json
        if self.skills:
            try:
                return json.loads(self.skills)
            except json.JSONDecodeError:
                return self.skills.split(',')
        return []
    
    def set_skills_list(self, skills_list):
        """Set skills from a Python list."""
        import json
        self.skills = json.dumps(skills_list)
