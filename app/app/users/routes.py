from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user, login_required
from urllib.parse import urlparse
from app import login_manager, db  # , bcrypt
from .models import User
from .forms import LoginForm, RegisterForm
from werkzeug.security import generate_password_hash


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# @login_manager.request_loader
# def load_user_api(user_id):
#     from app.users.models import User
#     # Загрузка пользователя из базы данных или хранилища
#     return User.query.get(user_id) #.first()


def login():
    if current_user.is_authenticated:
        return redirect(url_for('app_movies.home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        login_user(user)  # , remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or urlparse(next_page).netloc != '':
            next_page = url_for('app_movies.home')
        return redirect(next_page)
    print(form.errors)
    return render_template('login-2.html', title='Sign In', form=form)


def logout():
    logout_user()
    return redirect(url_for('app_user.login'))


def register():
    if current_user.is_authenticated:
        return redirect(url_for('app_movies.home'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.username.data
        email = form.email.data

        hashed_pwd = generate_password_hash(form.password.data)
        user = User(username=name, email=email, password=hashed_pwd)

        db.session.add(user)
        db.session.commit()
        return redirect(url_for('app_user.login'))
    return render_template('register-2.html', title='Register', form=form)


def profile():
    # Получаем текущего пользователя
    user = current_user
    return render_template('profile.html', user=user)
