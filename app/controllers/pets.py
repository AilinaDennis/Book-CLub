from flask import render_template, redirect, session, request
from app import app
from app.models.pet import Pet

@app.route('/pet/add', methods=['POST'])
def add_pet():
    Pet.pet_validation(request.form)
    selected = Pet.create_pet(request.form)
    return render_template('TEST_pet.html', selected = selected)

@app.route('/pet/edit', methods=['POST'])
def edit_pet():
    selected = Pet.edit_pet(request.form)
    return render_template('TEST_pet.html', selected = selected)

@app.route('/pet/delete', methods=['POST'])
def delete_pet():
    Pet.delete_pet('1')
    return redirect('/')