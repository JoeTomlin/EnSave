from flask_app.config.mysqlconnection import connectToMySQL

from flask import flash

import re

from flask_app.models import user

class Product:
    db = "ensave_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.cost = data['cost']
        self.quantity = data['quantity']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.creator = None
        
    @classmethod
    def get_all_products(cls):
        query = "SELECT * FROM products JOIN users ON products.users_id = users.id;"
        results = connectToMySQL('ensave_schema').query_db(query)
        print(results)
        all_products = []
        if results:
            for row in results:
                product = cls(row)
                creator = user.User(row)
                product.creator = user.User(row)
                all_products.append(product)
        print(all_products)        
        return all_products
    
    @classmethod
    def save (cls, data):
        query = """INSERT INTO products (name, cost, quantity, created_at, updated_at, users_id) 
        VALUES (%(name)s, %(cost)s, %(quantity)s, NOW(), NOW(), %(users_id)s);"""
        print(data)
        return connectToMySQL('ensave_schema').query_db(query, data)
    
    @classmethod
    def update_product(cls,data):
        print(data)
        query = """UPDATE products SET name=%(name)s,cost=%(cost)s,quantity=%(quantity)s WHERE id = %(id)s;"""
        print(query)
        return connectToMySQL('ensave_schema').query_db(query,data)
    
    @classmethod
    def delete_product(cls, data):
        query = "DELETE FROM products WHERE id = %(id)s;"
        results = connectToMySQL('ensave_schema').query_db(query)
        print("query")
        return connectToMySQL('ensave_schema').query_db(query, data)
    
    @staticmethod
    def validate_product(product):
        is_valid = True
        results = connectToMySQL('ensave_schema').query_db(product)
        if len(product['name']) < 3:
            flash("Your product name must be at least 3 characters long.", "product")
            is_valid = False
        if len(product['cost']) < 1:
            flash("Your product has to cost something.", "product")
            is_valid = False
        if len(product['quantity']) < 1:
            flash("If you have less than 1 product, you might as well delete it.", "product")
            is_valid = False
        return is_valid