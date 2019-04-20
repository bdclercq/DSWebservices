import os  # new


class BaseConfig:
    """Base configuration"""
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'my_precious'


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    pass


class ProductionConfig(BaseConfig):
    """Production configuration"""
    pass
