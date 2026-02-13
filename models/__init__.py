"""
Database models for SkillFit Career Recommendation System.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import all models after db is defined
from models.user import User
from models.resume import Resume, ResumeVersion
from models.feedback import Feedback
from models.career import Career
from models.admin import Admin
from models.skill_pattern import SkillPattern
from models.resume_history import ResumeHistory
from models.user_preferences import UserPreferences
from models.job_pattern import JobPattern
from models.oauth_account import OAuthAccount

__all__ = [
    'db', 
    'User', 
    'Resume', 
    'ResumeVersion',
    'Feedback', 
    'Career', 
    'SkillPattern', 
    'ResumeHistory',
    'UserPreferences',
    'JobPattern',
    'OAuthAccount'
]
