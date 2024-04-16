import sys
from flask import Flask
from app.settings import ProdConfig, DevConfig
from .extensions import db, admin, login_manager, swagger, migrate
from .routes import init_bp


def create_app(config_class):
    new_app = Flask(__name__)
    new_app.config.from_object(config_class)
    sys.path.append(new_app.config['ROOT_PATH'])  # add root path
    new_app.permanent_session_lifetime = new_app.config['SESSION_LIFETIME']  # lifetime session

    db.init_app(new_app)
    migrate.init_app(new_app, db)

    login_manager.init_app(new_app)
    login_manager.login_view = 'users.load_user'

    admin.init_app(new_app)
    admin.name = "FilmNet"
    admin.icon_url = new_app.config['ADMIN_ICON_PATH']

    swagger.init_app(new_app)

    init_bp(new_app)

    @new_app.shell_context_processor
    def make_shell_context():
        return {"app": new_app, "db": db}

    return new_app


app = create_app(config_class=DevConfig)
