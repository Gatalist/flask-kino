from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource, fields, marshal
from app import logger, db

from app.front_api.schemas import MoviesSchema, GenreSchema, CountrySchema
from app.front_api.schemas import DirectorSchema, ReliaseSchema
from app.movies.models import Movie, Genre, Country, Director, Reliase
from app.users.auth import error_response, token_required
from .mixin import Mixin



class MoviesMany(Mixin, MethodResource, Resource):
    description = """Пример использования:
                     /api/movie/page/1 - номер страницы с фильмами
                     'Access-Token': - ваш токен для доступа к API

                     
                    fetch('http://127.0.0.1:5000/api/movie/page/1', {
                        method: 'GET',
                        headers: {
                            'Access-Token': 'xxxxxxx-xxxxxx-xxxx-xxxx-xxxxxxxxx',
                            'Content-Type': 'application/json',
                        },
                    })"""
    schema = MoviesSchema

    # @logger.catch
    @doc(description=description, tags=['Movies'])
    @marshal_with(schema)
    @token_required
    def get(self, page):
        obj = Movie.query.order_by(Movie.id.desc())
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class MoviesOne(Mixin, MethodResource, Resource):
    description = """Пример использования:
                     /api/movie/1 - ID фильмама
                     'Access-Token': - ваш токен для доступа к API

                     
                    fetch('http://127.0.0.1:5000/api/movie/1', {
                        method: 'GET',
                        headers: {
                            'Access-Token': 'xxxxxxx-xxxxxx-xxxx-xxxx-xxxxxxxxx',
                            'Content-Type': 'application/json',
                        },
                    })"""
    schema = MoviesSchema

    @doc(description='Flask API.', tags=['Movies'])
    @marshal_with(schema)  # marshalling
    def get(self, movie_id):
        obj = Movie.query.filter_by(id=movie_id).first()
        if obj:
            return self.responce_object(obj, self.schema)
        return error_response(404, f"Not found movie id: {movie_id}")
    

class MoviesSearch(Mixin, MethodResource, Resource):
    description = """Пример использования:
                     /api/movie/search/ - название фильмама (полное или частичное)
                     'Access-Token': - ваш токен для доступа к API

                     
                    fetch('http://127.0.0.1:5000/api/movie/search/', {
                        method: 'GET',
                        headers: {
                            'Access-Token': 'xxxxxxx-xxxxxx-xxxx-xxxx-xxxxxxxxx',
                            'Content-Type': 'application/json',
                        },
                        data: {
                            'name': 'название фильма',
                        }
                    })"""
    schema = MoviesSchema

    # @logger.catch
    @doc(description=description, tags=['Search'])
    @marshal_with(schema)
    # @token_required
    def get(self, name, page):
        obj = Movie.query.filter(Movie.name_ru.ilike(f"%{name}%")).order_by(Movie.id.desc())
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class ReliaseMany(Mixin, MethodResource, Resource):
    description = 'Flask Restful API - Get all Reliase'
    schema = ReliaseSchema

    # @logger.catch
    @doc(description=description, tags=['Reliase'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self):
        obj = Reliase.query
        if obj:
            marshmallig = self.responce_many_objects(obj=obj, model_schema=self.schema)
            return self.json_result(page=None, marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class ReliaseOne(Mixin, MethodResource, Resource):
    description = 'Flask Restful API - Get all Reliase'
    schema = MoviesSchema

    # @logger.catch
    @doc(description=description, tags=['Reliase'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, reliase_id, page):
        obj = Movie.query.filter(Movie.year_id == int(reliase_id))
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class GenreMany(Mixin, MethodResource, Resource):
    description='Flask Restful API - Get all Genre'
    schema = GenreSchema

    # @logger.catch
    @doc(description=description, tags=['Genre'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self):    
        obj = Genre.query
        if obj:
            marshmallig = self.responce_many_objects(obj=obj, model_schema=self.schema)
            return self.json_result(page=None, marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class GenreOne(Mixin, MethodResource, Resource):
    description='Flask Restful API - Get all Genre'
    schema = MoviesSchema

    # @logger.catch
    @doc(description=description, tags=['Genre'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, genre_id, page):
        obj = Movie.query.filter(Movie.genres.any(Genre.id == genre_id))
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class DirectorMany(Mixin, MethodResource, Resource):
    description = 'Flask Restful API - Get all Director'
    schema = DirectorSchema

    # @logger.catch
    @doc(description=description, tags=['Director'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, page):
        obj = Director.query
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class DirectorOne(Mixin, MethodResource, Resource):
    description = 'Flask Restful API - Get all Director'
    schema = MoviesSchema

    # @logger.catch
    @doc(description=description, tags=['Director'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, director_id, page):
        obj = Movie.query.filter(Movie.director.any(Director.id == director_id))
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class CountryMany(Mixin, MethodResource, Resource):
    description = 'Flask Restful API - Get all Country'
    schema = CountrySchema

    # @logger.catch
    @doc(description=description, tags=['Country'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self):
        obj = Country.query
        if obj:
            marshmallig = self.responce_many_objects(obj=obj, model_schema=self.schema)
            return self.json_result(page=None, marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class CountryOne(Mixin, MethodResource, Resource):
    description = 'Flask Restful API - Get all Country'
    schema = MoviesSchema

    # @logger.catch
    @doc(description=description, tags=['Country'])
    @marshal_with(schema)  # marshalling
    # @token_required
    def get(self, country_id, page):
        obj = Movie.query.filter(Movie.countries.any(Country.id == country_id))
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")
