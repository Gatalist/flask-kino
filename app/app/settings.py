import os
import datetime
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)


class Config(object):
    HOST: str = "0.0.0.0"

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SESSION_LIFETIME = datetime.timedelta(days=10)

    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    STATIC_PATH = os.path.join(ROOT_PATH, 'static')
    TEMPLATES_PATH = os.path.join(ROOT_PATH, 'templates')
    MEDIA_PATH = os.path.join(STATIC_PATH, 'media')
    ADMIN_ICON_PATH = os.path.join(STATIC_PATH, 'cms.ico')

    PAGINATE_ITEM_IN_PAGE: int = 20

    TOKEN_NAME = "Access-Token"

    ADMIN_URL = "/admin"
    SECURITY_URL_PREFIX = ADMIN_URL
    SECURITY_LOGIN_URL = "/login/"
    SECURITY_LOGOUT_URL = "/logout/"
    SECURITY_POST_LOGIN_VIEW = ADMIN_URL
    SECURITY_POST_LOGOUT_VIEW = ADMIN_URL
    SECURITY_POST_REGISTER_VIEW = ADMIN_URL

    # Включает регистрацию
    SECURITY_REGISTERABLE = True
    SECURITY_REGISTER_URL = "/register/"
    SECURITY_SEND_REGISTER_EMAIL = False

    # Включает сброс пароля
    SECURITY_RECOVERABLE = True
    SECURITY_RESET_URL = "/reset/"
    SECURITY_SEND_PASSWORD_RESET_EMAIL = True

    # Включает изменение пароля
    SECURITY_CHANGEABLE = True
    SECURITY_CHANGE_URL = "/change/"
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False

    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_SALT')
    SECURITY_PASSWORD_HASH = os.getenv('SECURITY_HASH')


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG: bool = True
    PORT: int = 5000

    # CSRF_ENABLED = True

    db_uri: str = os.getenv('DB_URI')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_name: str = os.getenv('DB_NAME')  # database name
    db_addr: str = os.getenv('DB_ADDR')  # container_name to docker

    SQLALCHEMY_DATABASE_URI = f'{db_uri}://{db_user}:{db_pass}@{db_addr}/{db_name}'


class ProdConfig(Config):
    DEBUG: bool = False
    PORT: int = 5000

    CSRF_ENABLED = True

    db_uri: str = os.getenv('DB_URI')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_name: str = os.getenv('DB_NAME')  # database name
    db_addr: str = os.getenv('DB_ADDR')  # container_name to docker

    SQLALCHEMY_DATABASE_URI = f'{db_uri}://{db_user}:{db_pass}@{db_addr}/{db_name}'


class TestingConfig(Config):
    TESTING = True
    DEBUG: bool = True
    PORT: int = 5001
    # Отключаем CSRF для тестов
    WTF_CSRF_ENABLED = False
    CSRF_ENABLED = False

    db_uri: str = os.getenv('DB_URI')
    db_user: str = os.getenv('DB_USER')
    db_pass: str = os.getenv('DB_PASS')
    db_name: str = os.getenv('DB_NAME')  # database name
    # db_name: str = os.getenv('test_db_name')  # database name
    db_addr: str = os.getenv('DB_ADDR')  # container_name to docker

    SQLALCHEMY_DATABASE_URI = f'{db_uri}://{db_user}:{db_pass}@{db_addr}/{db_name}'


