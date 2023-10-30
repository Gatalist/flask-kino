from flask import Blueprint


users = Blueprint('app_users', __name__, template_folder='templates', static_folder='static')


# from .routes import login, logout, register, profile