from flask_apispec import marshal_with, use_kwargs, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from app import logger
from flask import request

from app.movies.schemas import (
    MoviesSchema, GenreSchema, CountrySchema,
    DirectorSchema, ReliaseSchema
)

from app.movies.models import (
    Movie, Genre, Country, Director, Reliase
)

from app.users.auth import error_response, token_required
from .services_api import Mixin, ApiDocumentation



# API фильмы на странице
class MoviesOnPage(Mixin, MethodResource, Resource):
    schema = MoviesSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/movie/page/{page}/', 
        desc='номер страницы с фильмами', 
        url_full='http://127.0.0.1:5000/api/movie/page/1')

    @logger.catch
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


# Страница фильма
class MoviesDetail(Mixin, MethodResource, Resource):
    schema = MoviesSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/movie/id/{id}/', 
        desc='ID фильмама для получения данных', 
        url_full='http://127.0.0.1:5000/api/movie/id/1')

    @logger.catch
    @doc(description=description, tags=['Movies'])
    @marshal_with(schema)  # marshalling
    def get(self, id):
        obj = Movie.query.filter_by(id=id).first()
        if obj:
            return self.responce_object(obj, self.schema)
        return error_response(404, f"Not found movie id: {id}")
    

class MoviesSearch(Mixin, MethodResource, Resource):
    schema = MoviesSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/movie/search/{page}/', 
        desc='название фильмама (полное или частичное) и номер страницы', 
        url_full='http://127.0.0.1:5000/api/search/1',
        data="'data': {'search': 'матр'}")

    @logger.catch
    @doc(description=description, tags=['Movies'])
    @marshal_with(schema)
    @token_required
    def get(self, page):
        search = request.args.get('search')
        obj = Movie.query.filter(Movie.name_ru.ilike(f"%{search}%")).order_by(Movie.id.desc())
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class ReliaseOnPage(Mixin, MethodResource, Resource):
    schema = ReliaseSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/reliase/', 
        desc='все года выхода фильмов', 
        url_full='http://127.0.0.1:5000/api/reliase/')

    @logger.catch
    @doc(description=description, tags=['Reliase'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self):
        obj = Reliase.query
        if obj:
            marshmallig = self.responce_many_objects(obj=obj, model_schema=self.schema)
            return self.json_result(page=None, marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class ReliaseDetail(Mixin, MethodResource, Resource):
    schema = MoviesSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/reliase/{id}/', 
        desc='ID года выхода для получения фильмов', 
        url_full='http://127.0.0.1:5000/api/reliase/1/')
    
    @logger.catch
    @doc(description=description, tags=['Reliase'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self, id):
        obj = Movie.query.filter_by(id=id).first()
        if obj:
            return self.responce_object(obj, self.schema)
        return error_response(404, f"Not found")


class GenreOnPage(Mixin, MethodResource, Resource):
    schema = GenreSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/genre/', 
        desc='все жанры фильмов', 
        url_full='http://127.0.0.1:5000/api/genre/')
    
    @logger.catch
    @doc(description=description, tags=['Genre'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self):    
        obj = Genre.query
        if obj:
            marshmallig = self.responce_many_objects(obj=obj, model_schema=self.schema)
            return self.json_result(page=None, marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class GenreDetail(Mixin, MethodResource, Resource):
    schema = MoviesSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/genre/{id}/{page}', 
        desc='ID жанра и номер страницы для получения фильмов этого жанра', 
        url_full='http://127.0.0.1:5000/api/genre/1/1')
    
    @logger.catch
    @doc(description=description, tags=['Genre'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self, id, page):
        obj = Movie.query.filter(Movie.genres.any(Genre.id == id))
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class DirectorOnPage(Mixin, MethodResource, Resource):
    schema = DirectorSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/director/{page}/', 
        desc='все режисеры фильмов', 
        url_full='http://127.0.0.1:5000/api/director/1/')
    
    @logger.catch
    @doc(description=description, tags=['Director'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self, page):
        obj = Director.query
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class DirectorDetail(Mixin, MethodResource, Resource):
    schema = MoviesSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/director/{id}/{page}/', 
        desc='ID режисера и номер страницы для получения фильмов с этим режисером', 
        url_full='http://127.0.0.1:5000/api/genre/1/1/')
    
    @logger.catch
    @doc(description=description, tags=['Director'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self, id, page):
        obj = Movie.query.filter(Movie.director.any(Director.id == id))
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class CountryOnPage(Mixin, MethodResource, Resource):
    schema = CountrySchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/country/', 
        desc='все страны выпуска фильмов', 
        url_full='http://127.0.0.1:5000/api/country/')

    @logger.catch
    @doc(description=description, tags=['Country'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self):
        obj = Country.query
        if obj:
            marshmallig = self.responce_many_objects(obj=obj, model_schema=self.schema)
            return self.json_result(page=None, marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")


class CountryDetail(Mixin, MethodResource, Resource):
    schema = MoviesSchema
    description = ApiDocumentation().documentation(
        method='GET',
        url='/api/country/{id}/{page}/', 
        desc='ID страны и номер страницы для получения фильмов с этой страны', 
        url_full='http://127.0.0.1:5000/api/country/1/1/')

    @logger.catch
    @doc(description=description, tags=['Country'])
    @marshal_with(schema)  # marshalling
    @token_required
    def get(self, id, page):
        obj = Movie.query.filter(Movie.countries.any(Country.id == id))
        if obj:
            obj_page = self.objects_in_page(page=int(page), obj=obj)
            marshmallig = self.responce_many_objects(obj=obj_page, model_schema=self.schema)
            return self.json_result(page=int(page), marshmallig=marshmallig, obj=obj)
        return error_response(404, f"Not found")
