"""
Database models for SkillFit Career Recommendation System.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models after db is defined
from models.user import User
from models.resume import Resume
from models.feedback import Feedback
from models.career import Career
from models.skill_pattern import SkillPattern
from models.resume_history import ResumeHistory

__all__ = ['db', 'User', 'Resume', 'Feedback', 'Career', 'SkillPattern', 'ResumeHistory']
