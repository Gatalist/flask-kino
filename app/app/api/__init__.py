from flask_restful import Api
from app import app
from .swagger_doc import Apispec_docs
from .routes import MoviesAPI, MoviesAPI2, Login



api = Api(app)
docs = Apispec_docs(app)


api.add_resource(MoviesAPI, '/movies')
api.add_resource(MoviesAPI2, '/movies/<movie_id>')
api.add_resource(Login, '/login-api')

docs.register(MoviesAPI)
docs.register(MoviesAPI2)
# docs.register(Login)

