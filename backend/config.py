# backend/config.py
import os
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    # Basic Flask config
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev')
    DEBUG = False
    TESTING = False
    
    # Database URIs
    AIRCRAFT_DATABASE_URI = os.environ.get(
        'AIRCRAFT_DATABASE_URI',
        'sqlite:///./data/aircraft_data.db'
    )
    GSE_DATABASE_URI = os.environ.get(
        'GSE_DATABASE_URI',
        'sqlite:///./data/gse_data.db'
    )
    
    # SQLAlchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQL_ECHO = False
    
    # Logging config
    LOG_LEVEL = logging.INFO
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # API config
    API_TITLE = 'Hydrogen Dashboard API'
    API_VERSION = 'v1'
    CORS_HEADERS = 'Content-Type'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQL_ECHO = True
    LOG_LEVEL = logging.DEBUG

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    # Use in-memory SQLite for testing
    AIRCRAFT_DATABASE_URI = 'sqlite:///:memory:'
    GSE_DATABASE_URI = 'sqlite:///:memory:'
    SQL_ECHO = False
    LOG_LEVEL = logging.DEBUG

class ProductionConfig(Config):
    """Production configuration."""
    # Override with production database URIs
    AIRCRAFT_DATABASE_URI = os.environ.get('PROD_AIRCRAFT_DATABASE_URI')
    GSE_DATABASE_URI = os.environ.get('PROD_GSE_DATABASE_URI')
    
    # Stricter security settings for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = 3600  # 1 hour
    
    # Production logging
    LOG_LEVEL = logging.WARNING

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=os.environ.get('FLASK_ENV', 'default')):
    """Get configuration class by name."""
    return config.get(config_name, config['default'])

def init_logging(app):
    """Initialize logging configuration."""
    logging.basicConfig(
        level=app.config['LOG_LEVEL'],
        format=app.config['LOG_FORMAT']
    )