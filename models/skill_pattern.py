"""
SkillPattern model for self-learning functionality.
"""

from datetime import datetime
from models import db


class SkillPattern(db.Model):
    """SkillPattern model for tracking skill-to-career patterns and learning."""
    
    __tablename__ = 'skill_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Skill-Career association
    skill = db.Column(db.String(100), nullable=False, index=True)
    career = db.Column(db.String(100), nullable=False, index=True)
    
    # Learning metrics
    occurrence_count = db.Column(db.Integer, default=1)
    positive_feedback_count = db.Column(db.Integer, default=0)
    negative_feedback_count = db.Column(db.Integer, default=0)
    confidence = db.Column(db.Float, default=0.5)  # 0.0 to 1.0
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Composite unique constraint
    __table_args__ = (
        db.UniqueConstraint('skill', 'career', name='unique_skill_career'),
    )
    
    def __repr__(self):
        return f'<SkillPattern {self.skill} -> {self.career} ({self.confidence:.2f})>'
    
    def record_positive_feedback(self):
        """Record positive feedback and update confidence."""
        self.positive_feedback_count += 1
        self._update_confidence()
    
    def record_negative_feedback(self):
        """Record negative feedback and update confidence."""
        self.negative_feedback_count += 1
        self._update_confidence()
    
    def increment_occurrence(self):
        """Increment occurrence count when pattern is observed."""
        self.occurrence_count += 1
        self.updated_at = datetime.utcnow()
    
    def _update_confidence(self):
        """
        Update confidence score based on feedback.
        Uses Bayesian-like update: more feedback = more certainty
        """
        total_feedback = self.positive_feedback_count + self.negative_feedback_count
        
        if total_feedback == 0:
            # No feedback yet, use base confidence
            self.confidence = 0.5
        else:
            # Calculate confidence based on feedback ratio
            # Add smoothing to avoid extreme values
            alpha = self.positive_feedback_count + 1  # Prior for positive
            beta = self.negative_feedback_count + 1   # Prior for negative
            self.confidence = alpha / (alpha + beta)
        
        self.updated_at = datetime.utcnow()
    
    @classmethod
    def get_or_create(cls, skill, career):
        """Get existing pattern or create new one."""
        pattern = cls.query.filter_by(skill=skill.lower(), career=career.lower()).first()
        if not pattern:
            pattern = cls(skill=skill.lower(), career=career.lower())
            db.session.add(pattern)
            db.session.commit()
        return pattern
    
    @classmethod
    def get_career_confidence(cls, skills, career):
        """
        Calculate overall confidence for a career based on skills.
        Returns weighted average confidence.
        """
        if not skills:
            return 0.0
        
        patterns = cls.query.filter(
            cls.skill.in_([s.lower() for s in skills]),
            cls.career == career.lower()
        ).all()
        
        if not patterns:
            return 0.5  # Default confidence for unknown patterns
        
        # Weight by occurrence count
        total_weight = sum(p.occurrence_count for p in patterns)
        if total_weight == 0:
            return 0.5
        
        weighted_confidence = sum(
            p.confidence * p.occurrence_count for p in patterns
        ) / total_weight
        
        return weighted_confidence
