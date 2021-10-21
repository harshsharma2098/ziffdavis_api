import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Parent configuration class"""

    DEBUG = False
    CSRF_ENABLED = True
    SECRET = os.environ.get("SECRET")
    UPLOAD_FOLDER = "static"


class DevelopmentConfig(Config):
    """Development configuration class"""

    DEBUG = True


class TestingConfig(Config):
    """Testing configuration class"""

    TESTING = True
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration class"""

    DEBUG = False
    TESTING = False
