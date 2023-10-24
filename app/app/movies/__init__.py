from flask import Blueprint



movie = Blueprint('app_movies', __name__, template_folder='templates', static_folder='static')



from .routes import HomeView, MovieDetailView, MovieSearchView



movie.add_url_rule('/', view_func=HomeView.as_view('home'))

movie.add_url_rule('/film/<slug>', view_func=MovieDetailView.as_view('movie_detail'))
movie.add_url_rule('/search', view_func=MovieSearchView.as_view('movie_search'))