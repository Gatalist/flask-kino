from flask import jsonify


# blueprints
from app.movies import movie_blueprint
from app.users import user_blueprint
from app.api import api_blueprint
from app.backup import backup_blueprint


def init_bp(app):
    #  Регистрируем Blueprints в приложении
    app.register_blueprint(movie_blueprint, url_prefix='/')
    app.register_blueprint(user_blueprint, url_prefix='/user/')
    app.register_blueprint(api_blueprint, url_prefix='/api/')
    app.register_blueprint(backup_blueprint)

    #  обработчики ошибок
    @app.errorhandler(404)
    def page_not_found(error):
        # Обработчик ошибки 404
        return jsonify({'error': f'{error}'}), 404

    @app.errorhandler(500)
    def handle_500(error):
        # Обработчик ошибки 500
        return jsonify({'error': f'{error}'}), 500

    return app
