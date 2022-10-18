from flask_app import app, render_template, redirect, request, session
from flask_app.models.pet import Pet
from flask_app.models.post import Post

@app.route('/post/pet', methods=['POST'])
def new_post():
    if request.form['description'] == '':
        redirect(f"/dashboard/{request.form['name']}")
    Post.save(request.form)
    return redirect(f"/dashboard/{request.form['name']}")

@app.route('/delete/post/<int:id>')
def delete(id):
    data = {
        'id': id
    }
    Post.delete(data)
    pet_data = {
        'id': session['pet_id']
    }
    name = Pet.get_one_user_pet(pet_data)['name']
    return redirect(f"/dashboard/{name}")