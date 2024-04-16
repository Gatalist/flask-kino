import os
import webbrowser
import shutil
from flask_admin import BaseView, expose
from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from app import settings
from flask import url_for, redirect


class MovieView(ModelView):
    column_list = ['id', 'poster_url', 'kinopoisk_id', 'imdb_id', 'name_ru', 'slug', 'year',
                   'type_video', 'rating_kinopoisk', 'rating_imdb', 'rating_critics']

    column_searchable_list = ('kinopoisk_id',)
    column_sortable_list = ['id', 'kinopoisk_id', 'year']

    # Определите, как отображать изображение в списке элементов
    column_formatters = {
        'poster_url': lambda view, context, model, name: Markup(
            f'<img src="{model.poster_url}" width="70" height="auto">') if model.poster_url else ''
    }

    def on_model_delete(self, model):
        #  Ваша логика удаления объекта и папки со всеми картинками
        print(f'Deleting object: {model}')

        media = settings.Config.MEDIA_PATH
        media_path = os.path.join(media, 'images', str(model.year), str(model.kinopoisk_id))
        print(media_path)

        try:
            shutil.rmtree(media_path)
            print(f"Папка {media_path} удалена успешно.")
        except FileNotFoundError:
            print(f"Папка {media_path} не найдена.")
        except Exception as e:
            print(f"Ошибка при удалении папки: {e}")

    # edit_template = 'admin/open_card.html'

    # def custom_action(self, id):
    #     # Ваша логика обработки пользовательского действия
    #     return redirect(url_for('admin.user_edit', id=id))


class RatingKinopoiskView(ModelView):
    column_list = ['id', 'star', 'created_on']


class RatingImdbView(ModelView):
    pass


class RatingFilmCriticsView(ModelView):
    pass


class ReleaseView(ModelView):
    column_list = ['id', 'year']


class FilmLengthView(ModelView):
    pass


class GenreView(ModelView):
    column_list = ['id', 'name']


class CountryView(ModelView):
    column_list = ['id', 'name']

    column_searchable_list = ('name',)


class AgeLimitView(ModelView):
    pass


class TypeVideoView(ModelView):
    pass


class DirectorView(ModelView):
    pass


class CreatorView(ModelView):
    pass


class ActorView(ModelView):
    column_list = ['id', 'name', 'tag', 'created_on']

    column_labels = {
        'tag': 'Tags'
    }

    column_descriptions = {
        'tag': 'Description for tag'
    }


class ScreenshotView(ModelView):
    pass


class SimilarView(ModelView):
    column_list = ['id', 'name']
    column_searchable_list = ('name',)


class TagActorView(ModelView):
    column_list = ['id', 'name', 'created_on']


class SegmentView(ModelView):
    column_list = ['id', 'name', 'created_on']
