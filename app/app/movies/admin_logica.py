import random, os
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, logout_user
from flask import url_for, redirect, request, abort
from app import settings
import shutil
from markupsafe import Markup
from flask_admin.model import typefmt



class MovieView(ModelView):   
   column_list = ['id', 'poster_url', 'kinopoisk_id', 'imdb_id', 'name_ru', 'year', 'type_video']

   column_searchable_list = ('kinopoisk_id', )

   # Определите, как отображать изображение в списке элементов
   column_formatters = {
      'poster_url': lambda view, context, model, name: Markup(f'<img src="{model.poster_url}" width="70" height="auto">') if model.poster_url else ''
   }
   

   def on_model_delete(self, model):
      # Ваша логика удаления объекта c папкой со всеми картинками
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


class RatingKinopoiskView(ModelView):
   column_list = ['id', 'star', 'created_on']


class RatingImdbView(ModelView):
   pass


class RatingFilmCriticsView(ModelView):
   pass


class ReliaseView(ModelView):
   column_list = ['id', 'year']


class FilmLengthView(ModelView):
   pass


class GenreView(ModelView):
   column_list = ['id', 'name']


class CountryView(ModelView):
   pass


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


class SimilarsView(ModelView):
   pass


class TrailerView(ModelView):
   column_list = ['id', 'name', 'url']


class TagActorView(ModelView):
   column_list = ['id', 'name', 'created_on']


class SegmentView(ModelView):
   column_list = ['id', 'name', 'created_on']
