from app import app
from app.settings import Config

# blueprints
from app.movies import movie
from app.users import users
from app.admin import admin_panel
# from app.admin.routes import app_admin

# api
from app.front_api import front_api, front_docs_api
# from app.api import api, docs



# register applications urls
app.register_blueprint(movie, url_prefix='/')
# app.register_blueprint(users, url_prefix='/user')


if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    