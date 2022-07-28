from flask import render_template, redirect, session, request
from app import app
from app.models.comment import Comment

@app.route('/comment/add/<selected>', methods=['POST'])
def add_comment(selected):
    if not session:
        return redirect('/')
    if not Comment.comment_validation(request.form):
        return redirect(f'/forum/{selected}')
    comment = Comment.create_comment(request.form)
    return redirect(f'/forum/{selected}')

@app.route('/comment/show/<selected>')
def show_comment(selected):
    if not session:
        return redirect('/')
    comment = Comment.get_comment(selected)
    return render_template('test_comment.html', comment = comment)

@app.route('/<forum>/comment/change/<selected>', methods=["POST"])
def change_comment(forum, selected):
    if not session:
        return redirect('/')
    if not Comment.comment_validation(request.form):
        return redirect(f'/{forum}/comment/edit/{selected}')
    Comment.edit_comment(request.form)
    return redirect(f'/forum/{forum}')

@app.route('/<forum>/comment/delete/<selected>')
def delete_comment(forum, selected):
    if not session:
        return redirect('/')
    Comment.delete_comment(selected)
    return redirect(f'/forum/{forum}')

