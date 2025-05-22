# forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length , Email
from wtforms import ValidationError
import re

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=20)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=6)])
    email = StringField('Email', validators=[InputRequired(), Email()])
    submit = SubmitField('Register')


    def validate_password(self, field):
        password = field.data

        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        if not re.search(r"[A-Z]", password):
            raise ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r"[a-z]", password):
            raise ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r"\d", password):
            raise ValidationError("Password must contain at least one digit.")
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            raise ValidationError("Password must contain at least one special character.")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Login')


class TwoFactorForm(FlaskForm):
    code = StringField('Verification Code', validators=[InputRequired(), Length(min=6, max=6)])
    submit = SubmitField('Verify')

