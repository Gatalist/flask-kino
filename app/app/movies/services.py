from flask import session
from sqlalchemy.orm import joinedload
from .models import (Movie, RatingKinopoisk, Release, Genre, Director, genre_movie, director_movie)


class ContextData:
    data_sorted = [
        {'value': "standard", 'text': 'стандартная'},
        {'value': "rating_asc", 'text': 'От мин до мах рейтинга'},
        {'value': "rating_desc", 'text': "От мах до мин рейтинга"},
        {'value': "release_date_asc", 'text': 'От старых до новых'},
        {'value': "release_date_desc", 'text': 'От новых до старых'}]

    context = {}

    def create_context(self):
        self.context["movies_sorted"] = self.data_sorted
        self.context["all_release"] = self.get_years()
        self.context["all_genres"] = self.get_genres()
        self.context["all_directors"] = self.top_directors()

    @staticmethod
    def top_directors():
        return Director.query.join(director_movie).group_by(Director.id).order_by(Director.id.desc())[:15]

    @staticmethod
    def get_genres():
        return Genre.query

    @staticmethod
    def get_years():
        return Release.query.order_by(Release.year.desc())

    @staticmethod
    def session_data(name, data):
        session.permanent = True
        if name not in session:
            session[name] = data
        else:
            session[name] = data
        session.modified = True
        return session

    def update_context_session(self, release, genre, director):
        # Добавляем активные фильтры в context
        self.context["is_active_years"] = release
        self.context["is_active_genres"] = genre
        self.context["is_active_directors"] = director
        # добавляем фильтра в сессию
        self.session_data('is_active_years', release)
        self.session_data('is_active_genres', genre)
        self.session_data('is_active_directors', director)


class FilterMovie(ContextData):
    def filter_movie(self, form=None):
        if form and form.get('form_name') == 'filter_movie':
            release = self.is_activate_filter(form, 'year_')
            genre = self.is_activate_filter(form, 'genre_')
            director = self.is_activate_filter(form, 'director_')
            self.update_context_session(release, genre, director)
        else:
            release = session.get('is_active_years')
            genre = session.get('is_active_genres')
            director = session.get('is_active_directors')
            self.update_context_session(release, genre, director)
        # фильтруем фильмы
        return self.activate_filter(release, genre, director)

    @staticmethod
    def is_activate_filter(form, filter_name):
        list_activate_filter = []
        for _filter in form:
            if _filter.startswith(filter_name):
                filter_id = _filter[len(filter_name):]
                list_activate_filter.append(int(filter_id))
        print(list_activate_filter)
        return list_activate_filter

    @staticmethod
    def activate_filter(active_release, active_genre, active_directors):
        movies = Movie.query
        if active_release:
            movies = movies.join(Release).filter(Release.id.in_(active_release))
        if active_genre:
            movies = movies.join(genre_movie).join(Genre).options(
                joinedload(Movie.genres)).filter(Genre.id.in_(active_genre))
        if active_directors:
            movies = movies.join(director_movie).join(Director).options(
                joinedload(Movie.genres)).filter(Director.id.in_(active_directors))
        return movies


class SortingMovie(ContextData):
    def get_name_sorted(self, name):
        for n in self.data_sorted:
            if n.get('value') == name:
                return n.get('text')

    def sort_movie(self, movie, form=None):
        if form and form.get('form_name') == 'sorted_movie':
            sorting = form.get('sorted')
            self.session_data('sorted', sorting)
            self.context["sorted_name"] = self.get_name_sorted(sorting)
        else:
            sorting = session.get('sorted')
            self.context["sorted_name"] = self.get_name_sorted(sorting)

        if sorting == "rating_asc":
            return movie.join(RatingKinopoisk).order_by(RatingKinopoisk.star.asc())

        if sorting == "rating_desc":
            return movie.join(RatingKinopoisk).order_by(RatingKinopoisk.star.desc())

        if sorting == "release_date_asc":
            if session.get('is_active_years'):
                return movie.order_by(Release.year.asc())
            return movie.join(Release).order_by(Release.year.asc())

        if sorting == "release_date_desc":
            if session.get('is_active_years'):
                return movie.order_by(Release.year.desc())
            return movie.join(Release).order_by(Release.year.desc())

        if sorting == "standard":
            return movie.order_by(Movie.id.desc())

        return movie
