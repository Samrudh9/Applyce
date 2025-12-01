"""
Resume model for storing uploaded resume data.
"""

import hashlib
from datetime import datetime
from models import db


class Resume(db.Model):
    """Resume model for storing parsed resume information."""
    
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True, index=True)
    
    # File info
    filename = db.Column(db.String(255))
    file_hash = db.Column(db.String(64))  # To detect duplicates
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User Context
    experience_level = db.Column(db.String(50))  # beginner, mid-level, senior-level
    target_role = db.Column(db.String(100))  # e.g., "Backend Developer"
    job_search_status = db.Column(db.String(50))  # actively_applying, exploring, etc.
    
    # Extracted Content
    raw_text = db.Column(db.Text)
    extracted_text = db.Column(db.Text)  # Kept for backward compatibility
    
    # Analysis Results (stored as JSON)
    skills = db.Column(db.JSON)  # List of extracted skills
    education = db.Column(db.JSON)  # Education details
    experience = db.Column(db.JSON)  # Work experience
    projects = db.Column(db.JSON)  # Projects
    certifications = db.Column(db.JSON)  # Certifications
    contact_info = db.Column(db.JSON)  # Email, phone, LinkedIn, GitHub
    
    # Scores - Resume Quality Score (matches ATS score)
    overall_score = db.Column(db.Integer)  # 0-100
    score_breakdown = db.Column(db.JSON)  # {"keyword_score": 80, "format_score": 75, "section_score": 85}
    ats_score = db.Column(db.Integer)  # ATS compatibility score (same as overall_score for consistency)
    ats_issues = db.Column(db.JSON)  # List of ATS issues
    
    # Kept for backward compatibility
    quality_score = db.Column(db.Integer)
    confidence_score = db.Column(db.Float)
    salary_estimate = db.Column(db.String(50))
    
    # Career Prediction
    predicted_career = db.Column(db.String(100))
    career_confidence = db.Column(db.Float)
    alternative_careers = db.Column(db.JSON)  # Top 3 alternatives
    
    # Feedback & Improvements
    feedback = db.Column(db.JSON)  # List of improvement suggestions
    missing_keywords = db.Column(db.JSON)  # Keywords missing for target role
    
    # Legacy field for backward compatibility
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    feedbacks = db.relationship('Feedback', backref='resume', lazy='dynamic')
    histories = db.relationship('ResumeVersion', backref='resume', lazy='dynamic')
    
    def __repr__(self):
        return f'<Resume {self.id} - {self.predicted_career}>'
    
    def get_skills_list(self):
        """Return skills as a Python list."""
        import json
        if self.skills:
            if isinstance(self.skills, list):
                return self.skills
            try:
                return json.loads(self.skills) if isinstance(self.skills, str) else self.skills
            except (json.JSONDecodeError, TypeError):
                return self.skills.split(',') if isinstance(self.skills, str) else []
        return []
    
    def set_skills_list(self, skills_list):
        """Set skills from a Python list."""
        self.skills = skills_list if isinstance(skills_list, list) else []
    
    @staticmethod
    def compute_file_hash(file_content):
        """Compute SHA-256 hash of file content to detect duplicates."""
        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8')
        return hashlib.sha256(file_content).hexdigest()
    
    def to_dict(self):
        """Convert resume to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'experience_level': self.experience_level,
            'target_role': self.target_role,
            'overall_score': self.overall_score,
            'ats_score': self.ats_score,
            'score_breakdown': self.score_breakdown,
            'predicted_career': self.predicted_career,
            'career_confidence': self.career_confidence,
            'alternative_careers': self.alternative_careers,
            'skills': self.get_skills_list(),
            'feedback': self.feedback,
            'missing_keywords': self.missing_keywords,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }


class ResumeVersion(db.Model):
    """Track resume versions and score improvements over time."""
    
    __tablename__ = 'resume_versions'
    
    id = db.Column(db.Integer, primary_key=True)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    version = db.Column(db.Integer, default=1)
    
    # Snapshot of scores at this version
    overall_score = db.Column(db.Integer)
    ats_score = db.Column(db.Integer)
    score_breakdown = db.Column(db.JSON)
    
    # What changed
    changes_made = db.Column(db.JSON)  # List of improvements applied
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ResumeVersion {self.id} - Resume {self.resume_id} v{self.version}>'
    
    def to_dict(self):
        """Convert to dictionary for JSON serialization."""
        return {
            'id': self.id,
            'resume_id': self.resume_id,
            'version': self.version,
            'overall_score': self.overall_score,
            'ats_score': self.ats_score,
            'score_breakdown': self.score_breakdown,
            'changes_made': self.changes_made,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
