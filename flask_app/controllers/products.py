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