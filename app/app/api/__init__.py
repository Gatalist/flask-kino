from flask import Blueprint
from flask_restful import Api

from .routes import (UserApiRegister, UserApiLogin, MoviesList, GenreList, CountryList, PersonList, ReleaseList,
                     MoviesSearch, MovieChange, MovieCreate)


api_blueprint = Blueprint('app_api', __name__, template_folder='templates', static_folder='static')
api = Api(api_blueprint)

# регистрируем url нашего api
api.add_resource(UserApiRegister, 'register/')
api.add_resource(UserApiLogin, 'login/')

api.add_resource(MovieCreate, 'movie/create/')
api.add_resource(MovieChange, 'movie/<movie_id>/')
api.add_resource(MoviesSearch, 'movie/search/')
api.add_resource(MoviesList, 'movie/')
#
api.add_resource(ReleaseList, 'release/')
api.add_resource(GenreList, 'genre/')
api.add_resource(PersonList, 'person/')
api.add_resource(CountryList, 'country/')
