import os

from decouple import config
from flask import Flask


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PLAY_FOLDER = os.path.join(BASE_DIR, "tmp", "play")
COMPRESS_FOLDER = os.path.join(BASE_DIR, "tmp", "compress")
COMPRESSED_IMAGE_FOLDER = os.path.join(BASE_DIR, "tmp", "compressed_images")

SAMPLE_AUDIO_FOLDER = os.path.join(BASE_DIR, "tmp", "samples", "audio")
SAMPLE_IMAGE_FOLDER = os.path.join(BASE_DIR, "tmp", "samples", "image")


class Config(object):
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = config("SECRET_KEY")
    STATIC_FOLDER = "tmp"


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

    app = Flask(
        __name__, static_url_path="/tmp", static_folder=os.path.join(BASE_DIR, "tmp")
    )
    app.config.from_object(DevelopmentConfig)

    with app.app_context():
        from .routes import general, audio, image

    return app
