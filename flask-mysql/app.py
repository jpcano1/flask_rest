from flask import Flask, json, request, jsonify, make_response
from flask_sqlalchemy import SQLAlchemy
from marshmallow_sqlalchemy import ModelSchema
from marshmallow import fields
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = os.path.join(".", ".env")
load_dotenv(dotenv_path=env_path, verbose=True)

app = Flask(__name__)

# MySQL Config
# mysql_username = ""
# mysql_password = ""
# mysql_host = ""
# mysql_port = ""
# mysql_db = ""

# PostgreSQL Config
postgres_host = os.getenv("POSTGRES_HOST")
postgres_db = os.getenv("POSTGRES_DB")
postgres_user = os.getenv("POSTGRES_USER")
postgres_password = os.getenv("POSTGRES_PASSWORD")

# app.config["SQLALCHEMY_DATABASE_URI"] = f'mysql+pymysql://{mysql_username}:{mysql_password}@{mysql_host}:{mysql_port}/{mysql_db}'
app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{postgres_user}:{postgres_password}@{postgres_host}:5432/{postgres_db}"

db = SQLAlchemy(app)

class Author(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    specialization = db.Column(db.String(50))

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self

    def __init__(self, name, specialization):
        self.name = name
        self.specialization = specialization

    def __repr__(self):
        return f"Product {self.id}"

"""This Schema helps us to return the Author model in JSON Format"""
class AuthorSchema(ModelSchema):
    class Meta(ModelSchema.Meta):
        model = Author
        sql_session = db.session
    
    id = fields.Integer(dump_only=True)
    name = fields.String(required=True)
    specialization = fields.String(required=True)

@app.route("/authors", methods=["GET"])
def index():
    get_authors = Author.query.all()
    author_schema = AuthorSchema(many=True)
    authors = author_schema.dump(get_authors)
    return make_response(jsonify({
        "authors": authors
    }))

@app.route("/authors", methods=["POST"])
def create_author():
    data = request.get_json()
    author_schema = AuthorSchema()
    author = author_schema.load(data, session=db.session)
    result = author_schema.dump(author.create())
    return make_response(
        jsonify({
            "author": result
        }), 
        201
    )

@app.route("/authors/<id>", methods=["GET"])
def get_author_by_id(id):
    get_author = Author.query.get(id)
    author_schema = AuthorSchema()
    author = author_schema.dump(get_author)
    return make_response(
        jsonify({
            "author": author,
        }),
        200
    )

@app.route("/authors/<id>", methods=["PUT"])
def update_author_by_id(id):
    data = request.get_json()
    get_author = Author.query.get(id)

    if data.get("specialization"):
        get_author.specialization = data["specialization"]
    
    if data.get("name"):
        get_author.name = data["name"]

    db.session.add(get_author)
    db.session.commit()
    author_schema = AuthorSchema(
        only=["id", "name", "specialization"]
    )
    author = author_schema.dump(get_author)
    return make_response(
        jsonify({
            "author": author
        })
    )

@app.route("/authors/<id>", methods=["DELETE"])
def delete_by_id(id):
    get_author = Author.query.get(id)
    db.session.delete(get_author)
    db.session.commit()
    return make_response("", 204)
    
db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=3000)