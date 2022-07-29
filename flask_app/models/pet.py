from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = "pets"

class Pet:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.animal = data['animal']
        self.name = data['name']
        self.gender = data['gender']
        self.breed = data['breed']
        self.dob = data['dob']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if "parent_name" in data:
            self.parent_name = data['parent_name']


    # CREATE
    @classmethod
    def save(cls, data):
        query = "INSERT INTO pets (animal, name, gender, breed, dob, user_id) VALUES (%(animal)s, %(name)s, %(gender)s, %(breed)s, %(dob)s, %(user_id)s)"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def add_friend(cls, data):
        query = "INSERT INTO friends (pet_id, friend_id) VALUES (%(pet_id)s, %(friend_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def send_message(cls, data):
        pass

    # READ
    @classmethod
    def get_all_pets(cls):
        query = "SELECT * FROM pets;"
        return connectToMySQL(DATABASE).query_db( query )

    @classmethod
    def get_all_user_pets(cls, data):
        query = "SELECT * FROM pets JOIN users ON pets.user_id = users.id WHERE users.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        pets = []
        for result in results:
            user_pets = {
                'id': result['id'],
                'animal': result['animal'],
                'name': result['name'],
                'gender': result['gender'],
                'breed': result['breed'],
                'dob': result['dob'],
                'user_id': result['user_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
                'parent_name': result['first_name']
            }
            pets.append( Pet(user_pets) )

        return pets

    @classmethod
    def get_one_user_pet(cls, data):
        query = "SELECT * FROM pets JOIN users ON pets.user_id = users.id WHERE pets.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        result = results[0]
        return result

    @classmethod
    def get_users_first_pet(cls, data):
        query = "SELECT * FROM pets JOIN users ON pets.user_id = users.id WHERE users.id = %(id)s LIMIT 1;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        result=[]
        if results:
            result = results[0]
        return result

    @classmethod
    def get_all_pet_friends(cls, data):
        query = "SELECT friend_id, pets2.*, pets.name as friender, pets2.name as friended FROM pets LEFT JOIN friends ON pets.id = friends.pet_id LEFT JOIN pets as pets2 ON pets2.id = friends.friend_id WHERE pets.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db( query, data )
        friends = []
        for result in results:
            friend_data = {
                'id': result['id'],
                'animal': result['animal'],
                'name': result['name'],
                'gender': result['gender'],
                'breed': result['breed'],
                'dob': result['dob'],
                'user_id': result['user_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
            }
            friends.append( Pet(friend_data) )
        return friends

    # VALIDATE
    @staticmethod
    def validate_pet(pet):
        is_valid = True
        if len(pet['first_name']) < 2:
            flash("first name must be at least 2 characters.", 'first_name')
            is_valid = False
        if len(pet['last_name']) < 2:
            flash("last name must be at least 2 characters.", 'last_name')
            is_valid = False
        return is_valid