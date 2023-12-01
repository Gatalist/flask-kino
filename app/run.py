from app import app
from app.settings import Config

# blueprints
from app.movies import movie_blueprint
from app.users import user_blueprint


# Регистрируем Blueprint'ы в приложении
app.register_blueprint(movie_blueprint, url_prefix='/')
app.register_blueprint(user_blueprint, url_prefix='/user')



# api
from app.front_api import front_api, front_api_docs
# from app.front_api import app_api, api, swagger



if __name__ == '__main__':
    app.run(debug=Config.DEBUG, host=Config.HOST, port=Config.PORT)
    