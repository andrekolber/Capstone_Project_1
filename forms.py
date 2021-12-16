from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

class SignUpForm(FlaskForm):
    """Form for signing up a new user."""

    username = StringField('Username:', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8)])
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])
    email = StringField('E-mail:', validators=[InputRequired(), Email()])

class LoginForm(FlaskForm):
    """Form for logging in a user."""

    username = StringField('Username:', validators=[InputRequired(), Length(min=1, max=20)])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8)])

class UserEditForm(FlaskForm):
    """Form for editing a user."""

    username = StringField('Username:', validators=[InputRequired(), Length(min=1, max=20)])
    email = StringField('E-mail:', validators=[InputRequired(), Email()])
    first_name = StringField('First Name:', validators=[InputRequired()])
    last_name = StringField('Last Name:', validators=[InputRequired()])
    password = PasswordField('Password:', validators=[InputRequired(), Length(min=8)])
