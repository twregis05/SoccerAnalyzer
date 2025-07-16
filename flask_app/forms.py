from ast import Pass
from flask_login import current_user
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from wtforms import StringField, SubmitField, TextAreaField, PasswordField, RadioField
from wtforms.validators import (
    InputRequired,
    Length,
    Email,
    EqualTo,
    ValidationError,
    Regexp
)


from .models import User


class SearchForm(FlaskForm):
    search_query = StringField(
        "Query", validators=[InputRequired(), Length(min=1, max=100)]
    )
    submit = SubmitField("Search")



class RegistrationForm(FlaskForm):
    first_name = StringField(
        "First name", validators=[InputRequired(), Length(min=1, max=40), Regexp(r'^[A-Za-z]+$', message="First name must contain only letters.")]
    )

    last_name = StringField(
        "Last name", validators=[InputRequired(), Length(min=1, max=40), Regexp(r'^[A-Za-z]+$', message="Last name must contain only letters.")]
    )
    username = StringField(
        "Username", validators=[InputRequired(), Length(min=1, max=40)]
    )
    email = StringField("Email", validators=[InputRequired(), Email()])
    password = PasswordField("Password", validators=[InputRequired()])
    confirm_password = PasswordField(
        "Confirm Password", validators=[InputRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

    def validate_email(self, email):
        user = User.objects(email=email.data).first()
        if user is not None:
            raise ValidationError("Email is taken")


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])
    submit = SubmitField('Submit')

class UpdateUsernameForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(), Length(min=1, max=40)])
    submit_username = SubmitField('Update')

    def validate_username(self, username):
        user = User.objects(username=username.data).first()
        if user is not None:
            raise ValidationError("Username is taken")

class UpdateProfilePicForm(FlaskForm):
    picture = FileField("Profile Picture", validators=[FileRequired(), FileAllowed(['jpg', 'png'], "File does not have an approved extension: jpg, png")])
    submit_picture = SubmitField('Update')
