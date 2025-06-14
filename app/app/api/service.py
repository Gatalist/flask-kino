from flask import jsonify, request
from werkzeug.http import HTTP_STATUS_CODES
from datetime import timedelta, datetime
from functools import wraps
import math
import jwt
import os
from pathlib import Path
from slugify import slugify
from app.settings import Config
from app import db
from app.users.models import User
from app.movies.models import (Movie, RatingKinopoisk, RatingCritic, RatingImdb, Release, TypeVideo, AgeLimit,
                               Country, Genre, Person, Screenshot, Similar, FilmLength, Video)


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


class Authorization(JsonifyObject):
    def create_user(self, input_data):
        # create_validation_schema = CreateUserSchema()

        # errors = create_validation_schema.validate(input_data)
        # if errors:
        #     return {'username': 'len be 4', 'pass': 'len be 6'}

        username = input_data.get('username', None)
        email = input_data.get('email', None)
        password = input_data.get('password', None)

        check_username_exist = User.query.filter_by(username=username).first()
        if check_username_exist:
            return jsonify({'error': 'Username already exist'})

        check_email_exist = User.query.filter_by(email=email).first()
        if check_email_exist:
            return jsonify({'error': 'Email already taken'})

        new_user = User(
            username=username,
            email=email
        )

        if new_user:
            new_user.set_password(password)
            db.session.add(new_user)  # Adds new User record to database
            db.session.commit()  # Comment

            return jsonify({
                'id': new_user.id,
                'username': new_user.username,
                'email': new_user.email,
                'token': self.generate_jwt_token(new_user),
            })

        return jsonify({"error": "user not created, server error"})

    def login_user(self, input_data):
        email = input_data.get("email", None)
        password = input_data.get("password", None)

        get_user = User.query.filter_by(email=email).first()
        if get_user is None:
            return self.error_response(status_code=404, message="User not found")

        if get_user.check_password(password):
            token = self.generate_jwt_token(get_user)
            return jsonify({Config.TOKEN_NAME: token})
        else:
            return self.error_response(status_code=404, message="Password is wrong")

    # расшифровываем токен
    @staticmethod
    def decrypt_token(token):
        data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        print(data)
        user = User.query.filter_by(id=data['id']).first()
        print(user)
        if user:
            return user

    def token_required(self, f):
        @wraps(f)
        def decorator(*args, **kwargs):
            token = request.headers.get(Config.TOKEN_NAME, None)
            if not token:
                return jsonify({'message': 'not found token'})
            user = self.decrypt_token(token)
            if user:
                if user.active:
                    kwargs["user_id"] = user.id
                else:
                    return self.error_response(status_code=404, message="token is invalid or user deactivate")
            else:
                return self.error_response(status_code=404, message="User not found")
            return f(*args, **kwargs)

        return decorator

    @staticmethod
    def generate_jwt_token(data, lifetime=None):
        """ Generates a new JWT token, wrapping information provided by payload (dict)
        Lifetime describes (in minutes) how much time the token will be valid """
        payload = {"id": data.id, "email": data.email, "password": data.password}
        if lifetime:
            payload['exp'] = (datetime.now() + timedelta(minutes=lifetime)).timestamp()
        return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")


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
                # Возвращаем информацию об найденном объекте
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
        else:
            print("NOT DELETE OBJECT")

    def update_object(self, model, **kwargs):
        instance = self.get_object(model, **kwargs)
        if instance:
            instance.update(**kwargs)
            db.session.commit()
            print("UPDATE OBJECT")
            return True
        else:
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
    def save_image(file, path_image, new_name) -> str or None:
        if file:
            type_img = file.filename.split('.')[-1]
            new_name_image = f"{new_name}.{type_img}"
            path_img = os.path.join(path_image, new_name_image)
            # Сохраняем файл на сервере
            file.save(path_img)
            print("\n----------- Save File ----------")
            return path_img.replace('/home/app/app', '')
        return None

    @staticmethod
    def create_str_date():
        # Укажите формат даты и времени с миллисекундами
        date_format = "%Y-%m-%d_%H.%M.%S.%f"
        # Получите текущую дату и время
        current_time = datetime.now()
        # Преобразуйте текущую дату и время в строку с учетом миллисекунд
        formatted_time = current_time.strftime(date_format)
        # Замените двоеточия на точки
        formatted_time = formatted_time.replace(':', '.')
        print(formatted_time)
        return formatted_time


class MovieCRUD(CRUD, Authorization, File):
    def det_data_movie(self, request_data):
        arg_list = dict()
        arg_list['kinopoisk_id'] = request_data.form.get('kinopoisk_id', None)
        arg_list['imdb_id'] = request_data.form.get('imdb_id', None)
        arg_list['name_ru'] = request_data.form.get('name_ru', None)
        arg_list['name_original'] = request_data.form.get("name_original", None)
        arg_list['rating_kinopoisk'] = self.get_or_create_object(RatingKinopoisk,
                                                                 star=request_data.form.get("rating_kinopoisk", None))
        arg_list['rating_imdb'] = self.get_or_create_object(RatingImdb, star=request_data.form.get("rating_imdb", None))
        arg_list['rating_critics'] = self.get_or_create_object(RatingCritic,
                                                               star=request_data.form.get("rating_critics", None))
        arg_list['year'] = self.get_or_create_object(Release, year=request_data.form.get("year", None))
        arg_list['film_length'] = self.get_or_create_object(FilmLength,
                                                            length=request_data.form.get("film_length", None))
        arg_list['slogan'] = request_data.form.get("slogan", None)
        arg_list['description'] = request_data.form.get("description", None)
        arg_list['short_description'] = request_data.form.get("short_description", None)
        arg_list['type_video'] = self.get_or_create_object(TypeVideo, name=request_data.form.get("type_video", None))
        arg_list['age_limits'] = self.get_or_create_object(AgeLimit, name=request_data.form.get("age_limits", None))
        arg_list['last_syncs'] = self.converting_date_time(request_data.form.get("last_syncs", None))
        return arg_list

    def get_or_create_movie(self, request_data):
        # Получаем данные из формы
        data_movie = self.det_data_movie(request_data)

        kinopoisk_id = request_data.form.get('kinopoisk_id', None)
        year = request_data.form.get("year", None)
        name_ru = request_data.form.get('name_ru', None)
        name_original = request_data.form.get("name_original", None)

        # проверяем есть ли уже такой фильм
        # movie = self.get_object(Movie, kinopoisk_id=input_data.get("kinopoisk_id"))
        # if movie:
        #     return movie

        # Создаем фильм
        movie = Movie(**data_movie)
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
            new_name = f"{number}_screen-{self.create_str_date()}"
            img = self.save_image(image_file, screen_img_path, new_name)
            list_screen_img.append(img)

            number += 1

        print(list_screen_img)
        token = request_data.headers.get(Config.TOKEN_NAME)
        print(token)

        movie.poster_url = self.save_image("poster", poster_img_path, poster)
        movie.user = self.decrypt_token(token)
        movie.slug = self.generate_slug(name_ru, name_original)

        countries = [self.get_or_create_object(Country, name=item) for item in request_data.form.get("countries", [])]
        genres = [self.get_or_create_object(Genre, name=item) for item in request_data.form.get("genres", [])]
        director = [self.get_or_create_object(Person, name=item) for item in request_data.form.get("director", [])]
        creator = [self.get_or_create_object(Person, name=item) for item in request_data.form.get("creator", [])]
        actor = [self.get_or_create_object(Person, name=item) for item in request_data.form.get("actor", [])]
        screen_img = [
            self.create_object(Screenshot, kinopoisk_id=kinopoisk_id, name="movie_id_{kinopoisk_id}_screen", url=item)
            for item in list_screen_img]
        similar = [self.get_or_create_object(Similar, kinopoisk_id=item.get('id'), name=item.get('name')) for item in
                   request_data.form.get("similar", [])]
        trailer = [self.create_object(Video, kinopoisk_id=item.get("kinopoisk_id"), name=item.get("name"),
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
