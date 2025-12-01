"""
Resume Service for handling resume database operations.
"""

import json
import logging
from datetime import datetime
from typing import Optional, List, Dict, Any

from models import db
from models.resume import Resume, ResumeVersion
from models.resume_history import ResumeHistory


def convert_numpy_types(value):
    """
    Convert numpy types to Python native types for database compatibility.
    This prevents PostgreSQL errors like 'schema "np" does not exist'.
    
    Args:
        value: The value to convert (could be numpy type or Python native type)
        
    Returns:
        Python native type equivalent of the value
    """
    if value is None:
        return value
    
    # Check if value has .item() method (numpy scalars)
    if hasattr(value, 'item'):
        return value.item()
    
    # Check if value is a numpy ndarray
    if hasattr(value, 'tolist'):
        return value.tolist()
    
    # Handle specific numpy type names
    type_name = type(value).__name__
    if type_name.startswith(('float', 'int', 'uint', 'bool')):
        # Try to convert to Python native type
        if 'float' in type_name:
            return float(value)
        elif 'int' in type_name or 'uint' in type_name:
            return int(value)
        elif 'bool' in type_name:
            return bool(value)
    
    return value


class ResumeService:
    """Service for managing resume database operations."""
    
    @staticmethod
    def save_analysis(
        user_id: int,
        filename: str,
        analysis_results: Dict[str, Any],
        context: Dict[str, Any],
        raw_text: str = None,
        ats_data: Dict[str, Any] = None
    ) -> Resume:
        """
        Save complete resume analysis to database.
        
        Args:
            user_id: The user's ID
            filename: Original filename of the resume
            analysis_results: Dictionary containing analysis results
            context: Dictionary with experience_level, target_role, etc.
            raw_text: The extracted text from the resume
            ats_data: ATS analysis results
            
        Returns:
            Resume: The created Resume object
        """
        try:
            # Compute file hash if raw_text is provided
            file_hash = Resume.compute_file_hash(raw_text) if raw_text else None
            
            # Extract ATS score - use overall_score for consistency
            ats_score = ats_data.get('overall_score', 0) if ats_data else 0
            
            # Use ATS score as the primary resume score for consistency
            overall_score = ats_score if ats_score else analysis_results.get('quality_score', 0)
            
            # Build score breakdown from ATS data
            score_breakdown = None
            if ats_data:
                score_breakdown = {
                    'keyword_score': ats_data.get('keyword_analysis', {}).get('score', 0),
                    'section_score': ats_data.get('section_analysis', {}).get('score', 0),
                    'format_score': ats_data.get('format_analysis', {}).get('score', 0),
                }
            
            # Extract predictions
            predictions = analysis_results.get('predictions', [])
            predicted_career = predictions[0][0] if predictions else analysis_results.get('predicted_career')
            career_confidence = predictions[0][1] if predictions else analysis_results.get('confidence', 0)
            alternative_careers = predictions[1:4] if len(predictions) > 1 else []
            
            resume = Resume(
                user_id=user_id,
                filename=filename,
                file_hash=file_hash,
                experience_level=context.get('experience_level'),
                target_role=context.get('target_role'),
                job_search_status=context.get('job_search_status'),
                raw_text=raw_text,
                extracted_text=raw_text,  # Backward compatibility
                skills=analysis_results.get('skills', []),
                education=analysis_results.get('education'),
                experience=analysis_results.get('experience'),
                projects=analysis_results.get('projects'),
                certifications=analysis_results.get('certifications'),
                contact_info=analysis_results.get('contact_info'),
                overall_score=overall_score,
                ats_score=overall_score,  # Same as overall_score for consistency
                quality_score=overall_score,  # Backward compatibility
                score_breakdown=score_breakdown,
                ats_issues=ats_data.get('keyword_analysis', {}).get('missing', []) if ats_data else [],
                predicted_career=predicted_career,
                career_confidence=career_confidence,
                confidence_score=career_confidence,  # Backward compatibility
                alternative_careers=alternative_careers,
                feedback=analysis_results.get('improvements', []),
                missing_keywords=ats_data.get('keyword_analysis', {}).get('missing', []) if ats_data else [],
                salary_estimate=analysis_results.get('predicted_salary')
            )
            
            db.session.add(resume)
            db.session.commit()
            
            logging.info(f"Resume saved for user {user_id}: {filename}")
            return resume
            
        except Exception as e:
            logging.error(f"Error saving resume analysis: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_user_resumes(user_id: int, limit: int = 10) -> List[Resume]:
        """
        Get user's resume history.
        
        Args:
            user_id: The user's ID
            limit: Maximum number of resumes to return
            
        Returns:
            List of Resume objects
        """
        return Resume.query.filter_by(user_id=user_id)\
            .order_by(Resume.uploaded_at.desc())\
            .limit(limit)\
            .all()
    
    @staticmethod
    def get_resume_by_id(resume_id: int, user_id: int = None) -> Optional[Resume]:
        """
        Get specific resume with optional security check.
        
        Args:
            resume_id: The resume's ID
            user_id: Optional user ID for security check
            
        Returns:
            Resume object or None
        """
        query = Resume.query.filter_by(id=resume_id)
        if user_id is not None:
            query = query.filter_by(user_id=user_id)
        return query.first()
    
    @staticmethod
    def track_improvement(resume_id: int, new_scores: Dict[str, Any], changes: List[str]) -> ResumeVersion:
        """
        Track score improvements over time by creating a new version.
        
        Args:
            resume_id: The resume's ID
            new_scores: Dictionary with new scores
            changes: List of changes/improvements made
            
        Returns:
            ResumeVersion object
        """
        try:
            # Get current version number
            latest_version = ResumeVersion.query.filter_by(resume_id=resume_id)\
                .order_by(ResumeVersion.version.desc())\
                .first()
            
            new_version_number = (latest_version.version + 1) if latest_version else 1
            
            version = ResumeVersion(
                resume_id=resume_id,
                version=new_version_number,
                overall_score=new_scores.get('overall_score'),
                ats_score=new_scores.get('ats_score'),
                score_breakdown=new_scores.get('score_breakdown'),
                changes_made=changes
            )
            
            db.session.add(version)
            db.session.commit()
            
            return version
            
        except Exception as e:
            logging.error(f"Error tracking improvement: {e}")
            db.session.rollback()
            raise
    
    @staticmethod
    def get_improvement_history(resume_id: int) -> List[ResumeVersion]:
        """
        Get score progression for a resume.
        
        Args:
            resume_id: The resume's ID
            
        Returns:
            List of ResumeVersion objects
        """
        return ResumeVersion.query.filter_by(resume_id=resume_id)\
            .order_by(ResumeVersion.version.asc())\
            .all()
    
    @staticmethod
    def compare_resumes(resume_id_1: int, resume_id_2: int) -> Dict[str, Any]:
        """
        Compare two resume versions.
        
        Args:
            resume_id_1: First resume ID
            resume_id_2: Second resume ID
            
        Returns:
            Dictionary with comparison results
        """
        resume1 = Resume.query.get(resume_id_1)
        resume2 = Resume.query.get(resume_id_2)
        
        if not resume1 or not resume2:
            return {'error': 'One or both resumes not found'}
        
        return {
            'resume_1': {
                'id': resume1.id,
                'filename': resume1.filename,
                'overall_score': resume1.overall_score,
                'ats_score': resume1.ats_score,
                'skills': resume1.get_skills_list(),
                'uploaded_at': resume1.uploaded_at.isoformat() if resume1.uploaded_at else None
            },
            'resume_2': {
                'id': resume2.id,
                'filename': resume2.filename,
                'overall_score': resume2.overall_score,
                'ats_score': resume2.ats_score,
                'skills': resume2.get_skills_list(),
                'uploaded_at': resume2.uploaded_at.isoformat() if resume2.uploaded_at else None
            },
            'score_difference': (resume2.overall_score or 0) - (resume1.overall_score or 0),
            'ats_score_difference': (resume2.ats_score or 0) - (resume1.ats_score or 0),
            'skills_added': list(set(resume2.get_skills_list()) - set(resume1.get_skills_list())),
            'skills_removed': list(set(resume1.get_skills_list()) - set(resume2.get_skills_list()))
        }
    
    @staticmethod
    def get_user_stats(user_id: int) -> Dict[str, Any]:
        """
        Get aggregated statistics for a user.
        
        Args:
            user_id: The user's ID
            
        Returns:
            Dictionary with user statistics
        """
        resumes = Resume.query.filter_by(user_id=user_id)\
            .order_by(Resume.uploaded_at.desc())\
            .all()
        
        if not resumes:
            return {
                'total_resumes': 0,
                'latest_score': 0,
                'best_score': 0,
                'average_score': 0,
                'improvement': 0,
                'all_skills': [],
                'top_career': None
            }
        
        scores = [r.overall_score or 0 for r in resumes]
        all_skills = set()
        for r in resumes:
            all_skills.update(r.get_skills_list())
        
        latest = resumes[0]
        
        return {
            'total_resumes': len(resumes),
            'latest_score': latest.overall_score or 0,
            'best_score': max(scores) if scores else 0,
            'average_score': sum(scores) / len(scores) if scores else 0,
            'improvement': (resumes[0].overall_score or 0) - (resumes[1].overall_score or 0) if len(resumes) > 1 else 0,
            'all_skills': list(all_skills),
            'top_career': latest.predicted_career,
            'career_confidence': latest.career_confidence
        }
    
    @staticmethod
    def save_to_history(
        user_id: int,
        filename: str,
        overall_score: int,
        ats_data: Dict[str, Any],
        predictions: List,
        skills_found: List[str],
        skill_gap_data: Dict[str, Any],
        salary_data: Dict[str, Any],
        experience_level: str = None,
        target_role: str = None
    ) -> ResumeHistory:
        """
        Save resume analysis to history table.
        
        Args:
            user_id: The user's ID
            filename: Original filename
            overall_score: Resume quality score (same as ATS score)
            ats_data: ATS analysis results
            predictions: Career predictions
            skills_found: List of detected skills
            skill_gap_data: Skill gap analysis results
            salary_data: Salary prediction data
            experience_level: User's experience level
            target_role: User's target role
            
        Returns:
            ResumeHistory object
        """
        try:
            # Use ATS overall score for consistency (both overall_score and ats_score are the same)
            ats_score = ats_data.get('overall_score', overall_score) if ats_data else overall_score
            
            # Build score breakdown from ATS data
            keyword_score = ats_data.get('keyword_analysis', {}).get('score', 0) if ats_data else 0
            format_score = ats_data.get('format_analysis', {}).get('score', 0) if ats_data else 0
            section_score = ats_data.get('section_analysis', {}).get('score', 0) if ats_data else 0
            
            # Convert numpy types to Python native types for PostgreSQL compatibility
            ats_score = convert_numpy_types(ats_score)
            keyword_score = convert_numpy_types(keyword_score)
            format_score = convert_numpy_types(format_score)
            section_score = convert_numpy_types(section_score)
            
            # Convert career confidence from predictions
            career_confidence = 0
            if predictions and len(predictions) > 0:
                career_confidence = convert_numpy_types(predictions[0][1])
            
            # Convert salary data
            salary_min = convert_numpy_types(salary_data.get('min', 0)) if salary_data else 0
            salary_max = convert_numpy_types(salary_data.get('max', 0)) if salary_data else 0
            
            # Ensure all scores are integers
            ats_score = int(ats_score) if ats_score else 0
            keyword_score = int(keyword_score) if keyword_score else 0
            format_score = int(format_score) if format_score else 0
            section_score = int(section_score) if section_score else 0
            salary_min = int(salary_min) if salary_min else 0
            salary_max = int(salary_max) if salary_max else 0
            
            # Ensure career_confidence is a float
            career_confidence = float(career_confidence) if career_confidence else 0.0
            
            # Convert predictions for JSON serialization
            serializable_predictions = []
            if predictions:
                for career, conf in predictions[:3]:
                    serializable_predictions.append((career, float(convert_numpy_types(conf))))
            
            history_entry = ResumeHistory(
                user_id=user_id,
                filename=filename,
                experience_level=experience_level,
                target_role=target_role,
                overall_score=ats_score,
                ats_score=ats_score,
                keyword_score=keyword_score,
                format_score=format_score,
                section_score=section_score,
                predicted_career=predictions[0][0] if predictions else None,
                career_confidence=career_confidence,
                top_careers=json.dumps(serializable_predictions) if serializable_predictions else '[]',
                skills_detected=json.dumps(skills_found) if skills_found else '[]',
                skills_missing=json.dumps(
                    skill_gap_data.get("skills_analysis", {}).get("missing_required", [])
                ) if skill_gap_data else '[]',
                skill_count=len(skills_found) if skills_found else 0,
                predicted_salary_min=salary_min,
                predicted_salary_max=salary_max
            )
            
            db.session.add(history_entry)
            db.session.commit()
            
            logging.info(f"Resume history saved for user {user_id}: {filename}")
            return history_entry
            
        except Exception as e:
            logging.error(f"Error saving resume history: {e}")
            db.session.rollback()
            raise
