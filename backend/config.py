import os
from datetime import timedelta

class Config:
    DEBUG = False
    TESTING = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'change-me-in-production')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///visionguard.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
    CORS_HEADERS = 'Content-Type'
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'change-me-in-production')
    JWT_ALGORITHM = 'HS256'
    JWT_EXPIRATION_DELTA = timedelta(hours=24)

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'

MODEL_CONFIG = {
    'face_detection': {
        'model_path': 'models/face_detection/model.weights',
        'config_path': 'models/face_detection/config.json',
        'confidence_threshold': 0.7,
        'nms_threshold': 0.4
    },
    'ppe_detection': {
        'model_path': 'ppe_model/best.pt',
        'config_path': None,
        'confidence_threshold': 0.5,
        'nms_threshold': 0.4
    },
    'box_counting': {
        'model_path': 'box_model/best_fixed.pt',
        'config_path': None,
        'confidence_threshold': 0.75,
        'nms_threshold': 0.3
    }
}

FEATURES = {
    'face_detection': {
        'enabled': True,
        'real_time': True,
        'batch_processing': True,
        'export_results': True
    },
    'ppe_detection': {
        'enabled': True,
        'real_time': True,
        'batch_processing': True,
        'export_results': True
    },
    'box_counting': {
        'enabled': True,
        'real_time': True,
        'batch_processing': True,
        'export_results': True
    }
}

API_CONFIG = {
    'version': 'v1',
    'base_url': os.getenv('API_BASE_URL', '/api'),
    'timeout': 30,
    'max_retries': 3
}

def get_config(env=None):
    if env is None:
        env = os.getenv('FLASK_ENV', 'development')
    if env == 'production':
        return ProductionConfig()
    elif env == 'testing':
        return TestingConfig()
    else:
        return DevelopmentConfig()

