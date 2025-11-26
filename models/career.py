"""
Career model for storing career information.
"""

from datetime import datetime
from models import db


class Career(db.Model):
    """Career model for storing career details."""
    
    __tablename__ = 'careers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    category = db.Column(db.String(50), index=True)
    description = db.Column(db.Text)
    
    # Requirements
    required_skills = db.Column(db.Text)  # JSON list
    preferred_skills = db.Column(db.Text)  # JSON list
    education_requirements = db.Column(db.String(200))
    experience_years = db.Column(db.String(20))  # e.g., "0-2", "3-5", "5+"
    
    # Salary information
    salary_min = db.Column(db.Integer)  # In INR
    salary_max = db.Column(db.Integer)  # In INR
    salary_currency = db.Column(db.String(10), default='INR')
    
    # Market info
    job_outlook = db.Column(db.String(50))  # 'High', 'Medium', 'Low'
    growth_rate = db.Column(db.Float)  # Percentage
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Career {self.name}>'
    
    def get_required_skills_list(self):
        """Return required skills as a Python list."""
        import json
        if self.required_skills:
            try:
                return json.loads(self.required_skills)
            except json.JSONDecodeError:
                return self.required_skills.split(',')
        return []
    
    def set_required_skills_list(self, skills_list):
        """Set required skills from a Python list."""
        import json
        self.required_skills = json.dumps(skills_list)
    
    def get_preferred_skills_list(self):
        """Return preferred skills as a Python list."""
        import json
        if self.preferred_skills:
            try:
                return json.loads(self.preferred_skills)
            except json.JSONDecodeError:
                return self.preferred_skills.split(',')
        return []
    
    def set_preferred_skills_list(self, skills_list):
        """Set preferred skills from a Python list."""
        import json
        self.preferred_skills = json.dumps(skills_list)
    
    def get_salary_range_display(self):
        """Return formatted salary range."""
        if self.salary_min and self.salary_max:
            min_lakh = self.salary_min / 100000
            max_lakh = self.salary_max / 100000
            return f"₹{min_lakh:.1f}L - ₹{max_lakh:.1f}L"
        return "Salary not available"
