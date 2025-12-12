"""
JobPattern model for storing job role patterns and required skills.
"""

from datetime import datetime
from models import db


class JobPattern(db.Model):
    """JobPattern model for tracking job descriptions and skill requirements."""
    
    __tablename__ = 'job_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Job role information
    job_role = db.Column(db.String(100), nullable=False, index=True)
    job_title = db.Column(db.String(200), nullable=True)
    
    # Skill requirements (stored as JSON or comma-separated)
    required_skills = db.Column(db.Text, nullable=False)  # Critical skills
    preferred_skills = db.Column(db.Text, nullable=True)  # Nice-to-have skills
    
    # Additional metadata
    description = db.Column(db.Text, nullable=True)
    experience_level = db.Column(db.String(50), nullable=True)  # Entry, Mid, Senior
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<JobPattern {self.job_role}>'
    
    @classmethod
    def get_by_role(cls, job_role):
        """Get job pattern by role."""
        return cls.query.filter_by(job_role=job_role.lower()).first()
    
    @classmethod
    def get_or_create_default(cls, job_role):
        """Get existing pattern or create a default one."""
        pattern = cls.get_by_role(job_role)
        if pattern:
            return pattern
        
        # Create a basic pattern based on common roles
        default_patterns = {
            'data scientist': {
                'required': 'python,sql,machine learning,statistics,data analysis',
                'preferred': 'tensorflow,pytorch,aws,docker,spark'
            },
            'frontend developer': {
                'required': 'html,css,javascript,react',
                'preferred': 'typescript,vue,angular,tailwind,webpack'
            },
            'backend developer': {
                'required': 'python,java,sql,api,rest',
                'preferred': 'docker,kubernetes,microservices,mongodb,redis'
            },
            'full stack developer': {
                'required': 'html,css,javascript,python,sql,react',
                'preferred': 'node.js,docker,aws,typescript,mongodb'
            },
            'devops engineer': {
                'required': 'linux,docker,kubernetes,ci/cd,git',
                'preferred': 'aws,terraform,jenkins,ansible,monitoring'
            }
        }
        
        role_lower = job_role.lower()
        default = default_patterns.get(role_lower, {
            'required': 'communication,problem solving,teamwork',
            'preferred': 'leadership,project management'
        })
        
        pattern = cls(
            job_role=role_lower,
            required_skills=default['required'],
            preferred_skills=default['preferred']
        )
        db.session.add(pattern)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
            # Try to get it again in case of race condition
            pattern = cls.get_by_role(job_role)
        
        return pattern
