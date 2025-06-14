import requests
from flask import session
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.util import _ORMJoin
from .models import (Movie, RatingKinopoisk, Release, Genre, Person, Country, genre_movie, director_movie, country_movie)


class ContextData:
    context = {}
    all_sorting = [
        {'id': "date_desc", 'value': 'По дате (новые)'},
        {'id': "date_asc", 'value': 'По дате (старые)'},
        {'id': "rating_desc", 'value': "По рейтингу (высокий)"},
        {'id': "rating_asc", 'value': 'По рейтингу (низкий)'},
        {'id': "title_desc", 'value': 'По названию (A-Z)'},
        {'id': "title_asc", 'value': 'По названию (Z-A)'},
    ]

    def create_context(self):
        self.context["all_sorting"] = self.all_sorting
        self.context["all_release"] = self.get_years()
        self.context["all_genres"] = self.get_genres()
        self.context["all_directors"] = self.top_directors()
        self.context["all_countries"] = self.get_countries()

    @staticmethod
    def top_directors():
        if len(Person.query.all()) > 0:
            _directors = Person.query.join(director_movie).group_by(Person.id).order_by(Person.id.desc())[:15]
            return [{'id': elem.id, 'value': elem.name} for elem in _directors]
        else:
            return []

    @staticmethod
    def get_countries():
        if len(Country.query.all()) > 0:
            _countries = Country.query.join(country_movie).group_by(Country.id).order_by(Country.id.desc())[:15]
            return [{'id': elem.id, 'value': elem.name} for elem in _countries]
        else:
            return []

    @staticmethod
    def get_genres():
        _genres = Genre.query
        return [{'id': elem.id, 'value': elem.name} for elem in _genres]

    @staticmethod
    def get_years():
        _years = Release.query.order_by(Release.year.desc())
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
    def activate_filter() -> object:
        release = session.get('is_active_years')
        genre = session.get('is_active_genres')
        country = session.get('is_active_countries')
        director = session.get('is_active_directors')
        sorting = session.get('is_active_sorted')

        joined_table = []
        query = Movie.query
        print("join_tables 1:", joined_table)

        if release:
            if "Release" not in joined_table:
                query = query.join(Release, Movie.year_id == Release.id)
                joined_table.append("Release")
            query = query.filter(Release.id.in_(release))

        if genre:
            if "Genre" not in joined_table:
                query = query.join(genre_movie).join(Genre)
                joined_table.append("Genre")
            query = query.options(joinedload(Movie.genres)).filter(Genre.id.in_(genre))

        if country:
            if "Country" not in joined_table:
                query = query.join(country_movie).join(Country)
                joined_table.append("Country")
            query = query.options(joinedload(Movie.countries)).filter(Country.id.in_(country))

        # if director:
        #     if "Director" not in joined_table:
        #         query = query.join(director_movie).join(Director)
        #         joined_table.append("Director")
        #     query = query.options(joinedload(Movie.genres)).filter(Director.id.in_(director))

        if sorting:
            if sorting == "rating_asc" or sorting == "rating_desc":
                if "RatingKinopoisk" not in joined_table:
                    query = query.join(RatingKinopoisk, Movie.rating_kinopoisk_id == RatingKinopoisk.id)
                    joined_table.append("RatingKinopoisk")

                if sorting == "rating_asc":
                    query = query.order_by(RatingKinopoisk.star.asc())

                if sorting == "rating_desc":
                    query = query.order_by(RatingKinopoisk.star.desc())

            if sorting == "date_asc" or sorting == "date_desc":
                if "Release" not in joined_table:
                    query = query.join(Release, Movie.year_id == Release.id)
                    joined_table.append("Release")

                if sorting == "date_asc":
                    query = query.order_by(Release.year.asc())

                if sorting == "date_desc":
                    query = query.order_by(Release.year.desc())

        print("join_tables 2:", joined_table)
        return query
