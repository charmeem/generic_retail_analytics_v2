"""Flask configuration."""
from os import environ, path
from dotenv import load_dotenv  #install using pip install python-dotenv

basedir = path.abspath(path.dirname(__file__))
load_dotenv(path.join(basedir, '.env'))

# NOTE Not utilizing .env currently

class Config:
    """Flask configuration variables."""
    
    # user configurations
    dash_debug = False
    dash_auto_reload = False
    
    # General Config
    FLASK_APP = "wsgi.py"
    # FLASK_ENV = environ.get("FLASK_ENV")
    # FLASK_ENV = 'development'
    FLASK_DEBUG = False
    # FLASK_DEBUG = False

    SECRET_KEY = environ.get("SECRET_KEY")

    # Assets
    # LESS_BIN = environ.get("LESS_BIN")
    LESS_BIN = "/c/Users/hp/AppData/Roaming/npm/lessc"
    # ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    ASSETS_DEBUG = False
    ASSETS_AUTO_BUILD = True
    # LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "static"
    TEMPLATES_FOLDER = "templates"
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")
    
    # Database
    SQLALCHEMY_DATABASE_URI = environ.get("SQLALCHEMY_DATABASE_URI")    
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #Email related configuration
    MAIL_SERVER=environ.get("MAIL_SERVER")
    MAIL_PORT = environ.get("MAIL_PORT")
    MAIL_USERNAME = environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = environ.get("MAIL_USE_TLS")
    MAIL_USE_SSL = environ.get("MAIL_USE_SSL")