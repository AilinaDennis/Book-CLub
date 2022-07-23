from flask import render_template, redirect, session, request
from app import app
from app.models.user import User

@app.route('/')
def main():
    return render_template('TEST_user.html')

@app.route('/regi', methods=['POST'])
def register():
    User.user_validation(request.form)
    selected = User.create_user(request.form)
    return render_template('TEST.html', selected = selected)

@app.route('/log', methods=['POST'])
def login():
    selected = User.check_login(request.form)
    pets = User.user_pets(session['id'])
    return render_template('TEST.html', selected = selected, pets = pets)

@app.route('/user/edit', methods=['POST'])
def edit_user():
    selected = User.edit_user(request.form)
    return render_template('TEST.html', selected = selected)

@app.route('/user/delete', methods=['POST'])
def delete_account():
    User.delete_user(session)
    User.logout()
    return redirect('/')

@app.route('/logout')
def logout():
    User.logout()
    return redirect('/')