import sys, datetime
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from app.settings import Config
from loguru import logger



app = Flask(__name__)
app.config.from_object(Config)


# add root path
sys.path.append(app.config.get('ROOT_PATH'))

# life time session
app.permanent_session_lifetime = datetime.timedelta(days=10)

# flask login
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'

# test client for unit test
client = app.test_client()

# create instance DataBase
db = SQLAlchemy(app)

# class instance Migrate
migrate = Migrate(app, db, compare_type=True)

# шыфрование
bcrypt = Bcrypt(app)

# logging loguru
logger.add(
    "loggs/loggs_app/debug.log", 
    format="{time} - [{level}] : {message}", 
    level="DEBUG", 
    rotation="100 KB")

# migrations
from .movies.models import *
from .users.models import *


@app.shell_context_processor
def make_shell_context():
    return {"app": app, "db": db}
