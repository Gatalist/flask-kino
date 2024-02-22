from flask import jsonify
from datetime import datetime
import math
import os
from pathlib import Path
from slugify import slugify
from flask import session
from sqlalchemy.orm import joinedload
from werkzeug.http import HTTP_STATUS_CODES
from app.settings import Config
from app import db
from app.users.service import Authorization
from .models import (Movie, RatingKinopoisk, RatingFilmCritics, RatingImdb, Reliase, TypeVideo, AgeLimit, Country,
                     Genre, Director, Creator, Actor, Screenshot, Similars, Trailer, FilmLength, genre_movie,
                     director_movie)


class MixinMovie:
    data_sorted = [
        {'value': "standard", 'text': 'стандартная'},
        {'value': "rating_asc", 'text': 'От мин до мах рейтинга'},
        {'value': "rating_desc", 'text': "От мах до мин рейтинга"},
        {'value': "release_date_asc", 'text': 'От старых до новых'},
        {'value': "release_date_desc", 'text': 'От новых до старых'}, ]

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
        return Reliase.query.order_by(Reliase.year.desc())

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
            movies = movies.join(Reliase).filter(Reliase.id.in_(active_release))
        if active_genre:
            movies = movies.join(genre_movie).join(Genre).options(
                joinedload(Movie.genres)).filter(Genre.id.in_(active_genre))
        if active_directors:
            movies = movies.join(director_movie).join(Director).options(
                joinedload(Movie.genres)).filter(Director.id.in_(active_directors))
        return movies

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
                return movie.order_by(Reliase.year.asc())
            return movie.join(Reliase).order_by(Reliase.year.asc())

        if sorting == "release_date_desc":
            if session.get('is_active_years'):
                return movie.order_by(Reliase.year.desc())
            return movie.join(Reliase).order_by(Reliase.year.desc())

        if sorting == "standard":
            return movie.order_by(Movie.id.desc())

        return movie


class JsonifyObject:
    @staticmethod
    def objects_in_page(page: int, obj: object) -> object:
        # Вычислите начальный и конечный индексы для выборки фильмов
        start = (page - 1) * Config.PAGINATE_ITEM_IN_PAGE
        end = start + Config.PAGINATE_ITEM_IN_PAGE
        # Выберите объекты для текущей страницы
        return obj[start:end]

    @staticmethod
    def serialize_object(obj: object, model_schema: object, many: bool) -> object:
        schema = model_schema(many=many)
        return schema.dump(obj)

    @staticmethod
    def json_response_one(serialize_obj):
        return jsonify(serialize_obj)

    @staticmethod
    def json_response_many(serialize_obj, obj_count: int, page: int or None):
        if page:
            pagination = {
                "pages": math.ceil(obj_count / Config.PAGINATE_ITEM_IN_PAGE),
                "current_page": page,
                "items": obj_count,
                "item_in_page": len(serialize_obj)
            }

            return jsonify({
                "pagination": pagination,
                "objects": serialize_obj
            })
        else:
            return jsonify({
                "items": obj_count,
                "objects": serialize_obj
            })

    @staticmethod
    def error_response(status_code, message=None):
        payload = {'error': HTTP_STATUS_CODES.get(status_code, 'Unknown error')}
        if message:
            payload['message'] = message
        response = jsonify(payload)
        response.status_code = status_code
        return response


class File:
    # проверяем путь к файлу, если его нет то создаем
    @staticmethod
    def get_or_create_path(path) -> str:
        if os.path.exists(path):
            return path
        Path(path).mkdir(parents=True)
        return path

    # генерируем путь к папке фильма
    def generate_path(self, *args) -> str:
        new_path = os.path.join(*args)
        return self.get_or_create_path(new_path)

    # сохраняем изображение и возвращаем путь
    @staticmethod
    def save_image(new_name, path_image, file) -> str or None:
        current_date = str(datetime.now().date())
        current_time = str(datetime.now().time()).split('.')[0].replace(':', '-')
        date_time = current_date + '-' + current_time
        if file:
            type_img = file.filename.split('.')[-1]
            new_name_image = f"{new_name}-{date_time}.{type_img}"

            path_img = os.path.join(path_image, new_name_image)

            # Сохраняем файл на сервере
            file.save(path_img)

            return path_img.replace('/home/app/app', '')

        return None

    # сохраняем изображение перебором в цикле
    def save_image_list(self, name, path_image, image_list) -> list:
        print("\n----------- Save File ----------")
        image_path = []
        i = 1
        if image_list:
            for image in image_list:
                new_name = f"{i}_{name}"
                new_path = self.save_image(new_name, path_image, image)
                image_path.append(new_path)
                i += 1
        return image_path


class CRUD:
    @staticmethod
    def get_object(model, **kwargs) -> object:
        # Пытаемся найти объект
        instance = model.query.filter_by(**kwargs).first()
        if instance:
            print(f"get obj > {model.__name__}:", instance)
            # Возвращаем информацию о новом объекте
            return instance
        # return None

    @staticmethod
    def create_object(model, **kwargs) -> object:
        # создаем новый объект
        new_instance = model(**kwargs)
        db.session.add(new_instance)
        db.session.commit()
        print(f"create obj > {model.__name__}:", new_instance)
        # Возвращаем информацию о новом объекте
        return new_instance

    def get_or_create_object(self, model, **kwargs) -> object:
        filtered_kwargs = {key: value for key, value in kwargs.items() if value is not None}
        if filtered_kwargs:
            instance = self.get_object(model, **kwargs)
            if instance:
                # Возвращаем информацию о новом объекте
                return instance
            else:
                # Возвращаем информацию о новом объекте
                return self.create_object(model, **kwargs)

    def delete_object(self, model, **kwargs):
        instance = self.get_object(model, **kwargs)
        if instance:
            db.session.delete(instance)
            db.session.commit()
            print("DELETE OBJECT")
            return True
        print("NOT DELETE OBJECT")

    def update_object(self, model, **kwargs):
        instance = self.get_object(model, **kwargs)
        if instance:
            instance.update(**kwargs)
            db.session.commit()
            print("UPDATE OBJECT")
        print("NOT UPDATE OBJECT")

    @staticmethod
    def converting_date_time(date_string) -> datetime:
        # конвертируем дату
        if date_string:
            # Формат строки даты и времени
            date_format = "%Y-%m-%d %H:%M:%S"
            # Преобразование строки в объект datetime
            return datetime.strptime(date_string, date_format)

    # связываем таблицы
    @staticmethod
    def related_table(obj, attr, list_data) -> object:
        print(f"related table > Movie:", attr)
        if hasattr(obj, attr):
            for item in list_data:
                getattr(obj, attr).append(item)
                print(item)
            return obj

    @staticmethod
    def generate_slug(name_ru, name_original):
        last_obj = Movie.query.order_by(Movie.id.desc()).first()
        idd = last_obj.id + 1
        print(idd, name_ru, name_original)
        if name_original:
            string = str(idd) + ' ' + name_original
        else:
            string = str(idd) + ' ' + name_ru
        return slugify(string)


class MovieCRUD(CRUD, Authorization, File):
    def get_or_create_movie(self, request_data):
        # Получаем данные из формы
        kinopoisk_id = request_data.form.get('kinopoisk_id', None)
        imdb_id = request_data.form.get('imdb_id', None)
        name_ru = request_data.form.get('name_ru', None)
        name_original = request_data.form.get("name_original", None)
        rating_kinopoisk = self.get_or_create_object(RatingKinopoisk,
                                                     star=request_data.form.get("rating_kinopoisk", None))
        rating_imdb = self.get_or_create_object(RatingImdb, star=request_data.form.get("rating_imdb", None))
        rating_critics = self.get_or_create_object(RatingFilmCritics,
                                                   star=request_data.form.get("rating_critics", None))
        year = self.get_or_create_object(Reliase, year=request_data.form.get("year", None))
        film_length = self.get_or_create_object(FilmLength, length=request_data.form.get("film_length", None))
        slogan = request_data.form.get("slogan", None)
        description = request_data.form.get("description", None)
        short_description = request_data.form.get("short_description", None)
        type_video = self.get_or_create_object(TypeVideo, name=request_data.form.get("type_video", None))
        age_limits = self.get_or_create_object(AgeLimit, name=request_data.form.get("age_limits", None))
        last_syncs = self.converting_date_time(request_data.form.get("last_syncs", None))

        if not year:
            return None
        # проверяем есть ли уже такой фильм
        # movie = self.get_object(Movie, kinopoisk_id=input_data.get("kinopoisk_id"))
        # if movie:
        #     return movie

        # Создаем фильм
        movie = Movie(
            kinopoisk_id=kinopoisk_id,
            imdb_id=imdb_id,
            name_ru=name_ru,
            name_original=name_original,
            rating_kinopoisk=rating_kinopoisk,
            rating_imdb=rating_imdb,
            rating_critics=rating_critics,
            year=year,
            film_length=film_length,
            slogan=slogan,
            description=description,
            short_description=short_description,
            type_video=type_video,
            age_limits=age_limits,
            last_syncs=last_syncs
        )

        db.session.add(movie)

        # Получаем файлы из формы
        poster = request_data.files.get('poster_url')
        screen_img = request_data.files.getlist('screen_img')

        # Сохраняем файлы
        poster_img_path = self.generate_path(Config.MEDIA_PATH, 'images', str(year), kinopoisk_id)
        list_screen_img = []
        number = 0
        for image_file in screen_img:
            screen_img_path = self.generate_path(Config.MEDIA_PATH, 'images', str(year), kinopoisk_id)
            img = self.save_image(f"{number}_screen", screen_img_path, image_file)
            list_screen_img.append(img)

            number += 1

        print(list_screen_img)
        token = request_data.headers.get(Config.TOKEN_NAME)
        print(token)

        movie.poster_url = self.save_image("poster", poster_img_path, poster)
        movie.user = self.unsecret_token(token)
        movie.slug = self.generate_slug(name_ru, name_original)

        countries = [self.get_or_create_object(Country, name=item) for item in request_data.form.get("countries", [])]
        genres = [self.get_or_create_object(Genre, name=item) for item in request_data.form.get("genres", [])]
        director = [self.get_or_create_object(Director, name=item) for item in request_data.form.get("director", [])]
        creator = [self.get_or_create_object(Creator, name=item) for item in request_data.form.get("creator", [])]
        actor = [self.get_or_create_object(Actor, name=item) for item in request_data.form.get("actor", [])]
        screen_img = [
            self.create_object(Screenshot, kinopoisk_id=kinopoisk_id, name="movie_id_{kinopoisk_id}_screen", url=item)
            for item in list_screen_img]
        similar = [self.get_or_create_object(Similars, kinopoisk_id=item.get('id'), name=item.get('name')) for item in
                   request_data.form.get("similar", [])]
        trailer = [self.create_object(Trailer, kinopoisk_id=item.get("kinopoisk_id"), name=item.get("name"),
                                      url=item.get("url")) for item in request_data.form.get("trailer", [])]

        self.related_table(obj=movie, attr='countries', list_data=countries)
        self.related_table(obj=movie, attr='genres', list_data=genres)
        self.related_table(obj=movie, attr='director', list_data=director)
        self.related_table(obj=movie, attr='creator', list_data=creator)
        self.related_table(obj=movie, attr='actor', list_data=actor)
        self.related_table(obj=movie, attr='screen_img', list_data=screen_img)
        self.related_table(obj=movie, attr='similar', list_data=similar)
        self.related_table(obj=movie, attr='trailer', list_data=trailer)

        db.session.commit()
        return movie
