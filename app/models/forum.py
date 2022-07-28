from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from app.models.user import User
from app.models.comment import Comment

db = 'pet_blog_schema'

class Forum():


    def __init__(self, data):

        self.id = data['id']
        self.forum_title = data['title']
        self.forum_description = data['description']
        self.forum_created_at = data['created_at']
        self.forum_updated_at = data['updated_at']
        self.owner = None
        self.comments = []

    @classmethod
    def create_forum(cls, data):

        query = """
        INSERT INTO forums(title, description, created_at, updated_at, user_id)
        VALUES(%(title)s, %(description)s, NOW(), NOW(), %(user_id)s);
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Forum.get_forum(result)
        return selected

    @classmethod
    def get_forum(cls, data):

        data = {
            'id' : data
        }

        query = """
        SELECT forums.id, forums.title, forums.description, forums.created_at, forums.updated_at, users.id as user_id, users.first_name, 
        users.last_name, users.email, users.created_at, users.updated_at, image_path
        FROM forums
        JOIN users ON forums.user_id = users.id
        WHERE forums.id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Forum(result[0])
        forum_owner = {
                'id' : result[0]['user_id'],
                'first_name' : result[0]['first_name'],
                'last_name' : result[0]['last_name'],
                'email' : result[0]['email'],
                'created_at' : result[0]['created_at'],
                'updated_at' : result[0]['updated_at'],
                'image_path' : result[0]['image_path']
            }
        owner = User(forum_owner)
        selected.owner = owner
        return selected

    @classmethod
    def forum_list(cls):
        
        query = """
        SELECT forums.id, forums.title, forums.description, forums.created_at, forums.updated_at, users.id as user_id, users.first_name, 
        users.last_name, users.email, users.created_at, users.updated_at, image_path
        FROM forums
        JOIN users ON forums.user_id = users.id
        """
        result = connectToMySQL(db).query_db(query)
        forums = []
        for index in result:
            forum_owner = {
                'id' : index['user_id'],
                'first_name' : index['first_name'],
                'last_name' : index['last_name'],
                'email' : index['email'],
                'created_at' : index['created_at'],
                'updated_at' : index['updated_at'],
                'image_path' : index['image_path']
            }
            owner = User(forum_owner)
            forum = Forum(index)
            forum.owner = owner
            forums.append(forum)
        return forums

    @classmethod
    def forum_comments(cls, data):
        
        data = {
            'id' : data
        }
        query = """
        SELECT comments.id, comments.user_id, comments.comment_body, comments.created_at, comments.updated_at, users.first_name, 
        users.last_name, users.email, users.created_at, users.updated_at, image_path
        FROM comments
        JOIN users on comments.user_id = users.id
        WHERE comments.forum_id = %(id)s
        ORDER BY comments.id DESC;
        """
        comments = []
        result = connectToMySQL(db).query_db(query, data)
        for index in result:
            comment = Comment(index)
            comment_owner = {
                    'id' : index['user_id'],
                    'first_name' : index['first_name'],
                    'last_name' : index['last_name'],
                    'email' : index['email'],
                    'created_at' : index['users.created_at'],
                    'updated_at' : index['users.updated_at'],
                    'image_path' : index['image_path']
                }
            owner = User(comment_owner)
            comment.owner = owner
            comments.append(comment)
        return comments

    @classmethod
    def edit_forum(cls, data):

        query = """
        UPDATE forums
        SET title = %(title)s,
        description = %(description)s,
        updated_at = NOW()
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Forum.get_forum(data['id'])
        return selected

    @classmethod
    def delete_forum(cls, data):

        data = {
            'id' : data
        }
        
        query = """
        DELETE
        FROM forums
        WHERE id = %(id)s;
        """
        connectToMySQL(db).query_db(query, data)
        
    