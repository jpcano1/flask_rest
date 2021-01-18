from flask import Blueprint, request, url_for, current_app
from ..utils.responses import response_with
from ..utils import responses as resp
from ..models import Author, AuthorSchema
from ..utils import db
from flask_jwt_extended import jwt_required
import copy
from werkzeug.utils import secure_filename

import sys
import os

allowed_extensions = {"image/jpeg", "image/png", "jpeg"}

def allowed_file(filetype):
    return filetype in allowed_extensions

author_routes = Blueprint("author_routes", __name__)

@author_routes.route("/", methods=["POST"])
@jwt_required
def create_author():
    try:
        data = request.get_json()
        author_schema = AuthorSchema()
        author = author_schema.load(data, session=db.session)
        result = author_schema.dump(author.create())
        return response_with(resp.SUCCESS_201, value={
            "author": result
        })
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422, value={
            "error_response": str(e)
        })

@author_routes.route("/", methods=["GET"])
def get_author_list():
    fetched = Author.query.all()
    author_schema = AuthorSchema(many=True, only=[
        "id",
        "first_name",
        "last_name",
        "books"
    ])
    authors = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={
        "authors": authors
    })

@author_routes.route("/<int:author_id>", methods=["GET"])
def get_author_detail(author_id):
    fetched = Author.query.get_or_404(author_id)
    author_schema = AuthorSchema(only=[
        "id",
        "first_name",
        "last_name"
    ])
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={
        "author": author
    })

@jwt_required
@author_routes.route("/<int:id>", methods=["PUT", "PATCH"])
def update_author_detail(id):
    method = request.method
    data = request.get_json()
    fetched = Author.query.get_or_404(id)
    if method == "PUT":
        try:
            fetched.first_name = data["first_name"]
            fetched.last_name = data["last_name"]
        except KeyError as e:
            return response_with(resp.INVALID_INPUT_422, value={
                "error_message": "Data lacks of fields, use PATCH instead"
            })

    elif method == "PATCH":
        fetched_copy = copy.copy(fetched)
        fetched.first_name = data.get("first_name",
                                      fetched_copy.first_name)
        fetched.last_name = data.get("last_name",
                                     fetched_copy.last_name)
        del fetched_copy
    db.session.add(fetched)
    db.session.commit()
    author_schema = AuthorSchema(only=[
        "id",
        "first_name",
        "last_name",
        "books"
    ])
    author = author_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={
        "author": author
    })

@jwt_required
@author_routes.route("/<int:id>", methods=["DELETE"])
def delete_author(id):
    fetched = Author.query.get_or_404(id)
    db.session.delete(fetched)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

@jwt_required
@author_routes.route("/avatar/<int:id>", methods=["POST"])
def set_author_avatar(id):
    try:
        fetched = Author.query.get_or_404(id)
        file = request.files.get("avatar", None)
        if file and allowed_file(file.content_type):
            filename = secure_filename(file.filename)
            file.save(os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            ))
        else:
            return response_with(resp.INVALID_INPUT_422, value={
                "message": "There is no file"
            })
        fetched.avatar = url_for("uploaded_file",
                                 filename=filename,
                                 _external=True)
        db.session.add(fetched)
        db.session.commit()
        author_schema = AuthorSchema()
        author = author_schema.dump(fetched)
        return response_with(resp.SUCCESS_200, value={
            "author": author
        })
    except Exception as e:
        print(e, file=sys.stderr)
        return response_with(resp.INVALID_INPUT_422)