from flask import redirect, render_template, request, session, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.product import Product

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/home')
def product_table():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session["user_id"]
    }
    products = Product.get_all_products()
    return render_template("home.html", user=User.get_by_id(data), products=products)

@app.route('/add/product', methods=['POST'])
def add_product():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Product.validate_product(request.form):
        return redirect('/home')
    data = {
        "name": request.form["name"],
        "cost": request.form["cost"],
        "quantity": request.form["quantity"],
        "users_id": session["user_id"]
    }
    print("hello")
    Product.save(data)
    return redirect('/home')

@app.route('/product/update', methods=['POST'])
def update_product():
    if not Product.validate_product(request.form):
        return redirect('/home')
    data = {
        "id": request.form['id'],
        "name": request.form["name"],
        "cost": request.form["cost"],
        "quantity": request.form["quantity"],
        "users_id": session["user_id"]
    }
    Product.update_product(data)
    return redirect('/home')

@app.route('/product/<int:id>/delete')
def delete_product(id):
    data = {
        "id":id
    }
    Product.delete_product(data)
    return redirect('/home')