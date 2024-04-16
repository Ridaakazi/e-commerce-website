from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired
from wtforms.validators import InputRequired, NumberRange,Length, ValidationError,Email
from .models import User
from flask import flash


class SearchForm(FlaskForm):
    searched = StringField("Searched",validators=[InputRequired()])
    submit = SubmitField("Submit")

class RegisterForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Username"})
    email = StringField(validators=[Email(), Length(max=50)], render_kw={"placeholder": "Email"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError("That username already exists. Please use a different one.")

    def validate_email(self, email):
        existing_user_email = User.query.filter_by(email=email.data).first()
        if existing_user_email:
            raise ValidationError("That email is already in use. Please use a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=40)], render_kw={"placeholder": "Password"})
    submit = SubmitField("Login")

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(
            username=username.data).first()

        if not existing_user_username:
            flash("Username does not exist. Please register first.", "danger")
            raise ValidationError()

  

