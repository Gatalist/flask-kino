from flask import jsonify
from app import db
from app.movies.models import Movies, Reliase, Ratings, Directors


class MixinMovie():
    def transaction_to_db(self, obj: object, method: str) -> None:
        try:
            if method == "add":
                db.session.add(obj)
            if method == "delete":
                db.session.delete(obj)
            if method =="update":
                pass
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise

    def responce_data(self, model: object, model_schema: object) -> jsonify:
        obj = model.query.all()
        schema = model_schema(many=True)
        print(schema)
        return jsonify(schema.dump(obj))

    def create_movie(self, **kwargs):
        reliase = Reliase.get_or_create(search=int(kwargs['reliase']))
        rating = Ratings.get_or_create(search=float(kwargs['rating']))
        director = Directors.get_or_create(search=kwargs['director'])
        poster_image = kwargs['poster']

        if not poster_image:
            poster_image = "https://motivatevalmorgan.com/wp-content/uploads/2016/06/default-movie-204x300.jpg"
       
        movie = Movies(
            title = kwargs['title'],
            description = kwargs['description'],
            poster = poster_image,
            reliase_id = reliase.id,
            director_id = director.id,
            rating_id = rating.id,
            user_id = kwargs["user_id"],
        )
        return movie
    
    def update_movie(self, movie, **kwargs):
        if kwargs['title']:
            movie.title = kwargs['title']
        if kwargs['description']:
            movie.description = kwargs['description']
        if kwargs['poster']:
            movie.poster = kwargs['poster']
        if kwargs['reliase']:
            reliase = Reliase.get_or_create(search=int(int(kwargs['reliase'])))
            movie.reliase_id = reliase.id
        if kwargs['rating']:
            rating = Ratings.get_or_create(search=float(float(kwargs['rating'])))
            movie.rating_id = rating.id
        if kwargs['director']:
            director = Directors.get_or_create(search=kwargs['director'])
            movie.director_id = director.id
        return movie
    

    def response_movie(self, obj: object):
        return jsonify({
            "id": str(obj.id),
            "title": str(obj.title),
            "poster": str(obj.poster),
            "description": obj.description,
            "reliase": str(obj.reliase),
            "director": str(obj.director),
            "rating": str(obj.rating),
            "genres": f"{obj.genres}",
        })
    
