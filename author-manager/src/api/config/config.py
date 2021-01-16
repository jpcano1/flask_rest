import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

class Config(object):
    USER = os.environ.get("POSTGRES_USER"),
    PASS = os.environ.get("POSTGRES_PASSWORD"),
    HOST = os.environ.get("POSTGRES_HOST"),
    DB = os.environ.get("POSTGRES_DB")

    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = "<Production DB URL>"

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_DATABASE_URI = f"postgresql://{Config.USER[0]}:{Config.PASS[0]}@{Config.HOST[0]}:5432/{Config.DB}"

    def __init__(self):
        super(DevelopmentConfig, self).__init__()

class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "<Testing DB URL>"
    SQLALCHEMY_ECHO = False
