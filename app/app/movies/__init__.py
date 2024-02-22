from flask import Blueprint
from app import db, admin, api  # , api_docs

from app.movies.routes import (HomeView, MovieDetailView, MovieSearchView)

from app.movies.models import (Movie, RatingKinopoisk, RatingImdb, RatingFilmCritics, Reliase, FilmLength,
                               Genre, AgeLimit, TypeVideo, Director, Creator, Actor, Screenshot, Similars, Country,
                               Trailer, TagActor, Segment)

from .admin_logica import (MovieView, RatingKinopoiskView, RatingImdbView, RatingFilmCriticsView, ReleaseView,
                           FilmLengthView, GenreView, AgeLimitView, TypeVideoView, DirectorView, TagActorView,
                           CreatorView, ActorView, ScreenshotView, SimilarsView, CountryView, TrailerView, SegmentView)

from .routes_api import (MoviesList, GenreList, CountryList, DirectorList, ReleaseList, MoviesSearch,
                         MovieChange, MovieCreate)


movie_blueprint = Blueprint('app_movies', __name__, template_folder='templates', static_folder='static')


# регистрируем роуты для нашего blueprint
movie_blueprint.add_url_rule('/', view_func=HomeView.as_view('home'))
movie_blueprint.add_url_rule('/film/<slug>', view_func=MovieDetailView.as_view('movie_detail'))
movie_blueprint.add_url_rule('/search', view_func=MovieSearchView.as_view('movie_search'))


# регистрируем модели в нашей админке
admin.add_view(MovieView(Movie, db.session))
admin.add_view(RatingKinopoiskView(RatingKinopoisk, db.session))
admin.add_view(RatingImdbView(RatingImdb, db.session))
admin.add_view(RatingFilmCriticsView(RatingFilmCritics, db.session))
admin.add_view(ReleaseView(Reliase, db.session))
admin.add_view(FilmLengthView(FilmLength, db.session))
admin.add_view(GenreView(Genre, db.session))
admin.add_view(CountryView(Country, db.session))
admin.add_view(AgeLimitView(AgeLimit, db.session))
admin.add_view(TypeVideoView(TypeVideo, db.session))
admin.add_view(DirectorView(Director, db.session))
admin.add_view(CreatorView(Creator, db.session))
admin.add_view(ActorView(Actor, db.session))
admin.add_view(ScreenshotView(Screenshot, db.session))
admin.add_view(SimilarsView(Similars, db.session))
admin.add_view(TrailerView(Trailer, db.session))
admin.add_view(TagActorView(TagActor, db.session))
admin.add_view(SegmentView(Segment, db.session))


# регистрируем url нашего api
api.add_resource(MovieCreate, '/api/movie/create/')
api.add_resource(MovieChange, '/api/movie/<movie_id>/')
api.add_resource(MoviesSearch, '/api/movie/search/')
api.add_resource(MoviesList, '/api/movie/')

api.add_resource(ReleaseList, '/api/release/')
api.add_resource(GenreList, '/api/genre/')
api.add_resource(DirectorList, '/api/director/')
api.add_resource(CountryList, '/api/country/')
