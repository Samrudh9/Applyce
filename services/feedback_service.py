"""
Feedback service for processing and storing user feedback.
"""

import json
from models import db
from models.feedback import Feedback
from models.skill_pattern import SkillPattern


class FeedbackService:
    """Service for handling user feedback on career predictions."""
    
    @staticmethod
    def record_feedback(feedback_type, predicted_career, skills=None, 
                       correct_career=None, user_id=None, resume_id=None, 
                       comments=None):
        """
        Record user feedback on a career prediction.
        
        Args:
            feedback_type: 'positive' or 'negative'
            predicted_career: The career that was predicted
            skills: List of skills used in prediction
            correct_career: User's correction (for negative feedback)
            user_id: Optional user ID
            resume_id: Optional resume ID
            comments: Optional user comments
            
        Returns:
            tuple: (success: bool, message: str)
        """
        try:
            # Create feedback record
            feedback = Feedback(
                user_id=user_id,
                resume_id=resume_id,
                feedback_type=feedback_type,
                predicted_career=predicted_career,
                correct_career=correct_career,
                skills=json.dumps(skills) if skills else None,
                comments=comments
            )
            db.session.add(feedback)
            
            # Update skill patterns for learning
            if skills:
                FeedbackService._update_skill_patterns(
                    skills=skills,
                    predicted_career=predicted_career,
                    correct_career=correct_career,
                    is_positive=(feedback_type == 'positive')
                )
            
            db.session.commit()
            return True, "Feedback recorded successfully"
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to record feedback: {str(e)}"
    
    @staticmethod
    def _update_skill_patterns(skills, predicted_career, correct_career, is_positive):
        """
        Update skill patterns based on feedback.
        
        For positive feedback: Reinforce skill->predicted_career patterns
        For negative feedback: Weaken skill->predicted_career, strengthen skill->correct_career
        """
        for skill in skills:
            # Update pattern for predicted career
            pattern = SkillPattern.get_or_create(skill, predicted_career)
            pattern.increment_occurrence()
            
            if is_positive:
                pattern.record_positive_feedback()
            else:
                pattern.record_negative_feedback()
                
                # If user provided correction, strengthen that pattern
                if correct_career:
                    correct_pattern = SkillPattern.get_or_create(skill, correct_career)
                    correct_pattern.increment_occurrence()
                    correct_pattern.record_positive_feedback()
    
    @staticmethod
    def get_feedback_stats():
        """Get overall feedback statistics."""
        total = Feedback.query.count()
        positive = Feedback.query.filter_by(feedback_type='positive').count()
        negative = Feedback.query.filter_by(feedback_type='negative').count()
        
        return {
            'total': total,
            'positive': positive,
            'negative': negative,
            'positive_rate': (positive / total * 100) if total > 0 else 0
        }
    
    @staticmethod
    def get_recent_feedback(limit=10):
        """Get recent feedback entries."""
        return Feedback.query.order_by(
            Feedback.created_at.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_feedback_for_career(career):
        """Get feedback statistics for a specific career."""
        feedbacks = Feedback.query.filter_by(predicted_career=career).all()
        
        if not feedbacks:
            return {'total': 0, 'positive': 0, 'negative': 0, 'accuracy': 0}
        
        positive = sum(1 for f in feedbacks if f.is_positive())
        negative = len(feedbacks) - positive
        
        return {
            'total': len(feedbacks),
            'positive': positive,
            'negative': negative,
            'accuracy': (positive / len(feedbacks) * 100) if feedbacks else 0
        }
