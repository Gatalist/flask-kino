from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FileField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, InputRequired, Length
from .models import User
import re


class RegisterForm(FlaskForm):
    username = StringField(
        label='Username',
       validators=[InputRequired(), Length(min=3, max=50)],
       render_kw={"placeholder": "Username"}
    )

    email = StringField(
        label='Email',
        validators=[DataRequired(), Email()],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
        label='Password',
        # validators=[InputRequired(), Length(min=8, max=20)],
        render_kw={"placeholder": "Password"}
    )

    password2 = PasswordField(
        label='Repeat Password',
        validators=[DataRequired(), EqualTo('password')],
        render_kw={"placeholder": "Repeat Password"}
    )

    def validate_username(self, username):
        existing_user_username = User.query.filter_by(username=username.data).first()
        if existing_user_username:
            raise ValidationError('Please use a unique name')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('email already exists')

    def validate_password(self, password):
        pwd = password.data
        errors = []

        if len(pwd) < 8 or len(pwd) > 20:
            errors.append('Field must be between 8 and 20 characters long')

        # Проверка наличия буквы
        if not re.findall(r"\w", pwd):
            errors.append('Password must contain at least one letter')

        # проверка наличия большой буквы
        if not re.findall(r'[A-Z]', pwd):
            errors.append('Password must contain at big letter')

        if not re.findall(r'[a-z]', pwd):
            errors.append('Password must contain at little letter')

        # Проверка наличия цифры
        if not re.findall(r"[^\d]", pwd):
            errors.append('Password must contain at least one digit')

        # Проверка наличия специальных символов
        if not re.findall(r"[^\w\d]", pwd):
            errors.append('Password must contain at least one special character')

        # Проверка отсутствия пробелов
        if re.search(r'\s', pwd):
            errors.append('Password must not contain spaces')

        if errors:
            print(errors)
            raise ValidationError(errors)


class LoginForm(FlaskForm):
    email = StringField(
        label='Email',
        validators=[DataRequired()],
        render_kw={"placeholder": "Email"}
    )

    password = PasswordField(
        validators=[InputRequired()],
        render_kw={"placeholder": "Password"}
    )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if not user:
            raise ValidationError('email not registered')

    @staticmethod
    def validate_password(form, field):
        pwd = form.password.data
        email = form.email.data
        user = User.query.filter_by(email=email).first()
        # Проверка пароля пользователя
        if not user or not user.check_password(pwd):
            raise ValidationError('Incorrect password')
