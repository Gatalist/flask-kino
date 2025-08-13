from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
import shutil
import os
from flask_admin.form import rules
from app.users.user_access import MixinUserAccessible
from app import db, settings
from .models import (
    actor_movie,
    country_movie,
    creator_movie,
    director_movie,
    genre_movie,
    screenshot_movie,
    similar_movie,
    user_movie,
    segment_movie,
    video_movie
)


class MovieView(MixinUserAccessible):
    column_list = [
        'id', 'poster_url', 'kinopoisk_id', 'imdb_id', 'name_ru', 'slug', 'year', 'type_video', 'rating_kinopoisk',
        'rating_imdb', 'rating_critics'
    ]

    custom_form_rules = (
        rules.FieldSet((
            'kinopoisk_id',
            'kinopoisk_hd_id',
            'imdb_id',
        ), 'ID-шники'),

        rules.FieldSet((
            'name_ru',
            'name_en',
            'name_uk',
            'name_original',
        ), 'Названия'),

        rules.FieldSet((
            'poster_url',
            'slug',
            'screen_img',
        ), 'Медиа'),

        rules.FieldSet((
            'year',
            'start_year',
            'end_year',
            'film_length',
        ), 'Годы и длительность'),

        rules.FieldSet((
            'director',
            'creator',
            'actor',
        ), 'Персонал'),

        rules.FieldSet((
            'countries',
            'genres',
            'description',
            'short_description',
            'editor_annotation',
            'slogan',
        ), 'Описание'),

        rules.FieldSet((
            'rating_mpaa',
            'rating_kinopoisk',
            'rating_imdb',
            'rating_critics',
        ), 'Рейтинги'),

        rules.FieldSet((
            'has_3d',
            'has_imax',
            'short_film',
            'serial',
            'completed',
        ), 'Флаги'),

        rules.FieldSet((
            'user',
        ), 'Пользователь'),
    )

    form_edit_rules = custom_form_rules
    form_create_rules = custom_form_rules

    form_excluded_columns = ('created_on', 'updated_on')

    column_filters = [
        'rating_critics.star', 'rating_kinopoisk.star', 'rating_imdb.star'
    ]

    column_searchable_list = ('kinopoisk_id',)

    column_sortable_list = [
        'id', 'kinopoisk_id', 'year', 'rating_critics.star', 'rating_kinopoisk.star', 'rating_imdb.star'
    ]

    # Определите, как отображать изображение в списке элементов
    column_formatters = {
        'poster_url': lambda view, context, model, name: Markup(
            f'<img src="{model.poster_url}" width="70" height="auto">') if model.poster_url else ''
    }

    def on_model_delete(self, model):
        # удалить картинки с папки фильма
        self.delete_image(model)
        # удалить зависимости с таблиц
        self.dell_from_table(model)

    @staticmethod
    def delete_image(movie):
        #  Удаление папки со всеми картинками
        print(f'Deleting object: {movie}')

        media = settings.Config.MEDIA_PATH
        media_path = os.path.join(media, 'movie', str(movie.year), str(movie.kinopoisk_id))
        print(media_path)

        try:
            shutil.rmtree(media_path)
            print(f"Папка {media_path} удалена успешно.")
        except FileNotFoundError:
            print(f"Папка {media_path} не найдена.")
        except Exception as e:
            print(f"Ошибка при удалении папки: {e}")

    def dell_from_table(self, movie):
        self.link_many_to_many(movie, actor_movie)
        self.link_many_to_many(movie, country_movie)
        self.link_many_to_many(movie, creator_movie)
        self.link_many_to_many(movie, director_movie)
        self.link_many_to_many(movie, genre_movie)
        self.link_many_to_many(movie, screenshot_movie)
        self.link_many_to_many(movie, similar_movie)
        self.link_many_to_many(movie, user_movie)
        self.link_many_to_many(movie, segment_movie)
        self.link_many_to_many(movie, video_movie)

    @staticmethod
    def link_many_to_many(movie, link_table):
        # Удаляем записи с таблицы many to many
        records = db.session.query(link_table).filter(link_table.c.movie_id == movie.id).all()
        # print(records)
        for record in records:
            db.session.query(link_table).filter(link_table.c.movie_id == record[0]).delete()

        # Сохранить изменения в базе данных
        db.session.commit()
        print("\ndelete link", '[', link_table, ']')


class RatingKinopoiskView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class RatingImdbView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class RatingFilmCriticsView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class RatingAwaitView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class RatingMPAAView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class ReleaseView(ModelView):
    column_list = ['id', 'year', 'created_on']
    column_searchable_list = ('year',)


class FilmLengthView(ModelView):
    column_list = ['id', 'length', 'created_on']
    column_searchable_list = ('length',)


class ProductionStatusView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class GenreView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class CountryView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class AgeLimitView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class TypeVideoView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class PersonView(ModelView):
    column_list = ['id', 'name_ru', 'person_id', 'created_on']
    column_searchable_list = ('name_ru',)


class ScreenshotView(ModelView):
    pass


class SimilarView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class TagActorView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class SegmentView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class VideoView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class VideoSourceView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)
