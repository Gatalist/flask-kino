from flask import render_template, request, redirect
from flask.views import MethodView
from app.settings import Config
from .services import MixinMovie
from .models import Movie
from app import logger


class HomeView(MixinMovie, MethodView):
    # @logger.catch
    def get(self):
        self.create_context()

        movie = self.filter_movie()
        movies = self.sort_movie(movie)
        print(movie.all())
        page = request.args.get('page', 1, type=int)
        pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages, **self.context)

    # @logger.catch
    def post(self):
        movie = self.filter_movie(request.form)
        movies = self.sort_movie(movie, request.form)
        page = request.args.get('page', 1, type=int)
        pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages, **self.context)


class MovieDetailView(MethodView):
    def get(self, slug):
        movie = Movie.query.filter(Movie.slug == slug).first()
        return render_template('detail_movie.html', movie=movie)


class MovieSearchView(MixinMovie, MethodView):
    @logger.catch
    def get(self):
        self.create_context()
        
        movie = Movie.query
        q = request.args.get('q')
        if q:
            search = movie.filter(Movie.name_ru.ilike(f"%{q}%"))
            if search:
                search_movie = search
            else:
                search_movie = []
        else:
            return redirect('/')

        page = request.args.get('page', 1, type=int)
        pages = search_movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages, **self.context)
