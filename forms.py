from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, FileField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange, unique, Email

class Register(FlaskForm):
    """Form for navbar Search"""
    username = StringField("Username",validators=[InputRequired(),unique(User.username)],render_kw={"placeholder": "Username"})
    password = StringField("Password", validators=[InputRequired()], render_kw={"placeholder": "password"})
    email = StringField("Email", validators=[InputRequired(),Email(),unique(User.email)], render_kw={"placeholder": "email"})
    first_name = StringField("First Name", validators=[InputRequired()],render_kw={"placeholder": "first name"})
    last_name = StringField("Last Name", validators=[InputRequired()],render_kw={"placeholder": "last name"})

class Login(FlaskForm):
    """add pet to the database"""

    username = StringField("Username",validators=[InputRequired()],render_kw={"placeholder": "Username"})
    password = StringField("Password", validators=[InputRequired()], render_kw={"placeholder": "password"})

