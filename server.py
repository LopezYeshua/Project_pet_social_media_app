from flask_app import app
from flask_app.controllers import users, pets, posts, comments, likes

if __name__ == "__main__":
    app.run(debug=True)