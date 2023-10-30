from flask import jsonify
from app import db
# from app.movies.models import Movie
from flask_apispec.views import MethodResource
from flask_restful import Resource
from flask_apispec import marshal_with, use_kwargs, doc



class MixinJsonify:
    def responce_many_objects(self, obj: object, model_schema: object) -> jsonify:
        schema = model_schema(many=True)
        print(schema)
        return jsonify(schema.dump(obj))

    def responce_object(self, obj: object, model_schema: object) -> jsonify:
        schema = model_schema(many=False)
        print(schema)
        return jsonify(schema.dump(obj))
