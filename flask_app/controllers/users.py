from flask_app import app, render_template, redirect, request, bcrypt, session, flash
from flask_app.models.user import User
from flask_app.models.pet import Pet

#* user login action
@app.route('/login', methods=['POST'])
def login():

    data = {"email": request.form["email"] }
    user = User.get_by_email(data)

    if not user:
        flash(u"Invalid Email/Password", 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash(u"Invalid Email/Password", 'login')
        return redirect('/')

    session['user_id'] = user.id
    return redirect('/pets/choose')

#* user login page
@app.route('/')
def index():
    return render_template('index.html')

#* user register page
@app.route('/users/register')
def register():
    return render_template('register.html')

#* user register action
@app.route('/users/create', methods=['POST'])
def register_user():

    if request.form['password']:
        pw_hash = bcrypt.generate_password_hash(request.form['password'])
    if not User.validate_user(request.form):
        return redirect('/users/register')

    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pw_hash
    }
    user_id = User.save(data)

    session['user_id'] = user_id
    return redirect("/pets/choose")


@app.route('/logout')
def logout():
    session.clear()
    print(session)
    return redirect('/')