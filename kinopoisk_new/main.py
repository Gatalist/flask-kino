from parser.kinopoisk import (
    WebRequesterKinopoiskMovie,
    WebRequesterKinopoiskPeople,
    WebRequesterKinopoiskSimilar
)
from parser.imdb import WebRequesterMovieScreenshotIMDB
from libs.postgres_orm import PostgresDB
from processing import FileImage
from settings import Settings


keys_1 = Settings.api_keys[1]
keys_2 = Settings.api_keys[2]
keys_3 = Settings.api_keys[3]
keys_4 = Settings.api_keys[4]

# keys_1 = ["r435t2tr-252524-253452-25235", "rt35t2tr-25g524-25b452-2a235"]


db = PostgresDB(
    host=Settings.host,
    db_name=Settings.database,
    user=Settings.user,
    password=Settings.password
)

image = FileImage(Settings.static_path)

api_movie = WebRequesterKinopoiskMovie(list_api_key=keys_1, start_from_year=1965)
api_people = WebRequesterKinopoiskPeople(keys_2)
api_similar = WebRequesterKinopoiskSimilar(keys_3)
web_screenshot = WebRequesterMovieScreenshotIMDB()

# проверяем статус подключения к серверу
server_status, message = api_movie.check_resource_status()
print(message)

# start_id = 298
start_id = 324
end_id = 500

if server_status == 200:
    # получение данных с api
    for idd in range(start_id, end_id):
        print(f'\n\n----> kinopoisk id: {idd} <-----')

        # проверяем нет ли в базе фильма с kinopoisk_id = movie_id
        if not db.select_data(
                table_name='movies',
                select_keys='id, kinopoisk_id',
                where_key_name='kinopoisk_id',
                where_key_data=idd):

            # получаем фильм
            movie = api_movie.get_ready_api_data(kinopoisk_id=idd)
            if movie['status_code'] == 200 and movie['filter']:
                print(movie)

                # получаем все данные для фильма
                print('\n----------  Получение данных для фильма ----------\n')
                kinopoisk_id = int(movie['data']['kinopoiskId'])
                imdb_id = movie['data']['imdbId']
                year = movie['data'].get('year')

                # получаем актеров, режисеров, сценаристов
                people = api_people.get_ready_api_data(kinopoisk_id=kinopoisk_id)
                print(people)

                # получаем похожие фильмы
                similars = api_similar.get_ready_api_data(kinopoisk_id=kinopoisk_id)
                print(similars)

                # получаем кадры к фильму
                screenshots = web_screenshot.request_screenshot(imdb_id)
                print(screenshots)

                # сохраняем главное фото и возвращаем ссылку
                poster_save = image.web_save_image(
                    web_url_image=movie['data'].get('posterUrl'),
                    name='postr',
                    kinopoisk_id=kinopoisk_id,
                    year=year,
                )
                print(poster_save)

                # сохраняем кадры с фильма и возвращаем список ссылок
                screenshots_save = image.web_save_image(
                    web_url_image=screenshots['data'],
                    name='screenshots',
                    kinopoisk_id=kinopoisk_id,
                    year=year,
                )
                print(screenshots_save)

                # Screenshot add db
                screenshots = db.create_screen_movie(kinopoisk_id=kinopoisk_id, list_value=screenshots_save)
                print(screenshots)

                # Rating_kinopoisk add db
                rating_kinopoisk = db.get_or_create(
                    table_name='rating_kinopoisk',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=movie['data'].get('ratingKinopoisk', None),
                    insert_keys=('star', 'created_on'),
                    insert_values=(movie['data'].get('ratingKinopoisk', None), db.current_datetime())
                )
                print(rating_kinopoisk)

                # rating_imdb add db
                rating_imdb = db.get_or_create(
                    table_name='rating_imdb',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=movie['data'].get('ratingImdb', None),
                    insert_keys=('star', 'created_on'),
                    insert_values=(movie['data'].get('ratingImdb', None), db.current_datetime())
                )
                print(rating_imdb)

                # rating_imdb add db
                rating_critics = db.get_or_create(
                    table_name='rating_critics',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=movie['data'].get('ratingFilmCritics', None),
                    insert_keys=('star', 'created_on'),
                    insert_values=(movie['data'].get('ratingFilmCritics', None), db.current_datetime())
                )
                print(rating_critics)

                # Release add db
                release = db.get_or_create(
                    table_name='releases',
                    select_key='id, year',
                    where_key_name='year',
                    where_key_data=movie['data'].get('year', None),
                    insert_keys=('year', 'created_on'),
                    insert_values=(movie['data'].get('year', None), db.current_datetime())
                )
                print(release)

                # Film length add db
                film_length = db.get_or_create(
                    table_name='film_length',
                    select_key='id, length',
                    where_key_name='length',
                    where_key_data=movie['data'].get('filmLength', None),
                    insert_keys=('length', 'created_on'),
                    insert_values=(movie['data'].get('filmLength', None), db.current_datetime())
                )
                print(film_length)

                # Type video add db
                type_video = db.get_or_create(
                    table_name='type_videos',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=movie['data'].get('type', None),
                    insert_keys=('name', 'created_on'),
                    insert_values=(movie['data'].get('type', None), db.current_datetime())
                )
                print(type_video)

                # Age limit add db
                age_limit = db.get_or_create(
                    table_name='age_limits',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=db.get_digit_age_limit(movie['data'].get('ratingAgeLimits', None)),
                    insert_keys=('name', 'created_on'),
                    insert_values=(db.get_digit_age_limit(movie['data'].get('ratingAgeLimits', None)), db.current_datetime())
                )
                print(age_limit)

                # Генерируем url к новому фильму
                new_url = db.generate_url(
                    movie['data'].get('nameRu', None),
                    movie['data'].get('nameOriginal', None),
                    db.get_last_movie_id()
                )
                print(new_url)

                # Genre add db
                genres = db.get_or_create_from_list(
                    table_name='genres',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data_list=movie['data'].get('genres', None),
                    insert_keys=('name', 'created_on'),
                    dict_key_name='genre'
                )
                print(genres)

                # Country add db
                country = db.get_or_create_from_list(
                    table_name='countries',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data_list=movie['data'].get('countries', None),
                    insert_keys=('name', 'created_on'),
                    dict_key_name='country'
                )
                print(country)

                # Director add db
                director = db.get_or_create_from_list(
                    table_name='directors',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data_list=movie['data'].get('director', None),
                    insert_keys=('name', 'created_on'),
                    dict_key_name=''
                )
                print(director)

                # Creator add db
                creator = db.get_or_create_from_list(
                    table_name='creators',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data_list=movie['data'].get('writer', None),
                    insert_keys=('name', 'created_on'),
                    dict_key_name=''
                )
                print(creator)

                # Actor add db
                popular_actor = db.popular_actor(people['data'].get('actor'), count_actor_save=12)
                actor = db.get_or_create_from_list(
                    table_name='actors',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data_list=popular_actor,
                    insert_keys=('name', 'created_on'),
                    dict_key_name=''
                )
                print(actor)

                similar = db.get_or_create_similar(similars['data'])

                # получаем пользователя
                user = db.select_data(
                    table_name='users',
                    select_keys='id, username',
                    where_key_name='username',
                    where_key_data='Admin'
                )

                # создаем фильм
                new_movie = db.create_movie(
                    kinopoisk_id=kinopoisk_id,
                    imdb_id=imdb_id,
                    name_ru=movie['data'].get('nameRu'),
                    name_original=movie['data'].get('nameOriginal'),
                    poster_url=poster_save,
                    slug=new_url,
                    rating_kinopoisk_id=rating_kinopoisk,
                    rating_imdb_id=rating_imdb,
                    rating_critics_id=rating_critics,
                    year_id=release,
                    film_length_id=film_length,
                    slogan=movie['data'].get('slogan'),
                    description=movie['data'].get('description'),
                    short_description=movie['data'].get('shortDescription'),
                    type_video_id=type_video,
                    age_limits_id=age_limit,
                    last_syncs=db.converting_date_time(movie['data'].get('lastSync')),
                    user_id=user,
                    created_on=db.current_datetime()
                )

                #  сохраняем данные в связанные таблицы many-to-many
                db.related_table(table_name='genre_movie', movie_id=new_movie, list_data=genres)
                db.related_table(table_name='country_movie', movie_id=new_movie, list_data=country)
                db.related_table(table_name='director_movie', movie_id=new_movie, list_data=director)
                db.related_table(table_name='actor_movie', movie_id=new_movie, list_data=actor)
                db.related_table(table_name='creator_movie', movie_id=new_movie, list_data=creator)
                db.related_table(table_name='screenshot_movie', movie_id=new_movie, list_data=screenshots)
                db.related_table(table_name='similar_movie', movie_id=new_movie, list_data=similar)

        else:
            print('\n Фильм уже существует\n')
        print('\n--------- Finish ----------\n\n\n')
