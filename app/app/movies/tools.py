from app import db, settings
import shutil
import os
from .models import (
    segment_movie, actor_movie, country_movie, creator_movie, Movie, Actor,
    director_movie, genre_movie, screenshot_movie, similar_movie, user_movie
)


class MovieTools:
    @staticmethod
    def delete_image(movie):
        #  Удаление папки со всеми картинками
        print(f'Deleting object: {movie}')

        media = settings.Config.MEDIA_PATH
        media_path = os.path.join(media, 'images', str(movie.year), str(movie.kinopoisk_id))
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

    @staticmethod
    def link_many_to_many(movie, link_table):
        # Удаляем записи с таблицы many to many
        records = db.session.query(link_table).filter(link_table.c.movie_id == movie.id).delete(synchronize_session=False)
        print(records)

        # Сохранить изменения в базе данных
        db.session.commit()
        print("\ndelete link", '[', link_table, ']')
