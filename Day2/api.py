from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import BookSchema

book_blp = Blueprint('books', 'books', url_prefix='/books', description='책에 관한 처리')

books = [] # DB 대용

@book_blp.route('/')
class BookList(MethodView):

    @book_blp.response(200, BookSchema(many=True))
    def get(self):
        return books
    
    @book_blp.arguments(BookSchema)
    @book_blp.response(201, BookSchema)
    def post(self, new_data):
        new_data['id'] = len(books) + 1
        books.append(new_data)

        return new_data
    
@book_blp.route('/<int:book_id>')
class Book(MethodView):
    
    @book_blp.response(200, BookSchema)
    def get(self, book_id):
        return book if (book:=next((book for book in books if book['id'] == book_id), None)) else abort(404, message='해당하는 책을 찾을 수 없습니다.')

    @book_blp.arguments(BookSchema)
    @book_blp.response(200, BookSchema)
    def put(self, new_data, book_id):
        book.update(new_data) if (book:=next((book for book in books if book['id'] == book_id), None)) else abort(404, message='해당하는 책을 찾을 수 없습니다.')

    @book_blp.response(204)
    def delete(self, book_id):
        books.remove(book) if (book:=next((book for book in books if book['id'] == book_id), None)) else abort(404, message='해당하는 책을 찾을 수 없습니다.')