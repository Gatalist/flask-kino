from flask_apispec import marshal_with, doc
from flask_apispec.views import MethodResource
from flask_restful import Resource
from flask import request
from app import logger
from app.users.auth import error_response
from .schemas import LoginUserSchema, CreateUserSchema
from .service import create_user, login_user, ApiDocumentation



# API фильмы на странице
class UserApiRegister(MethodResource, Resource):
    schema = CreateUserSchema
    description = ApiDocumentation().documentation(
        method='POST',
        url='/api/user/register/', 
        desc='заполняем данные для регистрации', 
        url_full='http://127.0.0.1:5000/api/user/register/',
        data="'data': {'username':'Alibaba', 'email':'user@email', 'password':'your_pasword'}")

    # @logger.catch
    @doc(description=description, tags=['User'])
    @marshal_with(schema)
    def post(self):
        input_data = request.get_json()
        obj = create_user(input_data)
        if obj:
            return self.responce_object(obj, self.schema)
        return error_response(404, f"Not found")


# Страница фильма
class UserApiLogin(MethodResource, Resource):
    schema = LoginUserSchema
    description = ApiDocumentation().documentation(
        method='POST',
        url='/api/user/login/', 
        desc='заполняем данные для получения доступа', 
        url_full='http://127.0.0.1:5000/api/user/login/',
        data="'data': {'email':'user@email', 'password':'your_pasword'}")

    # @logger.catch
    @doc(description=description, tags=['User'])
    @marshal_with(schema)  # marshalling
    def post(self):
        input_data = request.get_json()
        obj = login_user(input_data)
        if obj:
            return self.responce_object(obj, self.schema)
        return error_response(404, f"Not found")
    
