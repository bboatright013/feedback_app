"""Flask app for Feedback"""
from flask import Flask, render_template, request, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Feedback
from forms import Register, Login, GiveFeedback
from sqlalchemy.exc import IntegrityError


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

db.create_all()

def serialize_feedback(feedback):
    """Serialize a feedback post SQLAlchemy obj to dictionary."""

    return {
        "id": feedback.id,
        "title": feedback.title,
        "content": feedback.content,
        "username": feedback.username
    }

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

@app.errorhandler(401)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('401.html'), 401


@app.route('/feedback')
def feedback():
    """returns json of feedback in db"""
    feedback = Feedback.query.order_by(Feedback.id.desc()).all()
    serialized = [serialize_feedback(feed) for feed in feedback]
    return jsonify(feedback=serialized)

@app.route('/feedback/<username>')
def user_feedback(username):
    """returns json of feedback in db"""
    feedback = Feedback.query.order_by(Feedback.id.desc()).filter_by(username=username)
    serialized = [serialize_feedback(feed) for feed in feedback]
    return jsonify(feedback=serialized)

@app.route('/user')
def get_username():
    user = User.query.get_or_404(session['username'])
    return user.username

@app.route('/')
def root():
    return render_template('home.html')

@app.route('/register')
def register_page():
    register_form = Register()
    return render_template('register.html', register_form=register_form)

@app.route('/register', methods=["POST"])
def register(): 
    register_form = Register()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data
        email = register_form.email.data
        first = register_form.first_name.data
        last = register_form.last_name.data
        user = User.register(username, password, email, first, last);
        userx = User.query.filter_by(username=username).first()
        if userx:
            flash(f"username {user.username} already taken")
            return redirect('/register')
        else:
            try:
                db.session.add(user)
                db.session.commit()
                session["username"] = user.username
                flash(f"Welcome {username}!")
                return redirect("/")
            except IntegrityError:
                db.session.rollback()
                flash('Username or Email already taken')
                return redirect('/register')
    else:
        return render_template("register.html", register_form=register_form)

@app.route('/login')
def login_page():
    login_form = Login()
    return render_template('login.html', login_form=login_form)

@app.route('/login', methods=["POST"])
def login():
    login_form = Login()
    if login_form.validate_on_submit():
        name = login_form.username.data
        pwd = login_form.password.data
        # authenticate will return a user or False
        user = User.authenticate(name, pwd)
        if user:
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")
        else:
            flash('incorrect username or password')
            return redirect('/login')
    return render_template("login.html", login_form=login_form)

@app.route('/users/<username>')
def secret_page(username):
    if "username" not in session:
        flash("You must be logged in to view!")
        return redirect("/")
    elif session['username'] != username:
        flash("Access only granted to your account")
        return redirect("/")        
    else:
        user = User.query.get_or_404(username)
        posts = Feedback.query.filter_by(username=username).all()
        return render_template('secret.html', user=user, posts=posts)

@app.route('/users/<username>/delete', methods=["POST","GET"])
def delete_user(username):
    if request.method == "POST":
        if "username" not in session:
            flash("You must be logged in to delete your account!")
            return redirect("/")
        elif session['username'] != username:
            flash("Access only granted to your account")
            return redirect("/")        
        else:
            user = User.query.get_or_404(username)
            db.session.delete(user)
            db.session.commit()
            session.pop("username")
            return redirect('/')
    else:
        user = User.query.get_or_404(username)
        return render_template("delete.html", user=user)

@app.route('/users/<username>/feedback/add', methods=["POST","GET"])
def give_feedback(username):
    give_feedback = GiveFeedback()
    user = User.query.get_or_404(username)

    if session['username'] != username:
        flash("Access only granted to your account")
        return redirect("/")      
    else:  
        if give_feedback.validate_on_submit():
            feedback = Feedback(title=give_feedback.title.data,content=give_feedback.content.data, username=session['username'])
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{session['username']}")
        else:
            return render_template("give_feedback.html", give_feedback=give_feedback, username=username)

@app.route('/feedback/<int:feedback_id>/update', methods=["POST","GET"])
def update_feedback(feedback_id):
    give_feedback = GiveFeedback()
    feedback = Feedback.query.get_or_404(feedback_id)
    if session['username'] != feedback.username:
        flash("Access only granted to your account")
        return redirect("/")      
    else:  
        if give_feedback.validate_on_submit():
            feedback.title = give_feedback.title.data
            feedback.content = give_feedback.content.data
            db.session.add(feedback)
            db.session.commit()
            return redirect(f"/users/{session['username']}")
        else:
            return render_template("update_feedback.html", give_feedback=give_feedback, feedback_id=feedback_id)

@app.route('/feedback/<int:feedback_id>/delete', methods=["POST"])
def delete_feedback(feedback_id):
    feed = Feedback.query.get_or_404(feedback_id)
    if session['username'] != feed.username:
        flash("Access only granted to your account")
        return redirect("/")      
    else:  
        feedback = Feedback.query.get_or_404(feedback_id)
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/users/{session['username']}")


@app.route('/logout')
def logout():
    """Logs user out and redirects to homepage."""
    session.pop("username")
    return redirect("/")    