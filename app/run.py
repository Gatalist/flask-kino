from app import app
from app.settings import Config
from app.movies import movie
# from app.users import users
# from app.admin.routes import app_admin
from app.admin import admin_panel
# from app.api import api, docs



# register applications
app.register_blueprint(movie, url_prefix='/')
# app.register_blueprint(users, url_prefix='/user')


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    