import os
import re
import magic
from pathlib import Path
from typing import Optional, List, Tuple
from werkzeug.datastructures import FileStorage
from config import config

class ValidationError(Exception):
    """Custom validation error"""
    pass

class FileValidator:
    """Handles file upload validation and sanitization"""
    
    SAFE_FILENAME_PATTERN = re.compile(r'^[a-zA-Z0-9._-]+$')
    
    @staticmethod
    def validate_file_upload(file: FileStorage) -> Tuple[bool, str]:
        """Comprehensive file validation"""
        try:
            # Check if file exists
            if not file or not file.filename:
                return False, "No file provided"
            
            # Validate filename
            if not FileValidator._is_safe_filename(file.filename):
                return False, "Invalid filename characters"
            
            # Check file extension
            if not FileValidator._is_allowed_extension(file.filename):
                return False, f"File type not allowed. Allowed: {config.security.allowed_extensions}"
            
            # Check file size
            if not FileValidator._is_valid_size(file):
                return False, f"File too large. Max size: {config.security.max_file_size_mb}MB"
            
            # Validate MIME type
            if not FileValidator._is_valid_mime_type(file):
                return False, "Invalid file type detected"
            
            return True, "File is valid"
            
        except Exception as e:
            return False, f"Validation error: {str(e)}"
    
    @staticmethod
    def _is_safe_filename(filename: str) -> bool:
        """Check if filename contains only safe characters"""
        # Remove path traversal attempts
        if '..' in filename or '/' in filename or '\\' in filename:
            return False
        
        # Check for safe characters
        name = Path(filename).stem
        return bool(FileValidator.SAFE_FILENAME_PATTERN.match(name)) and len(name) <= 100
    
    @staticmethod
    def _is_allowed_extension(filename: str) -> bool:
        """Check if file extension is allowed"""
        ext = Path(filename).suffix.lower()
        return ext in config.security.allowed_extensions
    
    @staticmethod
    def _is_valid_size(file: FileStorage) -> bool:
        """Check if file size is within limits"""
        try:
            # Seek to end to get size
            file.seek(0, os.SEEK_END)
            size = file.tell()
            file.seek(0)  # Reset position
            
            max_size = config.security.max_file_size_mb * 1024 * 1024
            return size <= max_size
        except:
            return False
    
    @staticmethod
    def _is_valid_mime_type(file: FileStorage) -> bool:
        """Validate MIME type using python-magic"""
        try:
            # Read first 1024 bytes for MIME detection
            file.seek(0)
            header = file.read(1024)
            file.seek(0)
            
            mime_type = magic.from_buffer(header, mime=True)
            
            allowed_mimes = {
                'application/pdf',
                'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                'application/msword',
                'text/plain'
            }
            
            return mime_type in allowed_mimes
        except:
            return False

class TextValidator:
    """Validates and sanitizes text input"""
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = 10000) -> str:
        """Sanitize text input"""
        if not text:
            return ""
        
        # Remove control characters except whitespace
        sanitized = ''.join(char for char in text if ord(char) >= 32 or char in '\t\n\r')
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
    
    @staticmethod
    def validate_email(email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email)) if email else False
    
    @staticmethod
    def validate_url(url: str) -> bool:
        """Validate URL format"""
        pattern = r'^https?://(?:[-\w.])+(?:\:[0-9]+)?(?:/(?:[\w/_.])*(?:\?(?:[\w&=%.])*)?(?:\#(?:[\w.])*)?)?$'
        return bool(re.match(pattern, url)) if url else False
