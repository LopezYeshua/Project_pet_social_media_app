from flask_app import app, render_template, redirect, session, request
from flask_app.models.comment import Comment

@app.route('/comment/post', methods=['POST'])
def new_comment():
    data = {
        'pet_id': session['pet_id'],
        'post_id': request.form['post_id'],
        'description': request.form['description']
    }
    Comment.save(data)
    return redirect(f"/dashboard/{request.form['name']}")