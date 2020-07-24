"""Flask app for Feedback"""
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User
from forms import Register, Login

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback!!!'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()


@app.route('/')
def root():
    return render_template('home.html')

@app.route('/register')
def register_page():
    register_form = Register()
    return render_template('register.html', register_form=register_form)

@app.route('/register', methods=("POST"))
def register(): 
    register_form = Register()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data
        email = register_form.email.data
        first = register_form.first_name.data
        last = register_form.last_name.data
        user = User.register(username, password, email, first, last);
        db.session.add(user)
        db.session.commit()
        flash(f"Welcome {username}!")
        return redirect("/")

    else:
        return render_template("register.html", register_form=register_form)

@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=("POST"))
def login():
    return redirect('/')

@app.route('/secret')
def secret_page():
    return render_template('secret.html')