from flask_app.config.mysqlconnection import connectToMySQL

DATABASE = "pets"

class Like:
    def __init__(self, data) -> None:
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        if 'post_id' in data:
            self.post_id = data['post_id']
        if 'likes' in data:
            self.likes = data['likes']
        if 'comment_id' in data:
            self.comment_id = data['comment_id']
        self.pet_id = data['pet_id']


    # CREATE
    @classmethod
    def save_post_like(cls, data):
        query = "INSERT INTO post_likes (post_id, pet_id) VALUES (%(post_id)s, %(pet_id)s);"
        return connectToMySQL(DATABASE).query_db( query, data )

    @classmethod
    def save_comment_like(cls, data):
        query = "INSERT INTO comment_likes (comment_id, pet_id) VALUES (%(comment_id)s, %(pet_id)s)"
        return connectToMySQL(DATABASE).query_db( query, data )

    # READ
    @classmethod
    def get_all_post_likes_data(cls):
        query = "SELECT * FROM post_likes;"
        results = connectToMySQL(DATABASE).query_db( query)
        likes = []
        for result in results:
            post_likes = {
                'id': result['id'],
                'post_id': result['post_id'],
                'pet_id': result['pet_id'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
            }
            likes.append( Like(post_likes) )

        return likes

    @classmethod
    def get_all_post_likes_count(cls):
        query = "SELECT post_likes.*, COUNT(posts2.description) as likes FROM posts LEFT JOIN post_likes ON posts.id = post_likes.post_id LEFT JOIN posts as posts2 ON posts2.id = post_likes.post_id GROUP BY posts.id;"
        results = connectToMySQL(DATABASE).query_db( query)
        likes = []
        for result in results:
            post_likes = {
                'id': result['id'],
                'post_id': result['post_id'],
                'pet_id': result['pet_id'],
                'likes': result['likes'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
            }
            likes.append( Like(post_likes) )

        return likes

    @classmethod
    def get_all_comment_likes_count(cls):
        query = "SELECT comment_likes.*, COUNT(comments2.description) as likes FROM comments LEFT JOIN comment_likes ON comments.id = comment_likes.comment_id LEFT JOIN comments as comments2 ON comments2.id = comment_likes.comment_id GROUP BY comments.id;"
        results = connectToMySQL(DATABASE).query_db( query)
        likes = []
        for result in results:
            comment_likes = {
                'id': result['id'],
                'comment_id': result['comment_id'],
                'pet_id': result['pet_id'],
                'likes': result['likes'],
                'created_at': result['created_at'],
                'updated_at': result['updated_at'],
            }
            likes.append( Like(comment_likes) )

        return likes