from flask_apispec.views import MethodResource
from flask_restful import Resource
from flask import request
from flasgger import swag_from
from app import logger
from .service import Authorization


# API фильмы на странице
class UserApiRegister(MethodResource, Resource, Authorization):
    @swag_from('./docs/register.yaml')
    def post(self):
        input_data = request.get_json()
        return self.create_user(input_data)


# Страница фильма
class UserApiLogin(MethodResource, Resource, Authorization):
    @swag_from('./docs/login.yaml')
    def post(self):
        input_data = request.get_json()
        return self.login_user(input_data)
