from flask import Blueprint
from app import db, admin, api, api_docs

from app.movies.routes import (
    HomeView, MovieDetailView, MovieSearchView
)

from app.movies.models import (
    Movie, RatingKinopoisk, RatingImdb, RatingFilmCritics, Reliase, FilmLength,
    Genre, AgeLimit, TypeVideo, Director, Creator, Actor, Screenshot,
    Similars, Country, Trailer, TagActor, Segment
)

from .admin_logica import (
    MovieView, RatingKinopoiskView, RatingImdbView, RatingFilmCriticsView, ReliaseView,
    FilmLengthView, GenreView, AgeLimitView, TypeVideoView, DirectorView, TagActorView,
    CreatorView, ActorView, ScreenshotView, SimilarsView, CountryView, TrailerView,
    SegmentView
)

from .routes_api import (
    MoviesOnPage, GenreOnPage, CountryOnPage, DirectorOnPage, ReliaseOnPage, MoviesSearch,
    MoviesDetail, GenreDetail, CountryDetail, DirectorDetail, ReliaseDetail
)



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
admin.add_view(ReliaseView(Reliase, db.session))
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



# пегистрируем url нашего api
api.add_resource(MoviesOnPage, '/api/movie/page/<page>')
api.add_resource(MoviesDetail, '/api/movie/id/<id>')
api.add_resource(MoviesSearch, '/api/movie/search/<name>/<page>')

api.add_resource(ReliaseOnPage, '/api/reliase')
api.add_resource(ReliaseDetail, '/api/reliase/<id>')

api.add_resource(GenreOnPage, '/api/genre')
api.add_resource(GenreDetail, '/api/genre/<id>/<page>')

api.add_resource(DirectorOnPage, '/api/director/<page>')
api.add_resource(DirectorDetail, '/api/director/<id>/<page>')

api.add_resource(CountryOnPage, '/api/country')
api.add_resource(CountryDetail, '/api/country/<id>/<page>')





# Добавляем документацию
api_docs.register(MoviesOnPage)
api_docs.register(MoviesDetail)
api_docs.register(MoviesSearch)

api_docs.register(ReliaseOnPage)
api_docs.register(ReliaseDetail)

api_docs.register(GenreOnPage)
api_docs.register(GenreDetail)

api_docs.register(DirectorOnPage)
api_docs.register(DirectorDetail)

api_docs.register(CountryOnPage)
api_docs.register(CountryDetail)
