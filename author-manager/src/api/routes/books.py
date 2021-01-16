from flask import Blueprint, request
from ..utils import response_with
from ..utils import responses as resp
from ..models import BookSchema, Book
from ..utils import db
import psycopg2.errors as errors
import psycopg2

book_routes = Blueprint("book_routes", __name__)

@book_routes.route("/", methods=["POST"])
def create_book():
    try:
        data = request.get_json()
        book_schema = BookSchema()
        book = book_schema.load(data, session=db.session)
        result = book_schema.dump(book.create())
        return response_with(resp.SUCCESS_201, value={
            "book": result
        })
    except Exception as e:
        return response_with(resp.INVALID_INPUT_422, value={
            "error_message": str(e)
        })