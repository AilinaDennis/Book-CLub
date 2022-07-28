from flask import render_template, redirect, session, request
from app import app
from app.models.forum import Forum
from app.models.comment import Comment

@app.route('/forum/add')
def forum_info():
    if not session:
        return redirect('/')
    return render_template('forum.html')

@app.route('/forum/create', methods=['POST'])
def add_forum():
    if not session:
        return redirect('/')
    if not Forum.forum_validation(request.form):
        return render_template('forum.html')
    selected = Forum.create_forum(request.form)
    return redirect(f'/forum/{selected.id}')

@app.route('/forum/<selected>')
def show_forum(selected):
    if not session:
        return redirect('/')
    forum = Forum.get_forum(selected)
    comments = Forum.forum_comments(selected)
    return render_template('forum_display.html', forum = forum, comments = comments)

@app.route('/<forum>/comment/edit/<selected>')
def edit_comment(forum, selected):
    if not session:
        return redirect('/')
    comments = Forum.forum_comments(forum)
    forum = Forum.get_forum(forum)
    selected = int(selected)
    return render_template('forum_display.html', forum = forum, comments = comments, selected = selected)

@app.route('/forum/edit/<selected>')
def edit_forum(selected):
    if not session:
        return redirect('/')
    forum = Forum.get_forum(selected)
    return render_template('edit_forum.html', forum = forum)

@app.route('/forum/change/<selected>', methods=['POST'])
def change_forum(selected):
    if not session:
        return redirect('/')
    if not Forum.forum_validation(request.form):
        return redirect(f'/forum/edit/{selected}')
    Forum.edit_forum(request.form)
    return redirect(f'/forum/{selected}')

@app.route('/forums')
def forum_list():
    if not session:
        return redirect('/')
    forums = Forum.forum_list()
    return render_template('forum_list.html', forums = forums)

@app.route('/forum/delete/<selected>')
def delete_forum(selected):
    if not session:
        return redirect('/')
    Forum.delete_forum(selected)
    return redirect('/forums')