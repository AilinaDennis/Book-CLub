from winreg import QueryInfoKey
from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from app.models.user import User

db = 'pet_blog_schema'

class Comment():

    def __init__(self, data):

        self.id = data['id']
        self.comment_body = data['comment_body']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None

    @staticmethod
    def comment_validation(input):

        is_valid = True
        if input['comment_body'] == '':
            is_valid = False
            flash('Make sure you are leaving a comment and not blank space.')
        return is_valid

    @classmethod
    def create_comment(cls, data):

        query = """
        INSERT 
        INTO comments(user_id, forum_id, comment_body, created_at, updated_at)
        VALUES(%(user_id)s, %(forum_id)s, %(comment_body)s, NOW(), NOW());
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Comment.get_comment(result)
        return selected

    @classmethod
    def get_comment(cls, data):

        data = {
            'id' : data
        }
        query = """
        SELECT comments.id, comments.forum_id, comments.user_id, comments.comment_body, comments.created_at, comments.updated_at, users.first_name, 
        users.last_name, users.email, users.created_at, users.updated_at, image_path
        FROM comments
        JOIN users on comments.user_id = users.id
        WHERE comments.id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Comment(result[0])
        comment_owner = {
                'id' : result[0]['user_id'],
                'first_name' : result[0]['first_name'],
                'last_name' : result[0]['last_name'],
                'email' : result[0]['email'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at'],
                'image_path' : result[0]['image_path']
            }
        owner = User(comment_owner)
        selected.owner = owner
        return selected

    @classmethod
    def edit_comment(cls, data):

        query = """
        UPDATE comments
        SET comment_body = %(comment_body)s,
        updated_at = NOW()
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Comment.get_comment(data['id'])
        return selected

    @staticmethod
    def delete_comment(data):

        data = {
            'id' : data
        }
        query = """
        DELETE 
        FROM comments
        WHERE id = %(id)s;
        """
        connectToMySQL(db).query_db(query, data)
    