from flask import render_template, redirect, session, request
from app import app
from app.models.forum import Forum

@app.route('/forum/add')
def forum_info():
    return render_template('forum_input.html')

@app.route('/forum/create', methods=['POST'])
def add_forum():
    selected = Forum.create_forum(request.form)
    return redirect(f'/forum/{selected.id}')

@app.route('/forum/<selected>')
def show_forum(selected):
    forum = Forum.get_forum(selected)
    return render_template('forum_display.html', forum = forum)

@app.route('/forum/edit/<selected>')
def edit_forum(selected):
    forum = Forum.get_forum(selected)
    return render_template('edit_forum.html', forum = forum)

@app.route('/forum/change/<selected>', methods=['POST'])
def change_forum(selected):
    print(request.form)
    Forum.edit_forum(request.form)
    return redirect(f'/forum/{selected}')

@app.route('/forums')
def forum_list():
    forums = Forum.forum_list()
    return render_template('forum_list.html', forums = forums)

@app.route('/forum/delete/<selected>')
def delete_forum(selected):
    Forum.delete_forum(selected)
    return redirect('/forums')