from flask_wtf import Form
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
from wtforms import PasswordField
from wtforms import TextField
from wtforms.validators import EqualTo
from wtforms.validators import InputRequired

from my_app import db


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(100))
    pwdhash = Column(String())

    def __init__(self, username, password):
        self.username = username
        self.pwdhash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pwdhash, password)


class RegistrationForm(Form):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField(
        'Password',
        validators=[
            InputRequired(),
            EqualTo('confirm', message='Passwords must match'),
        ]
    )
    confirm = PasswordField('Confirm Password', validators=[InputRequired()])


class LoginForm(Form):
    username = TextField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
