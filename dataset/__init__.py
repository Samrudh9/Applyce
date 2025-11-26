# Dataset module initialization
# Contains career-related data for the recommendation system

from .roadmaps import get_career_roadmap, CAREER_ROADMAPS
from .skills import CAREER_SKILLS
from .career_descriptions import CAREER_DESCRIPTIONS
from .salary_data import SALARY_DATA

__all__ = [
    'get_career_roadmap',
    'CAREER_ROADMAPS',
    'CAREER_SKILLS',
    'CAREER_DESCRIPTIONS',
    'SALARY_DATA'
]
