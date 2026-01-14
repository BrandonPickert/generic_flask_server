"""Application configuration."""
import os
from datetime import timedelta


class Config:
    """Base configuration."""
    
    # Basic Flask config
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*').split(',')
    
    # JSON settings
    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = True
    
    # Session configuration
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    
    # Request size limits
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    
    # Timezone
    TIMEZONE = os.getenv('TIMEZONE', 'UTC')


class DevelopmentConfig(Config):
    """Development configuration."""
    
    DEBUG = True
    TESTING = False
    
    # Development database (SQLite example)
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL',
        'sqlite:///dev.db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = True


class ProductionConfig(Config):
    """Production configuration."""
    
    DEBUG = False
    TESTING = False
    
    # Production database
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'postgresql://localhost/prod_db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Security headers
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    def __init__(self):
        """Initialize production config and validate required settings."""
        super().__init__()
        if not os.getenv('SECRET_KEY'):
            raise ValueError('SECRET_KEY environment variable must be set in production')


class TestingConfig(Config):
    """Testing configuration."""
    
    DEBUG = False
    TESTING = True
    
    # Use in-memory database for tests
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Disable CSRF for testing
    WTF_CSRF_ENABLED = False


# Configuration dictionary
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
