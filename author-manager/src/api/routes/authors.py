from flask import Blueprint, request
from ..utils.responses import response_with
from ..utils import responses as resp
from ..models import Author, AuthorSchema
from ..utils import db
import copy

author_routes = Blueprint("author_routes", __name__)

@author_routes.route("/", methods=["POST"])
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

@author_routes.route("/<int:id>", methods=["PUT"])
def update_author_detail(id):
    data = request.get_json()
    fetched = Author.query.get_or_404(id)
    fetched_copy = copy.copy(fetched)
    fetched.first_name = data.get("first_name",
                                  fetched_copy.first_name)
    fetched.last_name = data.get("last_name",
                                 fetched_copy.last_name)
    db.session.add(fetched)
    db.session.commit()
    author_schema = AuthorSchema()
    author = author_schema.dump(fetched)
    del fetched_copy
    return response_with(resp.SUCCESS_200, value={
        "author": author
    })