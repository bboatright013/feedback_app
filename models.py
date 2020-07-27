"""Models for flask-feedback app."""
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt 

db = SQLAlchemy()
bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """user Model"""

    __tablename__ = "users"

    @classmethod
    def register(cls, username, pwd, email, first, last):
        """Register user w/hashed password & return user."""
        hashed = bcrypt.generate_password_hash(pwd)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode("utf8")
        # return instance of user w/username and hashed pwd
        return cls(username=username, password=hashed_utf8, email=email, first_name=first, last_name=last)

    @classmethod
    def authenticate(cls, username, pwd):
        """Validate that user exists & password is correct.
        Return user if valid; else return False.
        """
        u = User.query.filter_by(username=username).first()
        if u and bcrypt.check_password_hash(u.password, pwd):
            # return user instance
            return u
        else:
            return False

    username = db.Column(db.String(20),primary_key=True, unique=True)
    password = db.Column(db.String,nullable=False)
    email = db.Column(db.String(50),nullable = False, unique=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)

    feedback = db.relationship('Feedback',cascade="all, delete-orphan", backref="feed")

class Feedback(db.Model):
    """feedback model"""
    __tablename__ = "feedback"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.String, db.ForeignKey('users.username'), nullable=False)



# class User_feedback(db.Model):
#     """feedback model"""
#     __tablename__ = "user_feedback"

#     feedback_id = db.Column(db.Integer, db.ForeignKey('feedback.id'),nullable=False,primary_key=True)
#     username = db.Column(db.String, db.ForeignKey('users.username'), nullable=False,primary_key=True)