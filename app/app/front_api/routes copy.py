from flask_apispec import marshal_with, use_kwargs, doc
from flask import jsonify, request
from flask_apispec.views import MethodResource
from flask_restful import Resource
from werkzeug.security import check_password_hash
from app.front_api.schemas import MoviesSchema
from app.movies.models import Movie, Genre
from app import logger
from app.users.models import User
from .auth import error_response, token_required, generate_jwt_token
from .mixin import MixinMovie



class MoviesAPI(MixinMovie, MethodResource, Resource):
    # @logger.catch
    @doc(description='Flask API - Get all movie', tags=['Movies'])
    @marshal_with(MoviesSchema)  # marshalling
    def get(self):
        return self.responce_data(Movie, MoviesSchema)


    # @logger.catch
    @doc(description='Flask API.', tags=['Movies'])
    @use_kwargs(MoviesSchema, location=('json'))
    @marshal_with(MoviesSchema)  # marshalling
    @token_required
    def post(self, **kwargs):
        movie = self.create_movie(**kwargs)
        self.transaction_to_db(movie, "add")
        print('movie', movie)
        Genre.genre_add_to_movie(movie.id, kwargs["genres"])


class MoviesAPI2(MixinMovie, MethodResource, Resource):
    # @logger.catch
    @doc(description='Flask API.', tags=['Movies'])
    @marshal_with(MoviesSchema)  # marshalling
    def get(self, movie_id):
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie:
            return self.response_movie(movie, MoviesSchema)
        return error_response(301, "Not found movie")


    # @logger.catch
    @doc(description='update movie', tags=['Movies'])
    @use_kwargs(MoviesSchema, location=('json'))
    @marshal_with(MoviesSchema)
    @token_required
    def put(self, movie_id, **kwargs):
        movie = Movie.query.filter_by(id=movie_id).first()
        if movie:
            update_this_movie = self.update_movie(movie, **kwargs)
            self.transaction_to_db(update_this_movie, "update")
            Genre.genre_dell_to_movie(movie_id)
            Genre.genre_add_to_movie(movie.id, kwargs["genres"])
            return self.response_movie(movie)
        return error_response(301, "Not found movie")


    # @logger.catch
    @doc(description='delete movie', tags=['Movies'])
    @marshal_with(MoviesSchema)
    @token_required
    def delete(self, movie_id):
        movie = Movie.query.filter_by(id=int(movie_id)).first()
        if movie:
            Genre.genre_dell_to_movie(movie_id)
            self.transaction_to_db(movie, "delete")
            return self.response_movie(movie)
        return error_response(301, "Not found movie")
        
    

class Login(MethodResource, Resource):
    def post(self):
        params = request.json
        user = User.query.filter_by(email=params["email"]).first()
        if not user:
            return error_response(403, "Not found Emai")

        if check_password_hash(user.password, params["pwd"]):
            token = generate_jwt_token(data=user, lifetime=60) # <--- generates a JWT with valid within 1 hour by now
            return jsonify({'access_token': token})
        return error_response(403, "Not correct pasword")
