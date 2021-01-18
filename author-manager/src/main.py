import logging
import sys
from flask import Flask, send_from_directory
from api.utils import response_with, db, mail
import api.utils.responses as resp
from api.config import (DevelopmentConfig,
                        ProductionConfig,
                        TestingConfig)
from dotenv import load_dotenv, find_dotenv
from flask_jwt_extended import JWTManager
import os

# Blueprints
from api.routes import (author_routes,
                        book_routes,
                        user_routes)

load_dotenv(find_dotenv())

app = Flask(__name__)

if os.environ.get('WORK_ENV') == 'PROD':
    app_config = ProductionConfig
elif os.environ.get('WORK_ENV') == 'TEST':
    app_config = TestingConfig
else:
    app_config = DevelopmentConfig

app.config.from_object(app_config)
jwt = JWTManager(app)
mail.init_app(app)

db.init_app(app)
with app.app_context():
    db.create_all()

@app.after_request
def add_header(response):
    return response

@app.errorhandler(400)
def bad_request(error):
    logging.error(error)
    return response_with(resp.BAD_REQUEST_400)

@app.errorhandler(500)
def server_error(error):
    logging.error(error)
    return response_with(resp.SERVER_ERROR_500)

@app.errorhandler(404)
def not_found(error):
    logging.error(error)
    return response_with(resp.SERVER_ERROR_404)

@app.route("/avatar/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

logging.basicConfig(
    stream=sys.stdout,
    format="%(asctime)s|%(levelname)s|%(filename)s: %(lineno)s| %(message)s",
    level=logging.DEBUG
)

app.register_blueprint(author_routes, url_prefix="/api/authors")
app.register_blueprint(book_routes, url_prefix="/api/books")
app.register_blueprint(user_routes, url_prefix="/api/users")