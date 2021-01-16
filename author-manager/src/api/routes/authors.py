from flask import Blueprint, request
from ..utils.responses import response_with
from ..utils import responses as resp
from ..models import Author, AuthorSchema
from ..utils import db

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
        print(e)
        return response_with(resp.INVALID_INPUT_422)