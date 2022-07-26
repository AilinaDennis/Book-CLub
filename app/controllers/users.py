from flask import render_template, redirect, session, request
from app import app
from app.models.user import User

@app.route('/')
def main():
    return render_template('register.html')

@app.route('/regi', methods=['POST'])
def register():
    User.user_validation(request.form)
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
    return render_template('dashboard.html', user = user, pets = pets)

@app.route('/user/<selected>')
def change_user(selected):
    selected = User.get_user(selected)
    return render_template('edit_user.html', selected = selected)

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