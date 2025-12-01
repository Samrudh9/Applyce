"""
Career Recommendation Demo - Resume Parser Package

A comprehensive resume parsing and career recommendation system.
"""

__version__ = "1.0.0"
__author__ = "Career Recommendation Team"

# Core parsing functionality
from .resume_parser import (
    parse_resume_atomic,
    extract_text_from_file,
    extract_name_from_docx_robust,
    extract_projects_github_aware
)

# Configuration and utilities
from .config import config
from .utils.validators import FileValidator, TextValidator
from .utils.error_handler import ErrorHandler, ResumeParsingException

# ML components (conditional imports to handle missing dependencies)
try:
    from .ml_resume_classifier import MLResumeClassifier
except ImportError:
    MLResumeClassifier = None

try:
    from .quality_checker import QualityChecker
except ImportError:
    QualityChecker = None

__all__ = [
    'parse_resume_atomic',
    'extract_text_from_file', 
    'extract_name_from_docx_robust',
    'extract_projects_github_aware',
    'config',
    'FileValidator',
    'TextValidator', 
    'ErrorHandler',
    'ResumeParsingException',
    'MLResumeClassifier',
    'QualityChecker'
]

# Version check for critical dependencies
def check_dependencies():
    """Check if critical dependencies are available"""
    missing = []
    
    try:
        import docx
    except ImportError:
        missing.append('python-docx')
    
    try:
        import magic
    except ImportError:
        missing.append('python-magic')
    
    if missing:
        import warnings
        warnings.warn(f"Missing optional dependencies: {missing}")
    
    return len(missing) == 0

# Initialize dependency check
check_dependencies()
