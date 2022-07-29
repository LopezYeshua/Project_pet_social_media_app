from flask_app import app, render_template, redirect, request, session
from flask_app.models.pet import Pet
from flask_app.models.comment import Comment
from flask_app.models.post import Post
from flask_app.models.like import Like

@app.route('/pets/choose')
def choose_pets():
    data = {'id': session['user_id']}
    return render_template('pets.html', pets=Pet.get_all_user_pets(data))

@app.route('/pets/new')
def new_pets():
    return render_template('new_pet.html')

@app.route('/create/pet', methods=['POST'])
def create_pet():
    Pet.save(request.form)
    return redirect(f"/dashboard/{request.form['name']}")

#* START OF PET DASHBOARD CONTROLLER
@app.route('/dashboard/<string:displayed_pet>')
def dashboard(displayed_pet):
    data = {'id': session['user_id']}
    user_pet = {}
    pet_data = {}
    pets = Pet.get_all_user_pets(data)
    for pet in pets:
        if pet.name == displayed_pet:
            session['pet_id'] = pet.id
            pet_data = {'id': session['pet_id']}
            user_pet=Pet.get_one_user_pet(pet_data)
            print(pet)
    posts = Post.get_all_posts()
    if posts:
        posts.reverse()
    comments = Comment.get_all_comments()
    post_likes = Like.get_all_post_likes_count()
    friends = Pet.get_all_pet_friends(pet_data)
    comment_likes = Like.get_all_comment_likes_count()
    
    return render_template('/dashboard.html', pets=pets, pet=user_pet, posts=posts, comments=comments, post_likes=post_likes, friends = friends, comment_likes=comment_likes)

@app.route('/message/pet/<int:id>', methods=['POST'])
def message(id):
    friend_data = {'id': id}
    pet_data = {'id': session['pet_id']}
    user_pet=Pet.get_one_user_pet(pet_data)
    return redirect(f"/dashboard/{user_pet['name']}")

#* START OF PET FRIENDS CONTROLLER
@app.route('/pets/friends')
def pet_friends():
    pet_data = {'id': session['pet_id']}
    pet = Pet.get_one_user_pet(pet_data)
    all_pets = Pet.get_all_pets()
    friends = Pet.get_all_pet_friends(pet_data)
    return render_template('friends.html', all_pets = all_pets, pet=pet, friends = friends)

@app.route('/friend/pet/<int:num>')
def add_friend(num):
    data = {
        'friend_id': num,
        'pet_id': session['pet_id'],
    }
    Pet.add_friend(data)
    return redirect('/pets/friends')


#* START OF PET PROFILE CONTROLLER
@app.route('/pets/profile')
def pet_profile():
    pet_data = {'id': session['pet_id']}
    return render_template('pet_profile.html', pet = Pet.get_one_user_pet(pet_data))