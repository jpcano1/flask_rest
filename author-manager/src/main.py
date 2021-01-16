from flask import Flask, logging
from api.utils.database import db
from api.utils.responses import response_with
import api.utils.responses as resp
from api.config.config import (DevelopmentConfig,
                               ProductionConfig,
                               TestingConfig)
from dotenv import load_dotenv, find_dotenv
import os

# Blueprints
from api.routes.authors import author_routes

load_dotenv(find_dotenv())

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)

db.init_app(app)
with app.app_context():
    db.create_all()

@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(error):
    return response_with(resp.BAD_REQUEST_400, value={
        "error_message": str(error)
    })

@app.errorhandler(500)
def server_error(error):
    return response_with(resp.SERVER_ERROR_500, value={
        "error_message": str(error)
    })

@app.errorhandler(404)
def not_found(error):
    return response_with(resp.SERVER_ERROR_404, value={
        "error_message": str(error)
    })

app.register_blueprint(author_routes, url_prefix="/api/authors")