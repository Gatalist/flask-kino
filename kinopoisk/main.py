from api_new import ParserKinopoiskIMDB, Tools, DataBase, Processing
from datetime import datetime
import time


parser = ParserKinopoiskIMDB()
tools = Tools()
db = DataBase()
procese = Processing()



def create_popular_actor():
    file_actor = tools.read_file_actor_name('actor.txt')
    add_popular_actor = procese.get_or_create_actor(elem_list=file_actor)
    tag_id = 1

    print(add_popular_actor)
    conn = db.connect_db()
    cursor = conn.cursor()
    for actor_id in add_popular_actor:
        cursor.execute(f"INSERT INTO tag_actor VALUES (%s, %s);", (actor_id, tag_id))
    conn.commit()

    # next step
    # add role, user, tag


def parse_and_create_movie():
    # получение данных с api
    # start id -> 298 -> 4 647 040 +-
    for movie_id in range(974, 1000):
        print(f'\n\n----> kinopoisk id: {movie_id} <-----')

        # получаем все данные для фильма
        movie = parser.request_data_movie(kinopoisk_id=movie_id)
        # print(movie)
        if movie and procese.get_movie(movie.get('kinopoiskId')):
            piople = parser.request_data_piople(kinopoisk_id=movie.get('kinopoiskId'))

            popular_actor = procese.popular_actor(piople.get('actor'))

            similar = parser.request_data_similar(kinopoisk_id=movie.get('kinopoiskId'))
            screen_and_trailer = parser.request_data_screenshot_and_trailer(imdb_id=movie.get('imdbId'))

            # сохраняем картинки и возвращаем ссылки на них
            path = tools.generate_path(movie)
            poster = tools.save_image(name='postr', path_image=path,
                image_url=movie.get('posterUrl'))
            scrinshot_path = tools.save_image_list(name='image', path_image=path, 
                image_list=screen_and_trailer.get('screenshots', None))

            # записываем данные в таблицы
            rating_kinopoisk = procese.get_or_create_rating_kinopoisk(movie.get('ratingKinopoisk'))
            rating_imdb = procese.get_or_create_rating_imdb(movie.get('ratingImdb'))
            rating_critics = procese.get_or_create_rating_critics(movie.get('ratingFilmCritics'))
            reliase = procese.get_or_create_reliase(movie.get('year'))
            filmlength = procese.get_or_create_filmlength(movie.get('filmLength'))
            typevideo = procese.get_or_create_typevideo(movie.get('type'))
            agelimit = procese.get_or_create_agelimit(movie.get('ratingAgeLimits'))
            genre = procese.get_or_create_genre(elem_list=movie.get('genres'))
            country = procese.get_or_create_country(elem_list=movie.get('countries'))
            director = procese.get_or_create_director(elem_list=piople.get('director'))
            actor = procese.get_or_create_actor(elem_list=popular_actor)
            creator = procese.get_or_create_creator(elem_list=piople.get('creator'))
            screenshot = procese.create_screen_movie(movie.get('kinopoiskId', None), scrinshot_path)
            similars = procese.get_or_create_similar(similar)
            trailer = procese.create_trailer(screen_and_trailer.get('trailers', None))
            new_url = procese.generate_url(movie)

            # создаем фильм
            new_movie = procese.create_movie(kinopoisk_id=movie.get('kinopoiskId', None), imdb_id=movie.get('imdbId', None),
                name_ru=movie.get('nameRu'), name_original=movie.get('nameOriginal'),
                poster_url=poster, slug=new_url,
                rating_kinopoisk_id=rating_kinopoisk, rating_imdb_id=rating_imdb,
                rating_critics_id=rating_critics, year_id=reliase, film_length_id=filmlength,
                slogan=movie.get('slogan'), description=movie.get('description'),
                short_description=movie.get('shortDescription'), type_video_id=typevideo,
                age_limits_id=agelimit, last_syncs=db.converting_date_time(movie.get('lastSync')),
                user_id=procese.get_user('Admin'), created_on=datetime.now())

            # сохраняем данные в связаные таблицы many-to-many
            db.related_table(table_name='genre_movie', movie_id=new_movie, list_data=genre)
            db.related_table(table_name='country_movie', movie_id=new_movie, list_data=country)
            db.related_table(table_name='director_movie', movie_id=new_movie, list_data=director)
            db.related_table(table_name='actor_movie', movie_id=new_movie, list_data=actor)
            db.related_table(table_name='creator_movie', movie_id=new_movie, list_data=creator)
            db.related_table(table_name='screenshot_movie', movie_id=new_movie, list_data=screenshot)
            db.related_table(table_name='similars_movie', movie_id=new_movie, list_data=similars)
            db.related_table(table_name='trailer_movie', movie_id=new_movie, list_data=trailer)

        print('\n--------- Finish ----------\n\n\n')
        time.sleep(2)


# create_popular_actor()

parse_and_create_movie()
