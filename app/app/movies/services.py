import requests
from flask import session
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.util import _ORMJoin
from .models import (Movie, Rating, Release, Genre, Person, Country, genre_movie, director_movie, country_movie)
from app import db

class ContextData:
    context = {}

    all_sorting = [
        {'id': "date_desc", 'value': 'По дате (новые)'},
        {'id': "date_asc", 'value': 'По дате (старые)'},
        {'id': "rating_desc", 'value': "По рейтингу (высокий)"},
        {'id': "rating_asc", 'value': 'По рейтингу (низкий)'},
        {'id': "title_asc", 'value': 'По названию (A-Z)'},
        {'id': "title_desc", 'value': 'По названию (Z-A)'},
    ]

    def create_context(self):
        self.context["all_sorting"] = self.all_sorting
        self.context["all_release"] = self.get_years()
        self.context["all_genres"] = self.get_genres()
        self.context["all_directors"] = self.top_directors()
        self.context["all_countries"] = self.get_countries()

    @staticmethod
    def top_directors():
        # Проверяем наличие хотя бы 1 записи
        if not db.session.query(Person.id).first():
            return []

        _directors = (
            db.session.query(Person.id, Person.name_ru)
            .join(director_movie)
            .group_by(Person.id)
            .order_by(Person.id.desc())
            .limit(15)
        )
        return [{'id': elem.id, 'value': elem.name_ru} for elem in _directors]

    @staticmethod
    def get_countries():
        if not db.session.query(Country.id).first():
            return []

        _countries = (
            db.session.query(Country.id, Country.name)
            .join(country_movie)
            .group_by(Country.id)
            .order_by(Country.id.desc())
            .limit(15)
        )

        return [{'id': elem.id, 'value': elem.name} for elem in _countries]

    @staticmethod
    def get_genres():
        _genres = (
            db.session.query(Genre.id, Genre.name)
            .order_by(Genre.name.asc())
        )
        return [{'id': elem.id, 'value': elem.name} for elem in _genres]

    @staticmethod
    def get_years():
        _years = (
            db.session.query(Release.id, Release.year)
            .order_by(Release.year.desc())
        )
        return [{'id': elem.id, 'value': elem.year} for elem in _years]

    @staticmethod
    def session_data(name, data):
        session.permanent = True
        if name not in session:
            session[name] = data
        else:
            session[name] = data
        session.modified = True
        return session

    def update_context_session(self, release, genre, country, director, sorting):
        # Добавляем активные фильтры в context
        self.context["is_active_years"] = release
        self.context["is_active_genres"] = genre
        self.context["is_active_countries"] = country
        self.context["is_active_directors"] = director
        self.context["is_active_sorted"] = sorting
        # добавляем фильтра в сессию
        self.session_data('is_active_years', release)
        self.session_data('is_active_genres', genre)
        self.session_data('is_active_countries', country)
        self.session_data('is_active_directors', director)
        self.session_data('is_active_sorted', sorting)


class FilterMovie(ContextData):
    def filter_movie(self, form: requests = None) -> object:
        if form and form.get('form_name') == 'filter_movie':
            print(form)
            release = self.is_activate_filter(form, 'years')
            genre = self.is_activate_filter(form, 'genres')
            country = self.is_activate_filter(form, 'countries')
            director = self.is_activate_filter(form, 'directors')
            sorting = form.get("sorting", '')
            self.update_context_session(release, genre, country, director, sorting)
        return self.activate_filter()

    @staticmethod
    def is_activate_filter(form: requests, filter_name: str) -> list:
        active_filter = form.getlist(filter_name)

        if active_filter:
            active_filter = [int(item) for item in active_filter]
        print(filter_name, active_filter)
        return active_filter

    @staticmethod
    def activate_filter():
        release = session.get('is_active_years')
        genres = session.get('is_active_genres')
        countries = session.get('is_active_countries')
        directors = session.get('is_active_directors')
        sorting = session.get('is_active_sorted')

        query = Movie.query

        # ----- Фильтры -----
        if release:
            query = query.filter(Movie.year_id.in_(release))

        if genres:
            query = query.filter(Movie.genres.any(Genre.id.in_(genres)))

        if countries:
            query = query.filter(Movie.countries.any(Country.id.in_(countries)))

        if directors:
            query = query.filter(Movie.directors.any(Person.id.in_(directors)))

        # ----- Сортировка -----
        if sorting == "rating_asc":
            query = query.join(Rating, Movie.rating_imdb_id == Rating.id).order_by(Rating.star.asc())

        elif sorting == "rating_desc":
            query = query.join(Rating, Movie.rating_imdb_id == Rating.id).order_by(Rating.star.desc())

        elif sorting == "date_asc":
            query = query.join(Release, Movie.year_id == Release.id).order_by(Release.year.asc())

        elif sorting == "date_desc":
            query = query.join(Release, Movie.year_id == Release.id).order_by(Release.year.desc())

        elif sorting == "title_desc":
            query = query.order_by(Movie.name_ru.desc())

        elif sorting == "title_asc":
            query = query.order_by(Movie.name_ru.asc())

        return query