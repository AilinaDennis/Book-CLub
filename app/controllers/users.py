from flask import render_template, redirect, session, request, flash
from app import app
from app.models.user import User
import os
from werkzeug.utils import secure_filename

# UPLOAD_FOLDER = 'C:/Users/Adam/Desktop/713solo/pet-blog/Pet-Blog-main/app/static/media'
# ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def main():
    return render_template('register.html')

@app.route('/regi', methods=['POST'])
def register():
    if not User.user_validation(request.form):
        return render_template('register.html')
    selected = User.create_user(request.form)
    return redirect(f'/dashboard/{selected.id}')

@app.route('/log', methods=['POST'])
def login():
    selected = User.check_login(request.form)
    return redirect(f'/dashboard/{selected.id}')

@app.route('/dashboard/<selected>')
def dashboard(selected):
    print(selected)
    user = User.get_user(selected)
    pets = User.user_pets(selected)
    selected = int(selected)
    return render_template('dashboard.html', user = user, pets = pets)

@app.route('/dashboard/<selected>/edit')
def edit_user(selected):
    user = User.get_user(selected)
    pets = User.user_pets(selected)
    selected = user.id
    return render_template('dashboard.html', user = user, pets = pets, selected = selected)

@app.route('/user/<selected>')
def change_user(selected):
    selected = User.get_user(selected)
    return render_template('edit_user.html', selected = selected)

@app.route('/user/edit', methods=['POST'])
def edit_user_picture():
    selected = User.edit_user(request.form)
    if not request.files['file'].filename == '':
        User.change_user_image(request.files)
    return redirect(f'/dashboard/{selected.id}')

@app.route('/user/delete', methods=['POST'])
def delete_account():
    User.delete_user(session)
    User.logout()
    return redirect('/')

@app.route('/logout')
def logout():
    User.logout()
    return redirect('/')

@app.route('/post/image', methods=['POST'])
def upload_file():
    user = User.change_user_image(request.files)
    return redirect(f'/dashboard/{user.id}')