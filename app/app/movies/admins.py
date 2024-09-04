from flask_admin.contrib.sqla import ModelView
from markupsafe import Markup
from .tools import MovieTools


class MovieView(MovieTools, ModelView):
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
        # удалить картинки с папки фильма
        self.delete_image(model)
        # удалить зависимости с таблиц
        self.dell_from_table(model)


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
