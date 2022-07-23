from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
from flask_bcrypt import Bcrypt
from app.models.pet import Pet

db = 'pet_blog_schema'
bcrypt = Bcrypt(app)

class User():

    user_list = []

    def __init__(self, data):

        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pets = []

        User.user_list.append(self)

    @staticmethod
    def user_validation(input):

        is_valid = True

        if input['first_name'] == '':
            is_valid = False
            flash('First name is required' 'first')
        if input['last_name'] == '':
            is_valid = False
            flash('Last name is required', 'last')
        if input['email'] == '':
            is_valid = False
            flash('Email is required', 'email')
        if input['password'] != input['confirm']:
            is_valid = False
            flash('Passwords do not match')

        return is_valid

    @staticmethod
    def user_parse(input):

        user_info = {
            'first_name' : input['first_name'],
            'last_name' : input['last_name'],
            'email' : input['email'],
            'password' : bcrypt.generate_password_hash(input['password'])
        }

        return user_info

    @classmethod
    def create_user(cls, data):
        
        data = User.user_parse(data)
        query = """
        INSERT INTO users(first_name, last_name, email, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());
        """
        result =  connectToMySQL(db).query_db(query, data)
        session['id'] = result
        selected = User.get_user(result)
        return selected

    @staticmethod
    def check_login(data):

        query = """
        SELECT id, password
        FROM users
        WHERE email = %(email)s
        """
        result = connectToMySQL(db).query_db(query, data)
        if not result or bcrypt.check_password_hash(result[0]['password'], data['password']) == False:
            flash('Email or Password is incorrect.', 'login')
            return False
        session['id'] = result[0]['id']
        selected = User.get_user(result[0]['id'])

        return selected

    @classmethod
    def get_user(cls, result):

        if result == False:
            return result

        data = {
            'id' : result
        }
        query = """
        SELECT *
        FROM users
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        if session['id'] == result[0]['id']:
            User.create_session(result[0])

        return User(result[0])

    @staticmethod
    def create_session(data):
        session['first_name'] = data['first_name']
        session['last_name'] = data['last_name']
        session['email'] = data['email']

    @staticmethod
    def edit_user(data):
        
        query = """
        UPDATE users
        SET first_name = %(first_name)s,
        last_name = %(last_name)s, 
        email = %(email)s, 
        updated_at = NOW() 
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = User.get_user(session['id'])
        session['first_name'] = selected.first_name
        session['last_name'] = selected.last_name
        session['email'] = selected.email
        return selected

    @classmethod
    def user_pets(cls, data):

        data = {
            'id' : data
        }
    
        query = """
        SELECT *
        FROM pets
        JOIN users ON pets.user_id = users.id
        WHERE user_id = %(id)s
        """
        user_pets = []
        result = connectToMySQL(db).query_db(query, data)
        for index in result:
            pet = Pet(index)
            user_pets.append(pet)
        
        return user_pets

    @staticmethod
    def delete_user(data):

        query = """
        DELETE
        FROM users
        WHERE id = %(id)s;
        """

        result = connectToMySQL(db).query_db(query, data)


    @staticmethod
    def logout():

        session.clear()