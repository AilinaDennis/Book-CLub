from flask import render_template, redirect, session, request
from app import app
from app.models.pet import Pet

@app.route('/pet/add', methods=['POST'])
def add_pet():
    Pet.pet_validation(request.form)
    selected = Pet.create_pet(request.form)
    user = session['id']
    return redirect(f'/dashboard/{user}')

#the process should be as follows dashboard - click on add pet > brings to this route with the pet form on it > after hitting submit goes to the post route for /pet/add > which then should redirect either back to the dashboard or to the pets display page
#for the form you can either copy it or change, just make sure their is a hidden input their that has the session id passed as id in the request form
@app.route('/create/pet')
def new_pet():
    if not session:
        return redirect('/log') 

    return render_template('new_pet.html') 

@app.route('/pet/edit/<selected>')
def change_pet(selected):
    pet = Pet.get_pet(selected)
    return render_template('edit_pet.html', pet = pet)


@app.route('/pet/change/<selected>', methods=['POST'])
def edit_pet(selected):
    selected = Pet.edit_pet(request.form)
    return redirect(f'/pet/{selected.id}')

@app.route('/pet/delete/<selected>')
def delete_pet(selected):
    Pet.delete_pet(selected)
    user = session['id']
    return redirect(f'/dashboard/{user}')

#when displaying the pet it should pass back as an object so in the 
#html just put the link to /pet/{{ pet_object.id }} pet_object being whatever its named on the page
#where you selected the pet. note that its not set up to take in a dictionary key pair, only a value
#for the id. I can change if need be
@app.route('/pet/<selected>')
def show_pet(selected):
    pet = Pet.get_pet(selected)
    print(pet)
    return render_template('show_pet.html', pet = pet)
