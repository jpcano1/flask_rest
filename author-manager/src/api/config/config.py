import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config(object):
    POSTGRES_USERNAME = os.environ.get("POSTGRES_USER", None)
    POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", None)
    POSTGRES_HOST = os.environ.get("POSTGRES_HOST", None)
    POSTGRES_DB = os.environ.get("POSTGRES_DB", None)

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    MAIL_DEFAULT_SENDER = os.environ.get("EMAIL_SENDER")
    MAIL_SERVER = os.environ.get("EMAIL_SERVER")
    MAIL_PORT = os.environ.get("EMAIL_PORT")
    MAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
    MAIL_USE_TLS = os.environ.get("EMAIL_USE_TLS")
    MAIL_USE_SSL = os.environ.get("EMAIL_USE_SSL")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "<Production DB URL>"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.POSTGRES_USERNAME}:{Config.POSTGRES_PASSWORD}@{Config.POSTGRES_HOST}:5432/{Config.POSTGRES_DB}"
    SECRET_KEY = os.environ.get("SECRET_KEY", None)
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", None)

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "<Testing DB URL>"
    SQLALCHEMY_ECHO = False
