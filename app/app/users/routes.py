# from flask import render_template, flash, redirect, url_for, request
# from werkzeug.security import generate_password_hash, check_password_hash
# from werkzeug.urls import url_parse
# from flask_login import login_required, login_user, logout_user, current_user
# from app import db, login_manager
# from .models import Users
# from app.users import users


# @login_manager.user_loader
# def load_user(id):
#     return Users.query.get(int(id))


# @users.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('app_movies.view_movie'))


# @users.route('/register', methods=["POST", "GET"])
# def register():
#     if request.method == 'POST':
#         name = request.form['name']
#         email = request.form['email']
#         pwd_1 = request.form['pwd-1']
#         pwd_2 = request.form['pwd-2']
#         generate_hash_1 = generate_password_hash(pwd_1)

#         if len(name) < 3:
#             flash("Short name", "error_name")
#         elif email.find('@') == -1:
#             flash("Incorrect email", "error_email")
#         elif len(pwd_1) < 8:
#             flash("Password must be at least 8 characters long, contain a capital letter and symbols", "error_pwd")

#         elif not check_password_hash(generate_hash_1, pwd_2):
#             flash("Passwords do not match", "error_pwd-2")
#             # print("pasword - ok")
#         else:
#             try:
#                 user = Users(username=name, email=email, password=generate_hash_1)
#                 db.session.add(user)
#                 db.session.commit()
#                 flash("you have successfully registered")
#                 return redirect(url_for('app_users.login'))
#             except Exception as error:
#                 print(error)
#                 flash("Save error user in DataBase", "error_save")
#         print(name, email, pwd_1, pwd_2)
#     return render_template('register.html')


# @users.route('/login', methods=["POST", "GET"])
# def login():
#     if request.method == 'POST':
#         email = request.form['email']
#         password = request.form['pwd-1']
#         remember = request.form.get('remember', False)
#         print(email, password)
#         user = Users.query.filter_by(email=email).first()

#         if not user:
#             flash("No correct email or password", "error_save")
#             return redirect(url_for('app_users.login'))
        
#         if check_password_hash(user.password, password):
#             if remember:
#                 login_user(user, remember=remember)
#             else:
#                 login_user(user)
#             next_page = request.args.get('next')
#             if not next_page or url_parse(next_page).netloc != '':
#                 next_page = url_for('app_movies.view_movie')
#             return redirect(next_page)
#         else:
#             flash("No correct email or password", "error_save")
#             return redirect(url_for('app_users.login'))
#     return render_template('login.html', form=request.form)


# @users.route('/profile', methods=['GET', 'POST'])
# @login_required
# def profile():
#     user_id = current_user.id
#     user = Users.query.filter_by(id=user_id).first()
#     return render_template('user.html', user=user)
