from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, IntegerField, BooleanField, FileField
from wtforms.validators import InputRequired, Optional, AnyOf, URL, NumberRange, email_validator, Email
from wtforms.fields.html5 import EmailField


class Register(FlaskForm):
    """Form for user registration"""
    username = StringField("Username",validators=[InputRequired()],render_kw={"placeholder": "Username"}, )
    password = StringField("Password", validators=[InputRequired()], render_kw={"placeholder": "password"})
    email = EmailField("Email", validators=[InputRequired(),Email()], render_kw={"placeholder": "email"})
    first_name = StringField("First Name", validators=[InputRequired()],render_kw={"placeholder": "first name"})
    last_name = StringField("Last Name", validators=[InputRequired()],render_kw={"placeholder": "last name"})

class Login(FlaskForm):
    """login form"""

    username = StringField("Username",validators=[InputRequired()],render_kw={"placeholder": "Username"})
    password = StringField("Password", validators=[InputRequired()], render_kw={"placeholder": "password"})

class GiveFeedback(FlaskForm):
    """add feedback"""
    title = StringField("Title", validators=[InputRequired()])
    content = StringField("Content", validators=[InputRequired()])


