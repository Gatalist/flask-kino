from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_admin import Admin
from loguru import logger
from flasgger import Swagger
from .swagger import template, swagger_config


db = SQLAlchemy()
migrate = Migrate(compare_type=True)
admin = Admin()
swagger = Swagger(config=swagger_config, template=template)
login_manager = LoginManager()

# loging loguru
logger.add(
    "logs/logs_app/debug.log",
    format="{time} - [{level}] : {message}",
    level="DEBUG",
    rotation="100 KB")

