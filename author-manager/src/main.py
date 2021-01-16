import os
from flask import Flask, jsonify
from api.utils.database import db

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    with app.app_context():
        db.create_all()
    return app