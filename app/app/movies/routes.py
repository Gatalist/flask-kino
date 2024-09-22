from flask import render_template, request, redirect, make_response, url_for
from flask.views import MethodView
from app.settings import Config
from .services import FilterMovie, SortingMovie
from .models import Movie
from app.extensions import logger


class HomeView(FilterMovie, SortingMovie, MethodView):
    # @logger.catch
    def get(self):
        self.create_context()

        movie = self.filter_movie()
        movies = self.sort_movie(movie)
        print(movie.all())

        page = request.args.get('page', 1, type=int)
        print('page', page, type(page))
        pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index.html', pages=pages, **self.context)

    # @logger.catch
    def post(self):
        movie = self.filter_movie(request.form)
        movies = self.sort_movie(movie, request.form)
        page = request.args.get('page', 1, type=int)
        pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index.html', pages=pages, **self.context)
        # return redirect(url_for('index.html', page=page, **self.context))


class MovieDetailView(MethodView):
    def get(self, slug):
        movie = Movie.query.filter(Movie.slug == slug).first()
        return render_template('detail_movie.html', movie=movie)


class MovieSearchView(FilterMovie, MethodView):
    @logger.catch
    def get(self):
        self.create_context()
        
        movie = Movie.query
        q = request.args.get('q')
        if q:
            search = movie.filter(Movie.name_ru.ilike(f"%{q}%"))
            if not search:
                search = []
        else:
            return redirect('/')

        page = request.args.get('page', 1, type=int)
        pages = search.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index.html', pages=pages, **self.context)
