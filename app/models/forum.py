from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from app.models.user import User

db = 'pet_blog_schema'

class Forum():


    def __init__(self, data):

        self.id = data['id']
        self.forum_title = data['forum_title']
        self.forum_description = data['forum_description']
        self.forum_created_at = data['created_at']
        self.forum_updated_at = data['updated_at']
        self.owner = None
        self.comments = []

    @classmethod
    def create_forum(cls, data):

        query = """
        INSERT INTO forums(forum_title, forum_description, created_at, updated_at, user_id)
        VALUES(%(forum_title)s, %(forum_description)s, NOW(), NOW(), %(user_id)s);
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
        SELECT forums.id, forums.forum_title, forums.forum_description, forums.created_at, forums.updated_at, users.id as user_id, users.first_name, 
        users.last_name, users.email, users.created_at, users.updated_at
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
                'updated_at' : result[0]['updated_at']
            }
        owner = User(forum_owner)
        selected.owner = owner
        return selected

    @classmethod
    def forum_list(cls):
        
        query = """
        SELECT forums.id, forums.forum_title, forums.forum_description, forums.created_at, forums.updated_at, users.id as user_id, users.first_name, 
        users.last_name, users.email, users.created_at, users.updated_at
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
                'updated_at' : index['updated_at']
            }
            owner = User(forum_owner)
            forum = Forum(index)
            forum.owner = owner
            forums.append(forum)
        return forums

    @classmethod
    def edit_forum(data):

        query = """
        UPDATE forums
        SET forum_title = %(title)s,
        description = %(description)s,
        updated_at = NOW(),
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Forum.get_forum(data['id'])
        return selected

    @classmethod
    def delete_forum(data):
        
        query = """
        DELETE
        FROM forums
        WHERE id = %(id)s;
        """
        connectToMySQL(db).query_db(query, data)
        
    