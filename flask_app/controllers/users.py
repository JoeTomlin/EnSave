from flask import redirect, render_template, request, session, flash

from flask_app import app

from flask_app.models.user import User
from flask_app.models.product import Product

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/registration')
def registration():
    return render_template("registration.html")

@app.route('/login', methods=['POST'])
def login():
    print("hello")
    print(request.form)
    data = { 
        "username": request.form["username"]
    }
    print("HI")
    user_in_db = User.get_by_username(data)
    if not user_in_db:
        flash("Invalid Username")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect("/home")

@app.route('/register', methods=['POST'])
def register():
    print("data")
    print(request.form)
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        "name": request.form["name"],
        "email": request.form["email"],
        "state": request.form["state"],
        "username": request.form["username"],
        "password": bcrypt.generate_password_hash(request.form["password"]),
        "pswd_confirm": bcrypt.generate_password_hash(request.form["pswd_confirm"])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect("/")

@app.route('/profile')
def profile():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id": session["user_id"]
    }
    return render_template("profile.html", user=User.get_by_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')