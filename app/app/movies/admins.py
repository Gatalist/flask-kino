from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from app import settings  # , db
import shutil
import os
from .delete_from_many_to_many import delete_movie


class MovieView(ModelView):
    column_list = ['id', 'poster_url', 'kinopoisk_id', 'imdb_id', 'name_ru', 'slug', 'year',
                   'type_video', 'rating_kinopoisk', 'rating_imdb', 'rating_critics']

    column_filters = ['rating_critics.star', 'rating_kinopoisk.star', 'rating_imdb.star']

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

        # delete_movie(model)
    # edit_template = 'admin/open_card.html'

    # def custom_action(self, id):
    #     # Ваша логика обработки пользовательского действия
    #     return redirect(url_for('admin.user_edit', id=id))


class RatingKinopoiskView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class RatingImdbView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class RatingFilmCriticsView(ModelView):
    column_list = ['id', 'star', 'created_on']
    column_searchable_list = ('star',)


class ReleaseView(ModelView):
    column_list = ['id', 'year', 'created_on']
    column_searchable_list = ('year',)


class FilmLengthView(ModelView):
    column_list = ['id', 'length', 'created_on']
    column_searchable_list = ('length',)


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


class DirectorView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class CreatorView(ModelView):
    column_list = ['id', 'name', 'created_on']
    column_searchable_list = ('name',)


class ActorView(ModelView):
    column_list = ['id', 'name', 'tag', 'created_on']
    column_searchable_list = ('name',)


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
