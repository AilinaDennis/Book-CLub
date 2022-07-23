from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from app.models.user import User

db = 'pet_blog_schema'

class Forum():


    def __init__(self, data):

        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
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
        SELECT *
        FROM forums
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Forum(result[0])
        return selected

    @classmethod
    def forum_list(cls):
        
        query = """
        SELECT forums.id, forums.title, forums.description, forums.created_at, forums.updated_at, users.id as user_id, users.first_name, 
        users.last_name, users.email, users.created_at, users.updated_at
        FROM forums
        JOIN users ON forums.user_id = users.id
        """
        result = connectToMySQL(db).query_db(query)
        forums = []
        for index in result:
            forum_owner = {
                'id' : index['id'],
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
        SET title = %(title)s,
        description = %(description)s,
        updated_at = NOW(),
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Forum.get_forum(data['id'])
        return selected

    