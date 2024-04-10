from api_new import ParserKinopoiskIMDB, DataBase, Processing
from datetime import datetime
import time


parser = ParserKinopoiskIMDB()
db = DataBase()
processing = Processing()


# start id -> 298 -> 4 647 040 +-
def parse_and_create_movie(start_id: int, end_id: int):
    # получение данных с api
    for movie_id in range(start_id, end_id):
        print(f'\n\n----> kinopoisk id: {movie_id} <-----')
        # проверяем нет ли в базе фильма с kinopoisk_id = movie_id
        if not processing.get_movie(movie_id):
            # получаем все данные для фильма
            print('\n----------  Получение данных для фильма ----------\n')
            movie = parser.request_data_movie(kinopoisk_id=movie_id)
            if movie == "Forbidden":
                break

            if not parser.current_key:
                print("Not API key")
                break

            if movie and movie != 404:
                people = parser.request_data_people(kinopoisk_id=movie.get('kinopoiskId'))
                popular_actor = processing.popular_actor(people.get('actor'))
                similar = parser.request_data_similar(kinopoisk_id=movie.get('kinopoiskId'))
                screen_and_trailer = parser.request_movie_screenshot(imdb_id=movie.get('imdbId'))

                # сохраняем картинки и возвращаем ссылки на них
                path = parser.generate_path(movie)
                poster = parser.save_image(name='postr', path_image=path, image_url=movie.get('posterUrl'))
                screenshot_path = parser.save_image_list(
                    name='image', path_image=path, image_list=screen_and_trailer.get('screenshots', None))

                # записываем данные в таблицы
                rating_kinopoisk = processing.get_or_create_rating_kinopoisk(movie.get('ratingKinopoisk'))
                rating_imdb = processing.get_or_create_rating_imdb(movie.get('ratingImdb'))
                rating_critics = processing.get_or_create_rating_critics(movie.get('ratingFilmCritics'))
                release = processing.get_or_create_release(movie.get('year'))
                film_length = processing.get_or_create_film_length(movie.get('filmLength'))
                type_video = processing.get_or_create_type_video(movie.get('type'))
                age_limit = processing.get_or_create_age_limit(movie.get('ratingAgeLimits'))
                genre = processing.get_or_create_genre(elem_list=movie.get('genres'))
                country = processing.get_or_create_country(elem_list=movie.get('countries'))
                director = processing.get_or_create_director(elem_list=people.get('director'))
                actor = processing.get_or_create_actor(list_actor=popular_actor, count_actor_save=12)
                creator = processing.get_or_create_creator(elem_list=people.get('creator'))
                screenshot = processing.create_screen_movie(movie.get('kinopoiskId', None), screenshot_path)
                similar = processing.get_or_create_similar(similar)
                new_url = processing.generate_url(movie)

                # создаем фильм
                new_movie = processing.create_movie(kinopoisk_id=movie.get('kinopoiskId', None),
                                                    imdb_id=movie.get('imdbId', None),
                                                    name_ru=movie.get('nameRu'),
                                                    name_original=movie.get('nameOriginal'),
                                                    poster_url=poster,
                                                    slug=new_url,
                                                    rating_kinopoisk_id=rating_kinopoisk,
                                                    rating_imdb_id=rating_imdb,
                                                    rating_critics_id=rating_critics,
                                                    year_id=release,
                                                    film_length_id=film_length,
                                                    slogan=movie.get('slogan'),
                                                    description=movie.get('description'),
                                                    short_description=movie.get('shortDescription'),
                                                    type_video_id=type_video,
                                                    age_limits_id=age_limit,
                                                    last_syncs=db.converting_date_time(movie.get('lastSync')),
                                                    user_id=processing.get_user('Admin'),
                                                    created_on=datetime.now())

                #  сохраняем данные в связанные таблицы many-to-many
                db.related_table(table_name='genre_movie', movie_id=new_movie, list_data=genre)
                db.related_table(table_name='country_movie', movie_id=new_movie, list_data=country)
                db.related_table(table_name='director_movie', movie_id=new_movie, list_data=director)
                db.related_table(table_name='actor_movie', movie_id=new_movie, list_data=actor)
                db.related_table(table_name='creator_movie', movie_id=new_movie, list_data=creator)
                db.related_table(table_name='screenshot_movie', movie_id=new_movie, list_data=screenshot)
                db.related_table(table_name='similar_movie', movie_id=new_movie, list_data=similar)
        else:
            print('\n Фильм уже существует\n')
        print('\n--------- Finish ----------\n\n\n')
        time.sleep(2)


#  if database clear
#  before start first parser need next step
#  add role, add user Admin, add tag popular-actor, run create_popular_actor
# processing.create_popular_actor(file_actor_name='actor/actor.txt', tag_id=1)
# processing.create_popular_actor(file_actor_name='actor/1965.txt', tag_id=2)  # 1965

#  9000  9500
#  9500  10000
start = int(input("Enter number start: "))
end = int(input("Enter number end: "))
parse_and_create_movie(start_id=start, end_id=end)
