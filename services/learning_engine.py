"""
Self-learning engine for improving career predictions over time.
"""

from models import db
from models.skill_pattern import SkillPattern
from models.feedback import Feedback
from models.career import Career


class LearningEngine:
    """
    Self-learning engine that improves predictions based on user feedback.
    
    The engine:
    1. Tracks skill->career associations
    2. Updates confidence scores based on feedback
    3. Provides adjusted predictions based on learned patterns
    """
    
    @staticmethod
    def record_prediction(skills, predicted_career, confidence):
        """
        Record a prediction to build pattern knowledge.
        
        Args:
            skills: List of skills used in prediction
            predicted_career: The predicted career
            confidence: Original model confidence
        """
        for skill in skills:
            pattern = SkillPattern.get_or_create(skill, predicted_career)
            pattern.increment_occurrence()
        
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()
    
    @staticmethod
    def get_adjusted_confidence(skills, career, base_confidence):
        """
        Get adjusted confidence based on learned patterns.
        
        Args:
            skills: List of skills
            career: Career being evaluated
            base_confidence: Original model confidence
            
        Returns:
            float: Adjusted confidence score (0-100)
        """
        if not skills:
            return base_confidence
        
        # Get pattern-based confidence
        pattern_confidence = SkillPattern.get_career_confidence(skills, career)
        
        # Count how much feedback we have for this career
        feedback_count = Feedback.query.filter_by(predicted_career=career).count()
        
        # Weight based on amount of feedback data
        # More feedback = more trust in learned patterns
        if feedback_count == 0:
            # No feedback yet, use base confidence
            return base_confidence
        elif feedback_count < 10:
            # Little feedback, slightly adjust
            weight = 0.1 * feedback_count  # 0.1 to 0.9
            adjusted = (1 - weight) * base_confidence + weight * (pattern_confidence * 100)
        else:
            # Significant feedback, weight patterns more
            weight = min(0.5, 0.1 + 0.04 * feedback_count)  # Max 50% weight
            adjusted = (1 - weight) * base_confidence + weight * (pattern_confidence * 100)
        
        return round(adjusted, 2)
    
    @staticmethod
    def get_skill_career_insights(skill):
        """
        Get insights about which careers a skill maps to.
        
        Args:
            skill: The skill to analyze
            
        Returns:
            list: List of (career, confidence) tuples
        """
        patterns = SkillPattern.query.filter_by(
            skill=skill.lower()
        ).order_by(SkillPattern.confidence.desc()).all()
        
        return [(p.career, round(p.confidence * 100, 1)) for p in patterns]
    
    @staticmethod
    def get_career_skill_requirements(career):
        """
        Get learned skill requirements for a career.
        
        Args:
            career: Career name
            
        Returns:
            list: List of (skill, confidence) tuples
        """
        patterns = SkillPattern.query.filter_by(
            career=career.lower()
        ).order_by(SkillPattern.confidence.desc()).all()
        
        return [(p.skill, round(p.confidence * 100, 1)) for p in patterns]
    
    @staticmethod
    def get_top_patterns(limit=20):
        """
        Get top skill-career patterns by confidence.
        
        Returns:
            list: List of SkillPattern objects
        """
        return SkillPattern.query.filter(
            SkillPattern.occurrence_count > 0
        ).order_by(
            SkillPattern.confidence.desc()
        ).limit(limit).all()
    
    @staticmethod
    def get_learning_stats():
        """
        Get overall learning statistics.
        
        Returns:
            dict: Statistics about the learning engine
        """
        total_patterns = SkillPattern.query.count()
        total_feedback = Feedback.query.count()
        
        # Get average confidence using database aggregate function
        avg_result = db.session.query(db.func.avg(SkillPattern.confidence)).scalar()
        avg_confidence = avg_result if avg_result is not None else 0.5
        
        # Get most learned skills (highest occurrence)
        top_skills = db.session.query(
            SkillPattern.skill,
            db.func.sum(SkillPattern.occurrence_count).label('total')
        ).group_by(SkillPattern.skill).order_by(
            db.func.sum(SkillPattern.occurrence_count).desc()
        ).limit(10).all()
        
        return {
            'total_patterns': total_patterns,
            'total_feedback': total_feedback,
            'average_confidence': round(avg_confidence * 100, 1),
            'top_learned_skills': [{'skill': s, 'occurrences': t} for s, t in top_skills]
        }
    
    @staticmethod
    def adjust_predictions(predictions, skills):
        """
        Adjust a list of career predictions based on learned patterns.
        
        Args:
            predictions: List of (career, confidence) tuples
            skills: List of skills used in prediction
            
        Returns:
            list: Adjusted predictions sorted by confidence
        """
        adjusted = []
        for career, confidence in predictions:
            new_confidence = LearningEngine.get_adjusted_confidence(
                skills, career, confidence
            )
            adjusted.append((career, new_confidence))
        
        # Re-sort by adjusted confidence
        adjusted.sort(key=lambda x: x[1], reverse=True)
        return adjusted
