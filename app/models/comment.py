from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app

class Comment():

    def __init__(self, data):

        self.id = data['id']
        self.comment_body = data['comment_body']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.owner = None
        self.forum = None

    