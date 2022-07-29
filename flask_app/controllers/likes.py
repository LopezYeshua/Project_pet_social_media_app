from flask_app import app, render_template, redirect, request, session
from flask_app.models.like import Like
from flask_app.models.pet import Pet

@app.route('/like/post/<int:id>')
def like(id):
    data = {
        'pet_id': session['pet_id'],
        'post_id': id
    }
    Like.save_post_like(data)
    pet_data = {
        'id': session['pet_id']
    }
    name = Pet.get_one_user_pet(pet_data)['name']
    return redirect(f"/dashboard/{name}")

@app.route('/like/comment/<int:id>')
def like_comment(id):
    data = {
        'pet_id': session['pet_id'],
        'comment_id': id
    }
    Like.save_comment_like(data)
    pet_data = {
        'id': session['pet_id'],
    }
    name = Pet.get_one_user_pet(pet_data)['name']
    return redirect(f"/dashboard/{name}")