from flask_app import app, render_template, redirect, request, session
from flask_app.models.pet import Pet
from flask_app.models.post import Post

@app.route('/post/pet', methods=['POST'])
def new_post():
    if request.form['description'] == '':
        redirect(f"/dashboard/{request.form['name']}")
    Post.save(request.form)
    return redirect(f"/dashboard/{request.form['name']}")