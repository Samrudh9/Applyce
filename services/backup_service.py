"""
Backup service for SkillFit Career Recommendation System.
Provides comprehensive data backup and restore functionality.
"""

import os
import json
import csv
import io
import logging
from datetime import datetime, timezone
from typing import Dict, List, Any, Optional, Tuple
from pathlib import Path

from models import db
from models.user import User
from models.feedback import Feedback
from models.skill_pattern import SkillPattern
from models.resume_history import ResumeHistory

logger = logging.getLogger(__name__)


class BackupService:
    """Service for handling data backup and restore operations."""
    
    VERSION = "1.0"
    BACKUP_DIR = "backups"
    
    @classmethod
    def _ensure_backup_dir(cls) -> Path:
        """Ensure backup directory exists and return its path."""
        backup_path = Path(cls.BACKUP_DIR)
        backup_path.mkdir(exist_ok=True)
        return backup_path
    
    @classmethod
    def _get_statistics(cls) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            total_users = User.query.count()
            total_feedback = Feedback.query.count()
            total_patterns = SkillPattern.query.count()
            total_resumes = ResumeHistory.query.count()
            positive_feedback = Feedback.query.filter_by(feedback_type='positive').count()
            negative_feedback = Feedback.query.filter_by(feedback_type='negative').count()
            
            return {
                "total_users": total_users,
                "total_feedback": total_feedback,
                "total_patterns": total_patterns,
                "total_resumes": total_resumes,
                "positive_feedback": positive_feedback,
                "negative_feedback": negative_feedback
            }
        except Exception as e:
            return {
                "total_users": 0,
                "total_feedback": 0,
                "total_patterns": 0,
                "total_resumes": 0,
                "positive_feedback": 0,
                "negative_feedback": 0,
                "error": str(e)
            }
    
    @classmethod
    def _export_skill_patterns(cls) -> List[Dict[str, Any]]:
        """Export all skill patterns - AI's learned knowledge (most valuable)."""
        patterns = []
        try:
            for pattern in SkillPattern.query.all():
                patterns.append({
                    "id": pattern.id,
                    "skill": pattern.skill,
                    "career": pattern.career,
                    "confidence": pattern.confidence,
                    "occurrence_count": pattern.occurrence_count,
                    "positive_feedback_count": pattern.positive_feedback_count,
                    "negative_feedback_count": pattern.negative_feedback_count,
                    "created_at": pattern.created_at.isoformat() if pattern.created_at else None,
                    "updated_at": pattern.updated_at.isoformat() if pattern.updated_at else None
                })
        except Exception as e:
            logger.warning(f"Error exporting skill patterns: {e}")
        return patterns
    
    @classmethod
    def _export_feedback(cls) -> List[Dict[str, Any]]:
        """Export all user feedback data."""
        feedbacks = []
        try:
            for feedback in Feedback.query.all():
                feedbacks.append({
                    "id": feedback.id,
                    "user_id": feedback.user_id,
                    "feedback_type": feedback.feedback_type,
                    "predicted_career": feedback.predicted_career,
                    "correct_career": feedback.correct_career,
                    "skills": feedback.skills,
                    "comments": feedback.comments,
                    "created_at": feedback.created_at.isoformat() if feedback.created_at else None
                })
        except Exception as e:
            logger.warning(f"Error exporting feedback: {e}")
        return feedbacks
    
    @classmethod
    def _export_users(cls) -> List[Dict[str, Any]]:
        """Export all users (without password hashes for security)."""
        users = []
        try:
            for user in User.query.all():
                users.append({
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                    "created_at": user.created_at.isoformat() if user.created_at else None,
                    "last_login": user.last_login.isoformat() if user.last_login else None,
                    "is_active": user.is_active
                })
        except Exception as e:
            logger.warning(f"Error exporting users: {e}")
        return users
    
    @classmethod
    def _export_resume_history(cls) -> List[Dict[str, Any]]:
        """Export all resume analysis history."""
        history = []
        try:
            for resume in ResumeHistory.query.all():
                history.append({
                    "id": resume.id,
                    "user_id": resume.user_id,
                    "filename": resume.filename,
                    "upload_date": resume.upload_date.isoformat() if resume.upload_date else None,
                    "overall_score": resume.overall_score,
                    "ats_score": resume.ats_score,
                    "predicted_career": resume.predicted_career,
                    "career_confidence": resume.career_confidence,
                    "skills_detected": resume.skills_detected,
                    "skill_count": resume.skill_count,
                    "experience_level": resume.experience_level,
                    "target_role": resume.target_role
                })
        except Exception as e:
            logger.warning(f"Error exporting resume history: {e}")
        return history
    
    @classmethod
    def export_all_data(cls) -> Dict[str, Any]:
        """Export all data as a dictionary."""
        return {
            "export_date": datetime.now(timezone.utc).isoformat(),
            "version": cls.VERSION,
            "statistics": cls._get_statistics(),
            "skill_patterns": cls._export_skill_patterns(),
            "feedback": cls._export_feedback(),
            "users": cls._export_users(),
            "resume_history": cls._export_resume_history()
        }
    
    @classmethod
    def save_backup_to_file(cls, filename: Optional[str] = None) -> Tuple[bool, str, Optional[str]]:
        """
        Save backup to a local JSON file.
        
        Args:
            filename: Optional custom filename. If not provided, auto-generated.
            
        Returns:
            Tuple of (success, message, filepath)
        """
        try:
            backup_dir = cls._ensure_backup_dir()
            
            if not filename:
                timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
                filename = f"skillfit_backup_{timestamp}.json"
            
            # Sanitize filename to prevent path traversal
            safe_filename = os.path.basename(filename)
            if not safe_filename.endswith('.json'):
                safe_filename += '.json'
            
            filepath = backup_dir / safe_filename
            
            data = cls.export_all_data()
            
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            
            return True, f"Backup saved successfully", str(filepath)
            
        except Exception as e:
            return False, f"Failed to save backup: {str(e)}", None
    
    @classmethod
    def export_skill_patterns_csv(cls) -> str:
        """Export skill patterns as CSV string."""
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Header
        writer.writerow([
            'id', 'skill', 'career', 'confidence', 'occurrence_count',
            'positive_feedback_count', 'negative_feedback_count',
            'created_at', 'updated_at'
        ])
        
        # Data rows
        for pattern in cls._export_skill_patterns():
            writer.writerow([
                pattern.get('id', ''),
                pattern.get('skill', ''),
                pattern.get('career', ''),
                pattern.get('confidence', ''),
                pattern.get('occurrence_count', ''),
                pattern.get('positive_feedback_count', ''),
                pattern.get('negative_feedback_count', ''),
                pattern.get('created_at', ''),
                pattern.get('updated_at', '')
            ])
        
        return output.getvalue()
    
    @classmethod
    def backup_to_github(cls, repo_url: str, token: str, 
                        branch: str = "backup") -> Tuple[bool, str]:
        """
        Push backup to a private GitHub repository.
        
        Note: This is a placeholder for future implementation.
        Requires GitHub API integration.
        
        Args:
            repo_url: GitHub repository URL
            token: GitHub personal access token
            branch: Branch name for backups
            
        Returns:
            Tuple of (success, message)
        """
        # Placeholder for GitHub backup functionality
        return False, "GitHub backup feature coming soon. Please use JSON download for now."
    
    @classmethod
    def backup_to_google_drive(cls, credentials: Dict) -> Tuple[bool, str]:
        """
        Upload backup to Google Drive.
        
        Note: This is a placeholder for future implementation.
        
        Args:
            credentials: Google Drive API credentials
            
        Returns:
            Tuple of (success, message)
        """
        # Placeholder for Google Drive backup functionality
        return False, "Google Drive backup feature coming soon. Please use JSON download for now."
    
    @classmethod
    def get_backup_status(cls) -> List[Dict[str, Any]]:
        """List available backups with metadata."""
        backups = []
        try:
            backup_dir = cls._ensure_backup_dir()
            
            for filepath in sorted(backup_dir.glob("*.json"), reverse=True):
                stat = filepath.stat()
                
                # Try to read metadata from file
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        stats = data.get('statistics', {})
                except Exception:
                    stats = {}
                
                backups.append({
                    "filename": filepath.name,
                    "size_bytes": stat.st_size,
                    "size_kb": round(stat.st_size / 1024, 1),
                    "created_at": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "patterns_count": stats.get('total_patterns', 0),
                    "feedback_count": stats.get('total_feedback', 0),
                    "users_count": stats.get('total_users', 0),
                    "resumes_count": stats.get('total_resumes', 0)
                })
        except Exception:
            pass
        
        return backups
    
    @classmethod
    def restore_from_backup(cls, filepath: str) -> Tuple[bool, str, Dict[str, int]]:
        """
        Restore data from backup JSON file.
        Uses merge strategy: Don't replace, merge with existing data.
        
        Args:
            filepath: Path to the backup JSON file
            
        Returns:
            Tuple of (success, message, stats)
        """
        stats = {
            "patterns_added": 0,
            "patterns_updated": 0,
            "feedback_added": 0,
            "feedback_skipped": 0
        }
        
        try:
            # Sanitize filepath to prevent path traversal
            backup_dir = cls._ensure_backup_dir()
            safe_filename = os.path.basename(filepath)
            full_path = backup_dir / safe_filename
            
            if not full_path.exists():
                return False, f"Backup file not found: {safe_filename}", stats
            
            with open(full_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Restore skill patterns (most important)
            patterns_data = data.get('skill_patterns', [])
            for pattern_data in patterns_data:
                skill = pattern_data.get('skill', '').lower()
                career = pattern_data.get('career', '').lower()
                
                if not skill or not career:
                    continue
                
                existing = SkillPattern.query.filter_by(
                    skill=skill, 
                    career=career
                ).first()
                
                if existing:
                    # Merge by taking MAX values
                    existing.occurrence_count = max(
                        existing.occurrence_count or 0,
                        pattern_data.get('occurrence_count', 0)
                    )
                    existing.positive_feedback_count = max(
                        existing.positive_feedback_count or 0,
                        pattern_data.get('positive_feedback_count', 0)
                    )
                    existing.negative_feedback_count = max(
                        existing.negative_feedback_count or 0,
                        pattern_data.get('negative_feedback_count', 0)
                    )
                    existing.confidence = max(
                        existing.confidence or 0,
                        pattern_data.get('confidence', 0)
                    )
                    stats["patterns_updated"] += 1
                else:
                    # Create new pattern
                    new_pattern = SkillPattern(
                        skill=skill,
                        career=career,
                        occurrence_count=pattern_data.get('occurrence_count', 1),
                        positive_feedback_count=pattern_data.get('positive_feedback_count', 0),
                        negative_feedback_count=pattern_data.get('negative_feedback_count', 0),
                        confidence=pattern_data.get('confidence', 0.5)
                    )
                    db.session.add(new_pattern)
                    stats["patterns_added"] += 1
            
            # Restore feedback (skip duplicates by ID)
            feedback_data = data.get('feedback', [])
            existing_feedback_ids = {f.id for f in Feedback.query.all()}
            
            for fb_data in feedback_data:
                fb_id = fb_data.get('id')
                if fb_id and fb_id in existing_feedback_ids:
                    stats["feedback_skipped"] += 1
                    continue
                
                # Check for duplicate by content
                existing_by_content = Feedback.query.filter_by(
                    user_id=fb_data.get('user_id'),
                    feedback_type=fb_data.get('feedback_type'),
                    predicted_career=fb_data.get('predicted_career'),
                    skills=fb_data.get('skills')
                ).first()
                
                if existing_by_content:
                    stats["feedback_skipped"] += 1
                    continue
                
                new_feedback = Feedback(
                    user_id=fb_data.get('user_id'),
                    feedback_type=fb_data.get('feedback_type'),
                    predicted_career=fb_data.get('predicted_career'),
                    correct_career=fb_data.get('correct_career'),
                    skills=fb_data.get('skills'),
                    comments=fb_data.get('comments')
                )
                db.session.add(new_feedback)
                stats["feedback_added"] += 1
            
            db.session.commit()
            
            total_changes = (
                stats["patterns_added"] + 
                stats["patterns_updated"] + 
                stats["feedback_added"]
            )
            
            return True, f"Restore completed. {total_changes} changes applied.", stats
            
        except json.JSONDecodeError:
            return False, "Invalid backup file format", stats
        except Exception as e:
            db.session.rollback()
            return False, f"Restore failed: {str(e)}", stats
    
    @classmethod
    def get_backup_file_content(cls, filename: str) -> Optional[bytes]:
        """
        Get the content of a backup file for download.
        
        Args:
            filename: Name of the backup file
            
        Returns:
            File content as bytes, or None if not found
        """
        try:
            backup_dir = cls._ensure_backup_dir()
            # Sanitize filename to prevent path traversal
            safe_filename = os.path.basename(filename)
            filepath = backup_dir / safe_filename
            
            if filepath.exists() and filepath.suffix == '.json':
                with open(filepath, 'rb') as f:
                    return f.read()
        except Exception:
            pass
        
        return None
    
    @classmethod
    def delete_backup(cls, filename: str) -> Tuple[bool, str]:
        """
        Delete a backup file.
        
        Args:
            filename: Name of the backup file to delete
            
        Returns:
            Tuple of (success, message)
        """
        try:
            backup_dir = cls._ensure_backup_dir()
            # Sanitize filename to prevent path traversal
            safe_filename = os.path.basename(filename)
            filepath = backup_dir / safe_filename
            
            if not filepath.exists():
                return False, "Backup file not found"
            
            if filepath.suffix != '.json':
                return False, "Invalid file type"
            
            filepath.unlink()
            return True, "Backup deleted successfully"
            
        except Exception as e:
            return False, f"Failed to delete backup: {str(e)}"
