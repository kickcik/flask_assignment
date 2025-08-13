from flask_smorest import Blueprint, abort
from flask import request, jsonify

def create_posts_blueprint(mysql):
    posts_blp = Blueprint('Posts', __name__, description='Poasts API', url_prefix='/posts')

    @posts_blp.route('/' , methods = ['GET', 'POST'])
    def posts():
        cursor = mysql.connection.cursor()

        if request.method == "GET":
            sql = "SELECT * FROM posts"
            cursor.execute(sql)

            posts = cursor.fetchall()
            cursor.close()

            post_list = []

            for post in posts:
                post_list.append(
                    {
                        "id": post[0],
                        "title": post[1],
                        "content": post[2],
                    }
                )
            return jsonify(post_list)
        
        elif request.method == 'POST':
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(404, message='title or content is empty')
            
            sql = 'insert into posts(title, content) values(%s, %s)'
            cursor.execute(sql, (title, content))
            mysql.connection.commit()

            return jsonify({'msg':'successfully created post data', 'title': title, 'content': content}), 201
    
    @posts_blp.route('/<int:id>', methods = ['GET', 'PUT', 'DELETE'])
    def post(id):
        cursor = mysql.connection.cursor()
        sql = f'select * from posts where id = {id}'
        cursor.execute(sql)
        post = cursor.fetchone()

        if request.method == 'GET':
            if not post:
                abort(404, 'not found post')
            
            return jsonify({
                        'id':post[0],
                        'title':post[1],
                        'content':post[2],
                    })
        
        elif request.method == 'PUT': 
            title = request.json.get('title')
            content = request.json.get('content')

            if not title or not content:
                abort(400, 'not found title or content')
                
            if not post:
                abort(404, 'not found post')
            
            sql = 'UPDATE posts SET title=%s, content=%s WHERE id=%s'
            cursor.execute(sql, (title, content, id))
            mysql.connection.commit()

            return jsonify({'msg':'successfully updated title and content'})

        elif request.method == 'DELETE':
            if not post:
                abort(404, 'not found post')

            sql = f'delete from posts where id = {id}'
            cursor.execute(sql)
            mysql.connection.commit()

            return jsonify({'msg':'successfully deleted data'})
    return posts_blp