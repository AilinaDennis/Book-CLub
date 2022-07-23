from flask import render_template, redirect, session, request
from app import app
from app.models.forum import Forum

@app.route('/forum/add', methods=['POST'])
def add_forum():
    selected = Forum.create_forum(request.form)
    forums = Forum.forum_list()
    return render_template('TEST_forum.html', selected = selected, forums = forums)