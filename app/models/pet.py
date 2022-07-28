from app.config.mysqlconnection import MySQLConnection, connectToMySQL
from flask import flash, session
from app import app
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'C:/Users/Adam/Documents/group/Pet-Blog/app/static/media'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = 'pet_blog_schema'

class Pet():

    def __init__(self, data):
        self.id = data['id']
        self.pet_name = data['pet_name']
        self.pet_description = data['pet_description']
        self.pet_type = data['pet_type']
        self.pet_breed = data['pet_breed']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.picture = data['image_path']
        self.owner = None

    @staticmethod
    def pet_validation(input):

        is_valid = True

        if input['pet_name'] == '':
            is_valid = False
            flash('Your pets name is required' 'name')
        if input['pet_type'] == '':
            is_valid = False
            flash('The pet type is required', 'type')

        return is_valid

    @staticmethod
    def pet_parse(input):

        pet_info = {
            'pet_name' : input['pet_name'],
            'pet_type' : input['pet_type'],
            'pet_breed' : input['pet_breed'],
            'pet_description' : input['pet_description'],
            'id' : session['id']
        }

        return pet_info

    @classmethod
    def create_pet(cls, data):
        print(data)
        data = Pet.pet_parse(data)
        query = """
        INSERT INTO pets(pet_name, pet_description, pet_type, pet_breed, created_at, updated_at, user_id, image_path)
        VALUES (%(pet_name)s, %(pet_description)s, %(pet_type)s, %(pet_breed)s, NOW(), NOW(), %(id)s, '/static/media/pet_placeholder.jpeg');
        """
        result =  connectToMySQL(db).query_db(query, data)
        selected = Pet.get_pet(result)
        
        return selected

    @classmethod
    def get_pet(cls, result):

        if result == False:
            return result

        data = {
            'id' : result
        }
        query = """
        SELECT *
        FROM pets
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)

        return Pet(result[0])

    @staticmethod
    def edit_pet(data):
        
        query = """UPDATE pets
        SET pet_name = %(pet_name)s,
        pet_description = %(pet_description)s,
        pet_type = %(pet_type)s, 
        pet_breed = %(pet_breed)s, 
        updated_at = NOW() 
        WHERE id = %(id)s;
        """
        result = connectToMySQL(db).query_db(query, data)
        selected = Pet.get_pet(data['id'])
        return selected

    def delete_pet(data):

        data = {
            'id' : data
        }
        query = """
        DELETE
        FROM pets
        WHERE id = %(id)s
        """

        result = connectToMySQL(db).query_db(query, data)


    @staticmethod
    def allowed_file(filename):
        return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

    @classmethod
    def change_pet_image(self, pet_id, data):
   
        file = data['file']
        if file.filename == '':
            flash('No selected file')
            return False
        if file and Pet.allowed_file(file.filename):
            filename = str(pet_id) + 'pet.jpeg'
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        data = {
            'id' : pet_id,
            'image_path' : f'/static/media/{filename}'
        }
        query = """
        Update pets
        SET image_path = %(image_path)s,
        updated_at = NOW()
        WHERE id = %(id)s
        """
        connectToMySQL(db).query_db(query, data)
    