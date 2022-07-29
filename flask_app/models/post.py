from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = "pets"

class Post:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.description = data['description']
        self.pet_id = data['pet_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if data['animal']:
            self.animal = data['animal']
        if data['name']:
            self.name = data['name']


    # CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO posts (description, pet_id) VALUES (%(description)s, %(pet_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    # READ
    @classmethod
    def get_all_posts(cls):
        query = "SELECT * FROM posts JOIN pets ON posts.pet_id = pets.id;"
        results = connectToMySQL(DATABASE).query_db( query)
        posts = []
        for result in results:
            user_posts = {
                'id': result['id'],
                'description': result['description'],
                'pet_id': result['pet_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'animal': result['animal'],
                'name': result['name']
            }
            posts.append( Post(user_posts) )

        return posts
    

    # VALIDATE
    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['first_name']) < 2:
            flash("first name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(post['last_name']) < 2:
            flash("last name must be at least 2 characters.", 'last_name')
            is_valid = False
        return is_valid