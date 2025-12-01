import os
import logging
from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path

@dataclass
class SecurityConfig:
    """Security configuration settings"""
    max_file_size_mb: int = 10
    allowed_extensions: set = None
    csrf_token_expires: int = 3600
    
    def __post_init__(self):
        if self.allowed_extensions is None:
            self.allowed_extensions = {'.pdf', '.docx', '.doc', '.txt'}

@dataclass
class ParsingConfig:
    """Resume parsing configuration"""
    confidence_threshold: float = 0.7
    max_memory_mb: int = 500
    timeout_seconds: int = 30
    enable_pdf_parsing: bool = True

class Config:
    """Main configuration class with environment-based settings"""
    
    def __init__(self, env: str = None):
        self.env = env or os.getenv('FLASK_ENV', 'development')
        self.base_dir = Path(__file__).parent
        self._load_config()
    
    def _load_config(self):
        """Load configuration based on environment"""
        # Base configuration
        self.SECRET_KEY = os.getenv('SECRET_KEY', self._generate_secret_key())
        self.DEBUG = self.env == 'development'
        
        # Database
        self.DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///resume_parser.db')
        
        # API Keys (from environment only)
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN')
        
        # Security settings
        self.security = SecurityConfig()
        
        # Parsing settings
        self.parsing = ParsingConfig()
        
        # Logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # Feature flags
        self.ROADMAP_SUPPORT = os.getenv('ROADMAP_SUPPORT', 'true').lower() == 'true'
        self.ML_CLASSIFIER_ENABLED = os.getenv('ML_CLASSIFIER_ENABLED', 'false').lower() == 'true'
        self.GITHUB_INTEGRATION_ENABLED = os.getenv('GITHUB_INTEGRATION_ENABLED', 'false').lower() == 'true'
        
        # Admin credentials for backup access
        # Set these environment variables for production security
        # Example: ADMIN_ID=myadmin, ADMIN_PASSWORD=mysecurepassword
        self.ADMIN_ID = os.getenv('ADMIN_ID', 'admin')
        self.ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'skillfit2024')
        
        # File upload settings
        self.UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', self.base_dir / 'uploads')
        self.MAX_CONTENT_LENGTH = self.security.max_file_size_mb * 1024 * 1024
        
        self._validate_config()
    
    def _generate_secret_key(self) -> str:
        """Generate a secure secret key if none provided"""
        if self.env == 'production':
            raise ValueError("SECRET_KEY must be set in production environment")
        return os.urandom(24).hex()
    
    def _validate_config(self):
        """Validate critical configuration"""
        if self.env == 'production':
            required_vars = ['SECRET_KEY', 'DATABASE_URL']
            missing = [var for var in required_vars if not getattr(self, var, None)]
            if missing:
                raise ValueError(f"Missing required environment variables: {missing}")
    
    def get_api_key(self, service: str) -> str:
        """Safely get API key for a service"""
        key_map = {
            'openai': self.OPENAI_API_KEY,
            'github': self.GITHUB_API_TOKEN
        }
        
        key = key_map.get(service.lower())
        if not key:
            logging.warning(f"API key for {service} not configured")
        return key

    def get(self, key: str, default=None):
        """Get configuration value with default fallback"""
        return getattr(self, key, default)

# Global config instance
config = Config()
