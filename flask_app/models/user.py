from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class User:
    db = "ensave_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.email = data['email']
        self.state = data['state']
        self.username = data['username']
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
    
    @classmethod
    def save(cls, data):
        query = """INSERT INTO ensave_schema.users (name, email, state, username, password, created_at, updated_at) 
        VALUES (%(name)s, %(email)s, %(state)s, %(username)s, %(password)s, NOW(), NOW());"""
        return connectToMySQL('ensave_schema').query_db(query, data)
    
    @classmethod
    def get_by_username(cls,data):
        query = "SELECT * FROM users WHERE username = %(username)s;"
        result = connectToMySQL('ensave_schema').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @classmethod
    def get_by_id(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL('ensave_schema').query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        query = "SELECT * FROM ensave_schema.users WHERE email = %(email)s;"
        results = connectToMySQL('ensave_schema').query_db(query, user)
        if len(results) >= 1:
            flash("Email already in use.", "register")
            is_valid = False
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email.", "register")
            is_valid = False
        if len(user['name']) < 2:
            flash("Your name must be at least 2 characters.", "register")
            is_valid = False
        if len(user['username']) < 8:
            flash("Your username must be at least 8 characters.", "register")
            is_valid = False
        if len(user['password']) < 8:
            flash("Your password must be at least 8 characters.", "register")
            is_valid = False
        if user['password'] != user['pswd_confirm']:
            flash("Password does not match", "register")
            is_valid = False 
        return is_valid
    