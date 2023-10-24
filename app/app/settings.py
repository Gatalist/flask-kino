import os
from dotenv import load_dotenv
from pathlib import Path


dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)



class Config(object):
    DEBUG: bool = True
    HOST: str = "0.0.0.0"
    
    PORT: int = 5000

    # db_uri: str = 'postgresql'
    db_uri: str = os.getenv('db_uri')
    db_user: str = os.getenv('db_user')
    db_pass: str = os.getenv('db_pass')
    db_name: str = os.getenv('db_name')  # data base name
    db_addr: str = os.getenv('db_addr')  # container_name to docker

    # TESTING = False
    # CSRF_ENABLED = True

    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = f'{db_uri}://{db_user}:{db_pass}@{db_addr}/{db_name}'
    
    ROOT_PATH = os.path.abspath(os.path.dirname(__file__))
    STATIC_PATH = os.path.join(ROOT_PATH, 'static')
    TEMPLATES_PATH = os.path.join(ROOT_PATH, 'templates')
    MEDIA_PATH = os.path.join(STATIC_PATH, 'media')
    PAGINATE_ITEM_IN_PAGE: int = 12


    # URLs
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

    # Включет сброс пароля
    SECURITY_RECOVERABLE = True
    SECURITY_RESET_URL = "/reset/"
    SECURITY_SEND_PASSWORD_RESET_EMAIL = True

    # Включает изменение пароля
    SECURITY_CHANGEABLE = True
    SECURITY_CHANGE_URL = "/change/"
    SECURITY_SEND_PASSWORD_CHANGE_EMAIL = False
    

    # ALLOWED_EXTENSIONS = ["jpg", "png", "jpeg"]
    # MAX_CONTENT_LENGTH = 2000 * 1024  # 1 mb


    SECURITY_PASSWORD_SALT = os.getenv('SECURITY_SALT')
    SECURITY_PASSWORD_HASH = os.getenv('SECURITY_HASH')


# class ProdConfig(Config):
#     DEBUG = False


# class DevConfig(Config):
#     DEVELOPMENT = True
#     DEBUG = True


# class TestingConfig(Config):
#     TESTING = True
