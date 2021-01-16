from flask import Blueprint, request
from ..utils import response_with
from ..utils import responses as resp
from ..models import BookSchema, Book
from ..utils import db
import copy

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

@book_routes.route("/", methods=["GET"])
def get_book_list():
    fetched = Book.query.all()
    book_schema = BookSchema(many=True, only=[
        "id",
        "author_id",
        "title",
        "year"
    ])
    books = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={
        "books": books
    })

@book_routes.route("/<int:book_id>", methods=["GET"])
def get_book_detail(book_id):
    fetched = Book.query.get_or_404(book_id)
    book_schema = BookSchema()
    book = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={
        "book": book
    })

@book_routes.route("/<int:id>", methods=["PUT", "PATCH"])
def update_book_detail(id):
    method = request.method
    data = request.get_json()
    fetched = Book.query.get_or_404(id)
    if method == "PUT":
        try:
            fetched.title = data["title"]
            fetched.year = data["year"]
        except KeyError:
            return response_with(resp.INVALID_INPUT_422, value={
                "error_message": "Data lacks of fields, use PATCH instead"
            })

    elif method == "PATCH":
        fetched_copy = copy.copy(fetched)
        fetched.title = data.get("first_name", fetched_copy.title)
        fetched.year = data.get("year", fetched_copy.year)
        del fetched_copy
    db.session.add(fetched)
    db.session.commit()
    book_schema = BookSchema()
    book = book_schema.dump(fetched)
    return response_with(resp.SUCCESS_200, value={
        "book": book
    })

@book_routes.route("/<int:id>", methods=["DELETE"])
def delete_book(id):
    fetched = Book.query.get(id)
    db.session.delete(fetched)
    db.session.commit()
    return response_with(resp.SUCCESS_204)