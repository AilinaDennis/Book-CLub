from flask import render_template, redirect, session, request
from app import app
from app.models.pet import Pet

@app.route('/pet/add', methods=['POST'])
def add_pet():
    if not session:
        return redirect('/')
    if not Pet.pet_validation(request.form):
        return render_template('new_pet.html')
    selected = Pet.create_pet(request.form)
    user = session['id']
    return redirect(f'/dashboard/{user}')

@app.route('/create/pet')
def new_pet():
    if not session:
        return redirect('/log') 
    return render_template('new_pet.html') 

@app.route('/pet/edit/<selected>')
def change_pet(selected):
    if not session:
        return redirect('/')
    pet = Pet.get_pet(selected)
    return render_template('edit_pet.html', pet = pet)


@app.route('/pet/change/<selected>', methods=['POST'])
def edit_pet(selected):
    if not session:
        return redirect('/')
    user = session['id']
    if not Pet.pet_validation(request.form):
        return redirect(f'/pet/edit/{selected}')
    selected = Pet.edit_pet(request.form)
    if not request.files['file'].filename == '':
        Pet.change_pet_image(request.form['id'], request.files)
    return redirect(f'/dashboard/{user}')

@app.route('/pet/delete/<selected>')
def delete_pet(selected):
    if not session:
        return redirect('/')
    Pet.delete_pet(selected)
    user = session['id']
    return redirect(f'/dashboard/{user}')

@app.route('/pet/<selected>')
def show_pet(selected):
    if not session:
        return redirect('/')
    pet = Pet.get_pet(selected)
    print(pet)
    return render_template('show_pet.html', pet = pet)
