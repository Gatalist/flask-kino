from flask import jsonify, request
from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource, fields, marshal
# from werkzeug.security import check_password_hash
from sqlalchemy import func
from app import logger, db

from app.front_api.schemas import MoviesSchema, GenreSchema, CountrySchema, DirectorSchema, ReliaseSchema, PaginationSchema
from app.movies.models import Movie, Genre, Country, Director, Reliase, director_movie
from app.settings import Config
from app.users.models import User
from .auth import error_response, token_required, generate_jwt_token
from .mixin import MixinJsonify






class MoviesMany(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Movie'
    schema = MoviesSchema

    # @logger.catch
    @doc(description=description, tags=['Movies'])
    @marshal_with(schema)
    # @token_required
    def get(self, page):
        films = Movie.query.all()
        # Получите параметры пагинации из запроса
       
        per_page = Config.PAGINATE_ITEM_IN_PAGE
        page = int(page)
        # Вычислите начальный и конечный индексы для выборки фильмов
        start = (page - 1) * per_page
        end = start + per_page

        # Выберите фильмы для текущей страницы
        paginated_films = films[start:end]

        # Используйте схему Marshmallow для маршалинга данных
        serialized_films = self.responce_many_objects(paginated_films, self.schema)
        return serialized_films


class MoviesOne(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Movie'
    schema = MoviesSchema

    @doc(description='Flask API.', tags=['Movies'])
    @marshal_with(schema)  # marshalling
    def get(self, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie:
            return self.responce_object(movie, self.schema)
        return error_response(301, "Not found movie")


class GenreMany(MixinJsonify, MethodResource, Resource):
    description='Flask Restful API - Get all Genre'
    schema = GenreSchema

    # @logger.catch
    @doc(description=description, tags=['Genre'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self):
        genre = Genre.query.all()
        return self.responce_many_objects(genre, self.schema)


class GenreOne(MixinJsonify, MethodResource, Resource):
    description='Flask Restful API - Get all Genre'
    schema = GenreSchema

    # @logger.catch
    @doc(description=description, tags=['Genre'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, genre_id):
        genre = Genre.query.filter_by(id=genre_id).first()
        if genre:
            return self.responce_object(genre, self.schema)
        return error_response(301, "Not found genre")


class CountryMany(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Country'
    schema = CountrySchema

    # @logger.catch
    @doc(description=description, tags=['Country'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self):
        country = Country.query.all()
        return self.responce_many_objects(country, self.schema)
    

class CountryOne(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Country'
    schema = CountrySchema

    # @logger.catch
    @doc(description=description, tags=['Country'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, country_id):
        country = Country.query.filter_by(id=country_id).first()
        if country:
            return self.responce_object(country, self.schema)
        return error_response(301, "Not found country")


class DirectorMany(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Director'
    schema = DirectorSchema

    # @logger.catch
    @doc(description=description, tags=['Director'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self):
        # director = Movie.query.join(director_movie).join(Director).group_by(Director.id)
        # director = Movie.query.join(director_movie).join(Director).options(joinedload(Movie.director_id)).group_by(Director.id).limit(20).all()
        director = db.session.query(
            Director.id, func.count(Movie.id).label('movie_count')).join(Movie.director_id).group_by(
            Director.id).order_by(func.count(Movie.id).desc()).limit(20).all()
        print(director)
        return self.responce_many_objects(director, self.schema)


class DirectorOne(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Director'
    schema = DirectorSchema

    # @logger.catch
    @doc(description=description, tags=['Director'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, director_id):
        director = Director.query.filter_by(id=director_id).first()
        if director:
            return self.responce_object(director, self.schema)
        return error_response(301, "Not found director")


class ReliaseMany(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Reliase'
    schema = ReliaseSchema

    # @logger.catch
    @doc(description=description, tags=['Reliase'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self):
        reliase = Reliase.query.all()
        return self.responce_many_objects(reliase, self.schema)


class ReliaseOne(MixinJsonify, MethodResource, Resource):
    description = 'Flask Restful API - Get all Reliase'
    schema = ReliaseSchema

    # @logger.catch
    @doc(description=description, tags=['Reliase'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, reliase_id):
        reliase = Reliase.query.filter_by(id=reliase_id).first()
        if reliase:
            return self.responce_object(reliase, self.schema)
        return error_response(301, "Not found reliase")
