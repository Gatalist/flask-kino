import sys
from time import sleep

from flask import Flask
from flask_cors import CORS
from flask.signals import request_started, request_finished, appcontext_pushed
from sqlalchemy import inspect
from .settings import ProdConfig, DevConfig
from .extensions import db, admin, login_manager, swagger, migrate
from .users.default_objects import DefaultObjectsDB
from .routes import init_bp


def create_app(config_class):
    new_app = Flask(__name__)
    new_app.config.from_object(config_class)
    sys.path.append(new_app.config['ROOT_PATH'])  # add root path
    # new_app.permanent_session_lifetime = new_app.config['SESSION_LIFETIME']  # lifetime session

    db.init_app(new_app)
    migrate.init_app(new_app, db)

    login_manager.init_app(new_app)
    login_manager.login_view = 'users.load_user'

    admin.init_app(new_app)
    admin.icon_url = new_app.config['ADMIN_ICON_PATH']

    swagger.init_app(new_app)

    init_bp(new_app)

    @new_app.shell_context_processor
    def make_shell_context():
        return {"app": new_app, "db": db}

    return new_app


app = create_app(config_class=DevConfig)


def create_objects():
    print("✅ Request finished!")
    inspector = inspect(db.engine)
    if inspector.has_table("users"):
        default_objects = DefaultObjectsDB(app, db)
        default_objects.has_tables_db()

with app.app_context():
    create_objects()
