from flask import url_for
from flask_admin import Admin, helpers
# from flask_security import SQLAlchemyUserDatastore, Security

from app import app, db
from app.movies.models import Movie, RatingKinopoisk, RatingImdb, RatingFilmCritics, Reliase, FilmLength
from app.movies.models import Genre, CountryReliase, AgeLimit, TypeVideo, Director, Creator, Actor, Screenshot
from app.movies.models import Similars
# from app.users.models import Users, Role
# from .routes import MyAdminIndexView, UsersView
from .routes import MovieView, RatingKinopoiskView, RatingImdbView, RatingFilmCriticsView, ReliaseView
from .routes import FilmLengthView, GenreView, CountryReliaseView, AgeLimitView, TypeVideoView, DirectorView
from .routes import CreatorView, ActorView, ScreenshotView, SimilarsView
# Setup Flask-Security
# user_datastore = SQLAlchemyUserDatastore(db, Users, Role)
# security = Security(app, user_datastore)


# Create admin
# admin_panel = Admin(app, index_view=MyAdminIndexView(), base_template='admin/master-extended.html')
admin_panel = Admin(app)

admin_panel.add_view(MovieView(Movie, db.session))
admin_panel.add_view(RatingKinopoiskView(RatingKinopoisk, db.session))
admin_panel.add_view(RatingImdbView(RatingImdb, db.session))
admin_panel.add_view(RatingFilmCriticsView(RatingFilmCritics, db.session))
admin_panel.add_view(ReliaseView(Reliase, db.session))
admin_panel.add_view(FilmLengthView(FilmLength, db.session))
admin_panel.add_view(GenreView(Genre, db.session))
admin_panel.add_view(CountryReliaseView(CountryReliase, db.session))
admin_panel.add_view(AgeLimitView(AgeLimit, db.session))
admin_panel.add_view(TypeVideoView(TypeVideo, db.session))
admin_panel.add_view(DirectorView(Director, db.session))
admin_panel.add_view(CreatorView(Creator, db.session))
admin_panel.add_view(ActorView(Actor, db.session))
admin_panel.add_view(ScreenshotView(Screenshot, db.session))
admin_panel.add_view(SimilarsView(Similars, db.session))

# admin_panel.add_view(MovieScreenshotView(screenshot_movie, db.session))
# admin_panel.add_view(UsersView(Users, db.session))


# define a context processor for merging flask-admin's template context into the
# flask-security views.
# @security.context_processor
# def security_context_processor():
#     return dict(
#         admin_base_template=admin_panel.base_template,
#         admin_view=admin_panel.index_view,
#         h=helpers,
#         get_url=url_for
#     )
