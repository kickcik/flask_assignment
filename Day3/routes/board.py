from flask_smorest import Blueprint
from flask import request, jsonify
from flask.views import MethodView
from db import db
from models import Board

board_blp = Blueprint('Boards', 'Boards', description = 'Operation on boards', url_prefix='/board')

@board_blp.route('/')
class BoardList(MethodView):

    @board_blp.response(200)
    def get(self):
        boards = Board.query.all()

        return jsonify([{'id':board.id,
                         'title':board.title,
                         'content':board.content,
                         'user_id':board.author.id,
                         'author_name':board.author.name,
                         'author_email':board.author.email}
                         for board in boards])
    
    @board_blp.response(201)
    def post(self):
        data = request.json
        new_board = Board(title=data['title'], content=data['content'], user_id=data['user_id'])
        db.session.add(new_board)
        db.session.commit()

        return jsonify({'msg':'success create board'})

@board_blp.route('/<int:board_id>')
class BoardResource(MethodView):

    def get(self, board_id):
        board = Board.query.get_or_404(board_id)

        return jsonify({'id':board.id,
                         'title':board.title,
                         'content':board.content,
                         'author_name':board.author.name})
    
    def put(self, board_id):
        board = Board.query.get_or_404(board_id)

        data = request.json

        board.title = data['title']
        board.content = data['content']

        db.session.commit()

        return jsonify({'msg':'Seccessfully updated'})
    
    def delete(self, board_id):
        board = Board.query.get_or_404(board_id)
        db.session.delete(board)
        db.session.commit()

        return jsonify({'msg':'Seccessfully deleted'}) 