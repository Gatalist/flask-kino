from flask import jsonify
from app import app

# migrations
from .movies.models import *
from .users.models import *

# blueprints
from app.movies import movie_blueprint
from app.users import user_blueprint

# Регистрируем Blueprints в приложении
app.register_blueprint(movie_blueprint, url_prefix='/')
app.register_blueprint(user_blueprint, url_prefix='/user')


# Обработчик ошибки 404
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'error': f'{error}'}), 404


# Обработчик ошибки 500
@app.errorhandler(500)
def handle_500(error):
    return jsonify({'error': f'{error}'}), 500
