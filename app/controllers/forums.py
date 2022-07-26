from flask import render_template, redirect, session, request
from app import app
from app.models.forum import Forum

@app.route('/forum/add')
def forum_info():
    return render_template('forum_input_test.html')

@app.route('/forum/create', methods=['POST'])
def add_forum():
    selected = Forum.create_forum(request.form)
    return redirect(f'/forum/{selected.id}')

@app.route('/forum/<selected>')
def show_forum(selected):
    forum = Forum.get_forum(selected)
    return render_template('forum_display_test.html', forum = forum)

@app.route('/forums')
def fourm_list():
    forums = Forum.forum_list()
    return render_template('forum_list_test.html', forums = forums)