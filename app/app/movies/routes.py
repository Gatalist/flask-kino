from flask import render_template, request
from flask.views import MethodView
from app.settings import Config
# from .Mixin import MixinFilterMovie
from .models import Movie


class HomeView(MethodView):
    def get(self):
        # movie = self.filter_movie()
        movie = Movie.query
        # movie = self.sort_movie(movie)
        page = request.args.get('page', 1, type=int)
        pages = movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        # return render_template('index-2.html', pages=pages, **self.context)
        return render_template('index-2.html', pages=pages)
        # return {'status': 200}
    
    def post(self):
        movie = Movie.query
        # movie = self.filter_movie(request.form)
        # movie = self.sort_movie(movie, request.form)
        page = request.args.get('page', 1, type=int)
        pages = movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages)
        # return render_template('index-2.html', pages=pages, **self.context)
        # return {'status': 200}


class MovieDetailView(MethodView):
    def get(self, slug):
        movie = Movie.query.filter(Movie.slug==slug).first()
        return render_template('detail_movie.html', movie=movie)


class MovieSearchView(MethodView):
    def get(self):
        movie = Movie.query
        q = request.args.get('q')
        if q:
            search = movie.filter(Movie.name_ru.ilike(f"%{q}%"))
            if search:
                search_movie = search
            else:
                search_movie = []
            # movie = self.search_movie(q)
        page = request.args.get('page', 1, type=int)
        pages = search_movie.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index-2.html', pages=pages)
        # return render_template('index-2.html', pages=pages, **self.context)
        # return {'status': 200}
