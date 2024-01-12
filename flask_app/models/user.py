from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "ensave_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['name']
        self.email = data['email']
        self.last_name = data['state']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.products = []
        
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL('ensave_schema').query_db(query)
        users = []
        for row in results:
            users.append(cls[row])
        return users