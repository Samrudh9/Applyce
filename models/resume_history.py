"""
Resume History model for tracking user's resume upload history.
"""

from datetime import datetime
from models import db


class ResumeHistory(db.Model):
    """Store user's resume upload history and analysis results"""
    __tablename__ = 'resume_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Resume metadata
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Scores
    overall_score = db.Column(db.Integer, default=0)
    keyword_score = db.Column(db.Integer, default=0)
    format_score = db.Column(db.Integer, default=0)
    section_score = db.Column(db.Integer, default=0)
    
    # Career predictions
    predicted_career = db.Column(db.String(100))
    career_confidence = db.Column(db.Float, default=0.0)
    top_careers = db.Column(db.Text)  # JSON string of top 3 careers
    
    # Skills data
    skills_detected = db.Column(db.Text)  # JSON string
    skills_missing = db.Column(db.Text)   # JSON string
    skill_count = db.Column(db.Integer, default=0)
    
    # Salary prediction
    predicted_salary_min = db.Column(db.Integer)
    predicted_salary_max = db.Column(db.Integer)
    
    # Relationship
    user = db.relationship('User', backref=db.backref('resume_history', lazy='dynamic', order_by='ResumeHistory.upload_date.desc()'))
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization"""
        import json
        return {
            'id': self.id,
            'filename': self.filename,
            'upload_date': self.upload_date.isoformat() if self.upload_date else None,
            'overall_score': self.overall_score,
            'keyword_score': self.keyword_score,
            'format_score': self.format_score,
            'section_score': self.section_score,
            'predicted_career': self.predicted_career,
            'career_confidence': self.career_confidence,
            'top_careers': json.loads(self.top_careers) if self.top_careers else [],
            'skills_detected': json.loads(self.skills_detected) if self.skills_detected else [],
            'skills_missing': json.loads(self.skills_missing) if self.skills_missing else [],
            'skill_count': self.skill_count,
            'predicted_salary_min': self.predicted_salary_min,
            'predicted_salary_max': self.predicted_salary_max
        }
