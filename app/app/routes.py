from flask import jsonify  # , g
from app import app  # , login_manager


# migrations
from .movies.models import *
from .users.models import *


# blueprints
from app.movies import movie_blueprint
from app.users import user_blueprint
from app.api import api_blueprint


# Регистрируем Blueprints в приложении
app.register_blueprint(movie_blueprint, url_prefix='/')
app.register_blueprint(user_blueprint, url_prefix='/user/')
app.register_blueprint(api_blueprint, url_prefix='/api')


# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': f'{error}'}), 404


# Обработчик ошибки 500
@app.errorhandler(500)
def handle_500(error):
    return jsonify({'error': f'{error}'}), 500
