"""
Configuration module for SkillFit.
Loads environment variables safely from .env file (local) or system environment (production).
"""

import os
import logging
from typing import Dict, Any
from dataclasses import dataclass
from pathlib import Path
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

# Try to load .env file for local development
try:
    from dotenv import load_dotenv
    env_path = Path('.') / '.env'
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
except ImportError:
    pass  # python-dotenv not installed, use system env vars

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
        self.BASE_URL = os.getenv('BASE_URL', 'http://localhost:5000')
        
        # Database
        self.DATABASE_URL = self._normalize_database_url(os.getenv('DATABASE_URL', ''))
        self.SQLALCHEMY_DATABASE_URI = self.DATABASE_URL if self.DATABASE_URL else 'sqlite:///skillfit.db'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = False
        self.SQLALCHEMY_ENGINE_OPTIONS = self._engine_options(self.SQLALCHEMY_DATABASE_URI)
        
        # Admin credentials - MUST be set via environment variables in production
        self.ADMIN_ID = os.getenv('ADMIN_ID', 'admin@skillfit.com')
        self.ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'changeme')
        
        # Legacy admin credentials support (deprecated)
        self.ADMIN_CREDENTIALS_RAW = os.getenv('ADMIN_CREDENTIALS', '')
        
        # Job Search APIs
        self.ADZUNA_APP_ID = os.getenv('ADZUNA_APP_ID', '')
        self.ADZUNA_API_KEY = os.getenv('ADZUNA_API_KEY', '')
        self.RAPIDAPI_KEY = os.getenv('RAPIDAPI_KEY', '')
        
        # Email (Brevo/Sendinblue)
        self.MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp-relay.brevo.com')
        self.MAIL_PORT = int(os.getenv('MAIL_PORT', '587'))
        self.MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'true').lower() in ('true', '1', 'yes')
        self.MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'false').lower() in ('true', '1', 'yes')
        self.MAIL_USERNAME = os.getenv('MAIL_USERNAME', '')
        self.MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', '')
        self.MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER', 'SkillFit <noreply@skillfit.com>')
        
        # Alternative email credentials (for backward compatibility)
        self.EMAIL_ADDRESS = os.getenv('EMAIL_ADDRESS', '')
        self.EMAIL_PASSWORD = os.getenv('EMAIL_PASSWORD', '')
        
        # Optional APIs
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
        self.GITHUB_API_TOKEN = os.getenv('GITHUB_API_TOKEN', '')

        # OAuth
        self.GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID', '')
        self.GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET', '')
        self.OAUTH_REDIRECT_URL = os.getenv('OAUTH_REDIRECT_URL', '')
        
        # Security settings
        self.security = SecurityConfig()
        
        # Parsing settings
        self.parsing = ParsingConfig()
        
        # Logging
        self.LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
        
        # Feature flags
        self.ROADMAP_SUPPORT = os.getenv('ROADMAP_SUPPORT', 'true').lower() in ('true', '1', 'yes')
        self.ML_CLASSIFIER_ENABLED = os.getenv('ML_CLASSIFIER_ENABLED', 'false').lower() in ('true', '1', 'yes')
        self.GITHUB_INTEGRATION_ENABLED = os.getenv('GITHUB_INTEGRATION_ENABLED', 'false').lower() in ('true', '1', 'yes')
        
        # File upload settings
        self.UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', self.base_dir / 'uploads')
        self.MAX_CONTENT_LENGTH = self.security.max_file_size_mb * 1024 * 1024
        
        self._validate_config()

    @classmethod
    def get_admin_credentials(cls) -> dict:
        """Parse admin credentials from environment variable"""
        credentials = {}
        admin_creds_raw = os.getenv('ADMIN_CREDENTIALS', '')
        if admin_creds_raw:
            for pair in admin_creds_raw.split(','):
                if ':' in pair:
                    admin_id, password = pair.strip().split(':', 1)
                    credentials[admin_id.strip()] = password.strip()
        return credentials
    
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
            
            # Warn about weak default credentials in production
            if self.ADMIN_PASSWORD == 'changeme':
                logging.warning("⚠️  WARNING: Using default admin password 'changeme' in production! Change ADMIN_PASSWORD immediately!")
        
        # Always warn about insecure defaults in development too
        if self.ADMIN_PASSWORD in ['changeme', 'admin', 'admin123', 'password']:
            logging.warning("⚠️  Using weak default admin password. Set ADMIN_PASSWORD in your .env file!")
    
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

    def _normalize_database_url(self, raw_url: str) -> str:
        if not raw_url:
            return ''
        url = raw_url.strip()
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        parsed = urlparse(url)
        if parsed.scheme.startswith('postgresql'):
            query = dict(parse_qsl(parsed.query))
            query['sslmode'] = query.get('sslmode') or os.getenv('DB_SSLMODE', 'require')
            url = urlunparse(parsed._replace(query=urlencode(query)))
        return url

    def _engine_options(self, db_uri: str) -> dict:
        opts = {
            'pool_pre_ping': True,
            'pool_recycle': int(os.getenv('SQLALCHEMY_POOL_RECYCLE', '300')),
        }
        if db_uri and db_uri.startswith('postgresql'):
            opts.update({
                'pool_size': int(os.getenv('SQLALCHEMY_POOL_SIZE', '5')),
                'max_overflow': int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '5')),
                'connect_args': {'sslmode': os.getenv('DB_SSLMODE', 'require')},
            })
        return opts

# Global config instance
config = Config()
