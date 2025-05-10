from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app import db
from app.models import User
from werkzeug.security import generate_password_hash, check_password_hash


class LoginForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=32)]
    )
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Sign In")

    def validate_on_submit(self):
        rv = super().validate()
        if not rv:
            return False
        user = User.query.filter_by(username=self.username.data).first()
        if user is None:
            self.username.errors.append("Invalid username or password")
            return False
        if not check_password_hash(user.password_hash, self.password.data):
            self.password.errors.append("Invalid username or password")
            return False
        return True


class RegistrationForm(FlaskForm):
    username = StringField(
        "Username", validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField("Email", validators=[DataRequired(), Email(), Length(max=64)])
    password = PasswordField(
        "Password", validators=[DataRequired(), Length(min=6, max=32)]
    )
    password2 = PasswordField(
        "Repeat Password", validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Register")

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError(
                "Username already in use! Please choose a different one."
            )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError(
                "Email already in use! Please login or reset your password."
            )
