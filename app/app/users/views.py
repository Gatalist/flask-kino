from flask.views import View
from .models import User
from .service import create_user, login_user
from flask import jsonify, request



class UserApiRegisterView(View):
    # init_every_request = False
    methods = ["POST"]
    # print(request)
    # def __init__(self, model, template):
    #     self.model = User
        # self.template = template

    def dispatch_request(self):
        input_data = request.get_json()
        print(input_data)
        return jsonify(create_user(input_data))


class UserApiLoginView(View):
    methods = ["POST"]

    def dispatch_request(self):
        input_data = request.get_json()
        print(input_data)
        return jsonify(login_user(input_data))













# from flask import Response
# from flask_restful import Resource
# from flask import request, make_response

# # from flask_apispec.views import MethodResource
# from .auth import token_required
# # from flask_apispec import marshal_with, use_kwargs, doc



# class SignUpApi(MethodResource, Resource):
#     # description = 'Flask Restful API - register user'

#     # @logger.catch
#     # @doc(description=description, tags=['User'])
#     def post(self) -> Response:
#         input_data = request.get_json()
#         return create_user(input_data)


# class LoginApi(MethodResource, Resource):
#     @token_required
#     def post(self) -> Response:
#         input_data = request.get_json()
#         return login_user(input_data)