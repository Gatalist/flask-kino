from flask import render_template, request
from flask.views import MethodView
from app.settings import Config
from .Mixin import MixinFilterMovie
from .models import Movie



class HomeView(MixinFilterMovie,  MethodView):
    def get(self):
        movie = self.filter_movie()
        movie = self.sort_movie(movie)
        page = request.args.get('page', 1, type=int)
        pages = movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages, **self.context)
    
    def post(self):
        movie = self.filter_movie(request.form)
        movie = self.sort_movie(movie, request.form)
        page = request.args.get('page', 1, type=int)
        pages = movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages, **self.context)



class MovieDetailView(MethodView):
    def get(self, slug):
        movie = Movie.query.filter(Movie.slug==slug).first()
        return render_template('detail_movie.html', movie=movie)



class MovieSearchView(MixinFilterMovie, MethodView):
    def get(self):
        movie = Movie.query
        q = request.args.get('q')
        if q:
            movie = self.search_movie(q)
        page = request.args.get('page', 1, type=int)
        pages = movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages, **self.context)

