from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from flask_restful import Resource
from app.extensions import logger
from flask import request, jsonify
from flasgger import swag_from
from app.movies.schemas import (MoviesSchema, GenreSchema, CountrySchema, PersonSchema, ReleaseSchema)
from app.movies.models import (Movie, Genre, Country, Person, Release)
from app.api.service import Authorization, JsonifyObject, MovieCRUD


class UserApiRegister(Authorization, MethodResource, Resource):
    @swag_from('./docs/register.yaml')
    def post(self):
        input_data = request.get_json()
        return self.create_user(input_data)


class UserApiLogin(Authorization, MethodResource, Resource):
    @swag_from('./docs/login.yaml')
    def post(self):
        input_data = request.get_json()
        print(input_data)
        return self.login_user(input_data)


# API изменяем фильм
class MovieChange(MovieCRUD, MethodResource, Resource):
    # @logger.catch
    @marshal_with(MoviesSchema)  # marshalling
    @swag_from('./docs/movies_change.yaml')
    def get(self, movie_id):
        print("idd ->", movie_id)
        obj = Movie.query.filter_by(id=movie_id).first()
        if obj:
            serialize_obj = self.serialize_object(obj, MoviesSchema, many=False)
            return self.json_response_one(serialize_obj)
        return self.error_response(404, f"Not found movie id: {movie_id}")

    @marshal_with(MoviesSchema)
    @swag_from('./docs/movies_create.yaml')
    def put(self, movie_id):
        obj = Movie.query.filter_by(id=movie_id).first()
        if obj:
            serialize_obj = self.serialize_object(obj, MoviesSchema, many=False)
            return self.json_response_one(serialize_obj)
        return self.error_response(404, f"Not found movie id: {movie_id}")

    @marshal_with(MoviesSchema)
    @swag_from('./docs/movies_change.yaml')
    def delete(self, movie_id):
        delete = self.delete_object(Movie, id=movie_id)
        if delete:
            return jsonify({"status": "movie deleted"})
        return self.error_response(404, f"Not found movie id: {movie_id}")


# API создаем новый фильмы
class MovieCreate(MovieCRUD, MethodResource, Resource):
    # @logger.catch
    @marshal_with(MoviesSchema)
    @swag_from('./docs/movies_create.yaml')
    # @token_required
    def post(self):
        obj = self.get_or_create_movie(request)
        print(obj)
        if obj:
            serialize_obj = self.serialize_object(obj, MoviesSchema, many=False)
            return self.json_response_one(serialize_obj)
        return self.error_response(500, "Server error")


# API поиск фильмов
class MoviesSearch(JsonifyObject, MethodResource, Resource):
    # @logger.catch
    @marshal_with(MoviesSchema)
    @swag_from('./docs/movies_search.yaml')
    # @token_required
    def get(self):
        search = request.args.get('query')
        print('search - ', search)

        page = request.args.get('page')
        if not page:
            page = 1
        else:
            page = int(page)

        filter_obj = Movie.query.filter(Movie.name_ru.ilike(f"%{search}%")).order_by(Movie.id.desc())
        print('filter_obj - ', filter_obj)

        if filter_obj:
            obj_page = self.objects_in_page(page=page, obj=filter_obj)
            print('obj_page -', obj_page)
            filter_obj_count = filter_obj.count()
            serialize_obj = self.serialize_object(obj_page, MoviesSchema, many=True)
            return self.json_response_many(serialize_obj, filter_obj_count, page)
        return self.error_response(404, "Not found")


class MoviesList(JsonifyObject, MethodResource, Resource):
    # @logger.catch
    @marshal_with(MoviesSchema)
    @swag_from('./docs/movies_list.yaml')
    # @token_required
    def get(self):
        page = request.args.get('page')
        if not page:
            page = 1
        else:
            page = int(page)

        get_obj = Movie.query.order_by(Movie.id.desc())
        if get_obj:
            obj_page = self.objects_in_page(page=int(page), obj=get_obj)
            print('obj_page -', obj_page)
            obj_page_count = get_obj.count()
            serialize_obj = self.serialize_object(obj_page, MoviesSchema, many=True)
            return self.json_response_many(serialize_obj, obj_page_count, page)
        return self.error_response(404, f"Not found")


class ReleaseList(JsonifyObject, MethodResource, Resource):
    @logger.catch
    @marshal_with(ReleaseSchema)  # marshalling
    @swag_from('./docs/release_list.yaml')
    # @token_required
    def get(self):
        get_obj = Release.query
        if get_obj:
            obj_page_count = get_obj.count()
            serialize_obj = self.serialize_object(get_obj, ReleaseSchema, many=True)
            return self.json_response_many(serialize_obj, obj_page_count, page=None)
        return self.error_response(404, f"Not found")


class GenreList(JsonifyObject, MethodResource, Resource):
    @logger.catch
    @marshal_with(GenreSchema)  # marshalling
    @swag_from('./docs/genre_list.yaml')
    # @token_required
    def get(self):
        get_obj = Genre.query
        if get_obj:
            obj_page_count = get_obj.count()
            serialize_obj = self.serialize_object(get_obj, GenreSchema, many=True)
            return self.json_response_many(serialize_obj, obj_page_count, page=None)
        return self.error_response(404, f"Not found")


class PersonList(JsonifyObject, MethodResource, Resource):
    @logger.catch
    @marshal_with(PersonSchema)  # marshalling
    @swag_from('./docs/director_list.yaml')
    # @token_required
    def get(self):
        get_obj = Person.query
        if get_obj:
            obj_page_count = get_obj.count()
            serialize_obj = self.serialize_object(get_obj, PersonSchema, many=True)
            return self.json_response_many(serialize_obj, obj_page_count, page=None)
        return self.error_response(404, f"Not found")


class CountryList(JsonifyObject, MethodResource, Resource):
    @logger.catch
    @marshal_with(CountrySchema)  # marshalling
    @swag_from('./docs/country_list.yaml')
    # @token_required
    def get(self):
        get_obj = Country.query
        if get_obj:
            obj_page_count = get_obj.count()
            serialize_obj = self.serialize_object(get_obj, CountrySchema, many=True)
            return self.json_response_many(serialize_obj, obj_page_count, page=None)
        return self.error_response(404, f"Not found")
