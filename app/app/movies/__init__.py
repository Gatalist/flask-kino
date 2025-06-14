from flask import Blueprint
from app import db, admin
from app.movies.routes import (HomeView, MovieDetailView, MovieSearchView)

from app.movies.models import (Movie, RatingKinopoisk, RatingImdb, RatingCritic, Release, FilmLength,
                               Genre, AgeLimit, TypeVideo, Person, Screenshot, Similar, Country,
                               Tag, Segment)

from .admins import (MovieView, RatingKinopoiskView, RatingImdbView, RatingFilmCriticsView, ReleaseView,
                     FilmLengthView, GenreView, AgeLimitView, TypeVideoView, TagActorView,
                     PersonView, ScreenshotView, SimilarView, CountryView, SegmentView)


movie_blueprint = Blueprint('app_movies', __name__, template_folder='templates', static_folder='static')


# register router blueprint
movie_blueprint.add_url_rule('/', view_func=HomeView.as_view('home'))
movie_blueprint.add_url_rule('film/<slug>/', view_func=MovieDetailView.as_view('movie_detail'))
movie_blueprint.add_url_rule('search/', view_func=MovieSearchView.as_view('movie_search'))


# register admin model
admin.add_view(MovieView(Movie, db.session, name='Фильмы', category="Каталог"))
admin.add_view(RatingKinopoiskView(RatingKinopoisk, db.session, name='Кинопоиск', category="Рейтинг"))
admin.add_view(RatingImdbView(RatingImdb, db.session, name='Imdb', category="Рейтинг"))
admin.add_view(RatingFilmCriticsView(RatingCritic, db.session, name='Критики', category="Рейтинг"))
admin.add_view(ReleaseView(Release, db.session, name='Год выпуска', category="Каталог"))
admin.add_view(FilmLengthView(FilmLength, db.session, name='Продолжительность', category="Каталог"))
admin.add_view(GenreView(Genre, db.session, name='Жанр', category="Каталог"))
admin.add_view(CountryView(Country, db.session, name='Страна', category="Каталог"))
admin.add_view(AgeLimitView(AgeLimit, db.session, name='Возрастное ограничение', category="Каталог"))
admin.add_view(TypeVideoView(TypeVideo, db.session, name='Категория', category="Каталог"))
admin.add_view(PersonView(Person, db.session, name='Люди', category="Каталог"))
admin.add_view(ScreenshotView(Screenshot, db.session, name='Кадры с фильма', category="Каталог"))
admin.add_view(SimilarView(Similar, db.session, name='Похожие фильмы', category="Каталог"))
admin.add_view(TagActorView(Tag, db.session, name='Теги-актеров'))
admin.add_view(SegmentView(Segment, db.session, name='Сегменты'))
