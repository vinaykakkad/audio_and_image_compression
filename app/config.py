from decouple import config
from flask import Flask


class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config('SECRET_KEY')
    

class ProductionConfig(Config):
    DEBUG = False


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    EXPLAIN_TEMPLATE_LOADING = True
    TEMPLATES_AUTO_RELOAD = True


class TestingConfig(Config):
    TESTING = True


def create_app():
    """
        To create the app with proper configuations
    """

    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
   
    with app.app_context():
        from .routes import general, audio, image

    return app