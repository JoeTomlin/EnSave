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