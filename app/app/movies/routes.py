from flask import render_template, request, redirect
from flask.views import MethodView
from app.settings import Config
from .services import FilterMovie
from .models import Movie
from app.extensions import logger
from sqlalchemy.orm import selectinload


class HomeView(FilterMovie, MethodView):

    # @logger.catch
    def get(self):
        print("get movie")
        self.create_context()
        # query = Movie.query
        movies = self.filter_movie(request.form)
        print("movie filtered")
        # --- пагинация ---
        page = request.args.get('page', 1, type=int)
        pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        print("movie paginated")
        movies = pages.items

        movie_ids = [m.id for m in movies]
        print("movie_ids:", movie_ids)

        # --- догрузка связей через selectinload ---
        if movie_ids:
            (
                Movie.query
                .options(selectinload(Movie.genres))
                .options(selectinload(Movie.countries))
                .options(selectinload(Movie.director))
                .options(selectinload(Movie.year))
                .filter(Movie.id.in_(movie_ids))
                .all()
            )

        return render_template('index.html', pages=pages, **self.context)

    # @logger.catch
    def post(self):
        movies = self.filter_movie(request.form)
        # movies = self.sort_movie(movie)
        # movies.filter_by(publish=True).all()
        page = request.args.get('page', 1, type=int)
        pages = movies.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)
        return render_template('index.html', pages=pages, **self.context)


class MovieDetailView(MethodView):
    def get(self, slug):
        movie = Movie.query.filter(Movie.slug == slug).first()
        return render_template('detail_movie.html', movie=movie)


class MovieSearchView(FilterMovie, MethodView):

    def get(self):
        print("search movie")
        self.create_context()
        page = request.args.get('page', 1, type=int)
        q = request.args.get('q', '').strip()
        print("q", q)
        print("page", page)

        if not q:
            return redirect('/')

        # Основной запрос
        search = (
            Movie.query
            .filter(Movie.name_ru.ilike(f"%{q}%"))
        )

        # Пагинация

        pages = search.paginate(page=page, per_page=Config.PAGINATE_ITEM_IN_PAGE)

        # Дозагрузка связей (как в HomeView)
        movies = pages.items
        if movies:
            movie_ids = [m.id for m in movies]

            (
                Movie.query
                .options(selectinload(Movie.genres))
                .options(selectinload(Movie.year))
                .filter(Movie.id.in_(movie_ids))
                .all()
            )

        return render_template('index.html', pages=pages, q=q, **self.context)
