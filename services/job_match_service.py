"""
Job Match Service - Calculates job fit score and skill gaps.
"""

import re
import logging
from typing import Dict, List, Optional, Tuple
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

logger = logging.getLogger(__name__)


class JobMatchService:
    """
    Service to match resume skills with job descriptions.
    Calculates job fit percentage and identifies skill gaps.
    """
    
    # Common tech and soft skills for extraction
    SKILL_KEYWORDS = [
        'python', 'java', 'javascript', 'typescript', 'react', 'angular', 'vue', 
        'nodejs', 'node.js', 'html', 'css', 'sql', 'mongodb', 'postgresql', 
        'git', 'docker', 'kubernetes', 'aws', 'azure', 'gcp', 'machine learning', 
        'ml', 'ai', 'deep learning', 'data science', 'tensorflow', 'pytorch',
        'django', 'flask', 'spring', 'express', 'rest', 'api', 'graphql',
        'agile', 'scrum', 'ci/cd', 'jenkins', 'linux', 'bash', 'devops',
        'frontend', 'backend', 'full stack', 'mobile', 'android', 'ios',
        'swift', 'kotlin', 'flutter', 'react native', 'figma', 'ui/ux',
        'communication', 'leadership', 'teamwork', 'problem solving',
        'project management', 'analytical', 'critical thinking'
    ]
    
    def __init__(self):
        """Initialize the job match service."""
        self._compile_patterns()
    
    def _compile_patterns(self):
        """Compile regex patterns for skill extraction."""
        # Create pattern for skill matching - sort by length (longest first) to match multi-word skills first
        sorted_skills = sorted(self.SKILL_KEYWORDS, key=len, reverse=True)
        escaped_skills = [re.escape(skill) for skill in sorted_skills]
        pattern = r'\b(' + '|'.join(escaped_skills) + r')\b'
        self._skill_pattern = re.compile(pattern, re.IGNORECASE)
    
    def extract_skills_from_text(self, text: str) -> List[str]:
        """
        Extract skills from text using pattern matching.
        
        Args:
            text: Resume or job description text
            
        Returns:
            List of detected skills (lowercase, deduplicated)
        """
        if not text:
            return []
        
        text_lower = text.lower()
        matches = self._skill_pattern.findall(text_lower)
        
        # Deduplicate and normalize
        skills = list(set(match.strip() for match in matches))
        
        return sorted(skills)
    
    def calculate_semantic_similarity(self, text1: str, text2: str) -> float:
        """
        Calculate semantic similarity between two texts using TF-IDF and cosine similarity.
        
        Args:
            text1: First text (e.g., resume)
            text2: Second text (e.g., job description)
            
        Returns:
            Similarity score between 0 and 1
        """
        if not text1 or not text2:
            logger.warning("Empty text provided for semantic similarity calculation")
            return 0.0
        
        try:
            vectorizer = TfidfVectorizer(
                lowercase=True,
                stop_words='english',
                ngram_range=(1, 2),
                max_features=500
            )
            
            tfidf_matrix = vectorizer.fit_transform([text1, text2])
            similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
            
            return float(similarity)
        except Exception as e:
            logger.error(f"Semantic similarity calculation error: {e}. Text1 length: {len(text1)}, Text2 length: {len(text2)}")
            return 0.0
    
    def parse_skills_input(self, skills_input: str) -> List[str]:
        """
        Parse skills from various input formats.
        
        Args:
            skills_input: Skills as comma-separated string, JSON, etc.
            
        Returns:
            List of skills
        """
        if not skills_input:
            return []
        
        # Handle comma-separated
        if ',' in skills_input:
            skills = [s.strip().lower() for s in skills_input.split(',')]
            return [s for s in skills if s]
        
        # Handle space-separated
        skills = [s.strip().lower() for s in skills_input.split()]
        return [s for s in skills if s and len(s) > 1]
    
    def calculate_job_match(
        self,
        resume_skills: List[str],
        job_description: str,
        required_skills: Optional[List[str]] = None,
        preferred_skills: Optional[List[str]] = None
    ) -> Dict:
        """
        Calculate comprehensive job match score.
        
        Args:
            resume_skills: List of skills from resume
            job_description: Full job description text
            required_skills: List of required skills (optional)
            preferred_skills: List of preferred skills (optional)
            
        Returns:
            Dictionary with match results
        """
        # Normalize resume skills
        resume_skills_normalized = [s.lower().strip() for s in resume_skills]
        
        # Extract skills from job description if not provided
        if not required_skills and not preferred_skills:
            jd_skills = self.extract_skills_from_text(job_description)
            # Split 60/40 between required and preferred
            split_point = int(len(jd_skills) * 0.6)
            required_skills = jd_skills[:split_point] if split_point > 0 else jd_skills
            preferred_skills = jd_skills[split_point:] if split_point > 0 else []
        else:
            # Normalize provided skills
            required_skills = [s.lower().strip() for s in (required_skills or [])]
            preferred_skills = [s.lower().strip() for s in (preferred_skills or [])]
        
        # Calculate matches
        required_matched = list(set(resume_skills_normalized) & set(required_skills))
        preferred_matched = list(set(resume_skills_normalized) & set(preferred_skills))
        
        # Calculate missing skills
        missing_required = list(set(required_skills) - set(resume_skills_normalized))
        missing_preferred = list(set(preferred_skills) - set(resume_skills_normalized))
        
        # Calculate match percentage with weighted scoring
        # Required skills: 70% weight, Preferred skills: 30% weight
        total_required = len(required_skills) if required_skills else 0
        total_preferred = len(preferred_skills) if preferred_skills else 0
        
        if total_required == 0 and total_preferred == 0:
            # No skills specified, use semantic similarity
            semantic_score = self.calculate_semantic_similarity(
                ' '.join(resume_skills_normalized),
                job_description
            )
            match_percentage = round(semantic_score * 100, 1)
        else:
            # Calculate weighted score
            required_score = (len(required_matched) / total_required * 100) if total_required > 0 else 100
            preferred_score = (len(preferred_matched) / total_preferred * 100) if total_preferred > 0 else 100
            
            # Weight: 70% required, 30% preferred
            if total_required > 0 and total_preferred > 0:
                match_percentage = round(required_score * 0.7 + preferred_score * 0.3, 1)
            elif total_required > 0:
                match_percentage = round(required_score, 1)
            else:
                match_percentage = round(preferred_score, 1)
        
        # Calculate semantic similarity for additional context
        semantic_similarity = self.calculate_semantic_similarity(
            ' '.join(resume_skills_normalized),
            job_description
        )
        
        return {
            'match_percentage': match_percentage,
            'semantic_similarity': round(semantic_similarity * 100, 1),
            'required_matched': sorted(required_matched),
            'preferred_matched': sorted(preferred_matched),
            'missing_required': sorted(missing_required),
            'missing_preferred': sorted(missing_preferred),
            'total_resume_skills': len(resume_skills_normalized),
            'total_required_skills': total_required,
            'total_preferred_skills': total_preferred,
            'recommendation': self._get_recommendation(match_percentage)
        }
    
    def _get_recommendation(self, match_percentage: float) -> str:
        """Get recommendation based on match percentage."""
        if match_percentage >= 80:
            return "Excellent match! You meet most requirements."
        elif match_percentage >= 60:
            return "Good match. Consider applying and highlighting relevant experience."
        elif match_percentage >= 40:
            return "Moderate match. Focus on learning missing skills before applying."
        else:
            return "Low match. Significant skill gaps exist. Consider other roles or upskilling."


# Singleton instance
job_match_service = JobMatchService()
