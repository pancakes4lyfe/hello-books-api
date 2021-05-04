from app import db
from flask import Blueprint
from flask import request
from .models.book import Book
from flask import jsonify

books_bp = Blueprint("books", __name__, url_prefix="/books")

#helper function to check if id is an integer
def is_int(value):
    try:
        return int(value)
    except ValueError:
        return False

@books_bp.route("/<book_id>", methods=["GET", "PUT", "DELETE"], strict_slashes=False)
def handle_book(book_id):
    book = Book.query.get(book_id)
    if book is None:
        return jsonify({
            "message": f"Book with id {book_id} was not found",
            "success": False
        }), 404
    if request.method == "GET":
        return jsonify(book.to_json()), 200
    elif request.method == "PUT":
        form_data = request.get_json()
        book.title = form_data["title"]
        book.description = form_data["description"]
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Book #{book.id} successfully updated"
        }), 200
    elif request.method == "DELETE":
        db.session.delete(book)
        db.session.commit()
        return jsonify({
            "success": True,
            "message": f"Book #{book.id} successfully deleted"
        }), 200

@books_bp.route("", methods=["GET"], strict_slashes=False)
def books_index():
    #This now allows queries by title
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()
    books_response = []

    for book in books:
        books_response.append(book.to_json())
    return jsonify(books_response), 200

@books_bp.route("", methods=["POST"], strict_slashes=False)
def books():
    request_body = request.get_json()
    new_book = Book(title = request_body["title"], 
                        description = request_body["description"])
    db.session.add(new_book)
    db.session.commit()
    return jsonify ({
        "success": True,
        "message": f"Book {new_book.title} has been created"
    }), 201
