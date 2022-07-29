
from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = "pets"

class Comment:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.description = data['description']
        self.post_id = data['post_id']
        self.pet_id = data['pet_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if data['name']:
            self.name = data['name']


    # CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (description, post_id, pet_id) VALUES (%(description)s, %(post_id)s, %(pet_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    # READ
    @classmethod
    def get_all_comments(cls):
        query = "SELECT * FROM comments JOIN pets ON comments.pet_id = pets.id;"
        results = connectToMySQL(DATABASE).query_db( query)
        comments = []
        for result in results:
            user_comments = {
                'id': result['id'],
                'description': result['description'],
                'post_id': result['post_id'],
                'pet_id': result['pet_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'name': result['name']
            }
            comments.append( Comment(user_comments) )

        return comments

    @classmethod
    def get_one_user_comment(cls, data):
        query = "SELECT * FROM comments JOIN pets ON comments.user_id = users.id WHERE pets.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        result = results[0]
        return result

    # VALIDATE
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['first_name']) < 2:
            flash("first name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(comment['last_name']) < 2:
            flash("last name must be at least 2 characters.", 'last_name')
            is_valid = False
        if not EMAIL_REGEX.match(comment['email']): 
            flash("Invalid email address!", 'email')
            is_valid = False
        if len(comment['password']) < 8:
            flash("password too short.", 'password')
            is_valid = False
        if comment['password'] != comment['password_confirmation']:
            flash("Passwords do not match.", 'password_confirmation')
            is_valid = False
        if comment['password'].isalpha() and comment['password'].isdigit() == False:
            flash("Password must have: 1 uppercase letter, 1 number.", 'password')
            is_valid = False
        return is_valid