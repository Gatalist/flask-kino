import sys
import datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
# from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from loguru import logger
from flask_admin import Admin
from flask_restful import Api
from flasgger import Swagger
from app.settings import Config
from .swagger import template, swagger_config


app = Flask(__name__)
app.config.from_object(Config)

# add root path
sys.path.append(app.config.get('ROOT_PATH'))

# lifetime session
app.permanent_session_lifetime = datetime.timedelta(days=Config.session_lifetime)

# flask login
# login_manager = LoginManager(app)
# login_manager.login_view = 'users.login'

# test client for unit test
client = app.test_client()

# create instance DataBase
db = SQLAlchemy(app)

# class instance Migrate
migrate = Migrate(app, db, compare_type=True)

# шифрование
bcrypt = Bcrypt(app)

# admin panel
admin = Admin(app)

# API and documentation
api = Api(app)
# api_docs = Apispec_docs(app)
swagger = Swagger(app, config=swagger_config, template=template)

# loging loguru
logger.add(
    "logs/logs_app/debug.log",
    format="{time} - [{level}] : {message}",
    level="DEBUG",
    rotation="100 KB")


@app.shell_context_processor
def make_shell_context():
    return {"app": app, "db": db}
