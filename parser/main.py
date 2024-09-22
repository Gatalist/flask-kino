from settings import Settings
from libs.kinopoisk import WebRequesterKinopoisk
from libs.imdb import WebRequesterIMDB
from libs.file_image import FileImage
from libs.database import Database
from libs.utils import current_datetime, generate_url, converting_date_time


keys_1 = Settings.api_keys[1]
keys_2 = Settings.api_keys[2]
keys_3 = Settings.api_keys[3]
keys_4 = Settings.api_keys[4]

db = Database(
    host=Settings.host,
    db_name=Settings.database,
    user=Settings.user,
    password=Settings.password
)

image = FileImage(Settings.static_path)

# проверяем статус подключения к серверу
api = WebRequesterKinopoisk(keys_2)
imdb = WebRequesterIMDB()

server_status = api.is_resource_availability(url=api.base_kinopoisk_api_url)
print(server_status)

start_id = 53_104
end_id = 100_000


# add new user
# user = db.add_row(
#     table_name='users', 
#     attrs={
#         "active": True,
#         "username": "Admin",
#         "email": "test@gmail.com",
#         "password": "32rf23fw2wf",
#         "created_on": current_datetime()
#         }
# )



if server_status:
    # получение данных с api
    for idd in range(start_id, end_id):
        print(f'\n\n----> kinopoisk id: {idd} <-----')

        # проверяем нет ли в базе фильма с kinopoisk_id = movie_id
        if not db.get_row(table_name='movies', attrs={'kinopoisk_id': idd}):
            # получаем фильм
            movie = api.response_movie(kinopoisk_id=idd, response_type="json")
            print(movie)

            if not api.current_key:
                break

            if not movie.get('result'):
                continue

            # получаем все данные для фильма
            # print('\n----------  Получение данных для фильма ----------\n')
            kinopoisk_id = int(movie['result']['kinopoiskId'])
            imdb_id = movie['result']['imdbId']
            year = movie['result'].get('year')

            # получаем актеров, режисеров, сценаристов
            people = api.response_people(kinopoisk_id=kinopoisk_id, response_type="json")
            print(people)

            # получаем похожие фильмы
            similars = api.response_similar(kinopoisk_id=kinopoisk_id, response_type="json")
            print(similars)


            # # сохраняем главное фото и возвращаем ссылку
            poster_save = image.web_save_image(
                web_url_image=movie['result'].get('posterUrl'),
                name='postr',
                kinopoisk_id=kinopoisk_id,
                year=year,
            )
            print(f"{poster_save=}")

            # получаем кадры к фильму
            movie_screenshots = imdb.request_screenshot(imdb_id)
            print(f"{movie_screenshots=}")

            # сохраняем кадры с фильма и возвращаем список ссылок
            screenshots_save = image.web_save_image(
                web_url_image=movie_screenshots['result'],
                name='screenshots',
                kinopoisk_id=kinopoisk_id,
                year=year,
            )
            print(screenshots_save)

            # Screenshot add db
            screenshots = db.create_screen_movie(table_name='screenshots', data=screenshots_save, attrs={"kinopoisk_id": kinopoisk_id})
            print(screenshots)

            rating_kinopoisk = db.get_or_create(table_name='rating_kinopoisk', attrs={"star": movie['result'].get('ratingKinopoisk'), "created_on": current_datetime()})
            print(f"{rating_kinopoisk=}")
            
            rating_imdb = db.get_or_create(table_name='rating_imdb', attrs={"star": movie['result'].get('ratingImdb'), "created_on": current_datetime()})
            print(f"{rating_imdb=}")

            rating_critics = db.get_or_create(table_name='rating_critics', attrs={"star": movie['result'].get('ratingFilmCritics'), "created_on": current_datetime()})
            print(f"{rating_critics=}")

            release = db.get_or_create(table_name='releases', attrs={"year": movie['result'].get('year'), "created_on": current_datetime()})
            print(f"{release=}")

            film_length = db.get_or_create(table_name='film_length', attrs={"length": movie['result'].get('filmLength'), "created_on": current_datetime()})
            print(f"{film_length=}")

            type_video = db.get_or_create(table_name='type_videos', attrs={"name": movie['result'].get('type'), "created_on": current_datetime()})
            print(f"{type_video=}")

            age_limit = db.get_or_create(table_name='age_limits', attrs={"name": movie['result'].get('ratingAgeLimits'), "created_on": current_datetime()})
            print(f"{age_limit=}")

            genres = db.get_or_create_list(table_name='genres', data=movie['result'].get('genres'), attrs={"name": "", "created_on": ""})
            print(f"{genres=}")

            country = db.get_or_create_list(table_name='countries', data=movie['result'].get('countries'), attrs={"name": "", "created_on": ""})
            print(f"{country=}")

            director = db.get_or_create_list(table_name='directors', data=people['result'].get('director'), attrs={"name": "", "created_on": ""})
            print(f"{director=}")

            creator = db.get_or_create_list(table_name='creators', data=people['result'].get('writer'), attrs={"name": "", "created_on": ""})
            print(f"{creator=}")

            actor = db.get_or_create_list(table_name='actors', data=people['result'].get('actor'), attrs={"name": "", "created_on": ""})
            print(f"{actor=}")
            filter_popular_actor = db.get_popular_actor(list_actor=actor, count_actor_save=12)
            print(f"{filter_popular_actor=}")

            similar = db.get_or_create_similar(table_name='similars', data=similars['result'], attrs={"kinopoisk_id": "", "name": "", "created_on": ""})
            print(f"{similar=}")

            popular_actor = db.get_popular_actor(people['result'].get('actor'), count_actor_save=12)
            print(f"{popular_actor=}")

            # Генерируем url к новому фильму
            new_url = generate_url(
                movie['result'].get('nameRu'),
                movie['result'].get('nameOriginal'),
                db.get_last_id(table_name='movies')
            )
            print(f"{new_url=}")

            user_id = db.get_row(table_name='users', attrs={"username": "Admin"})
            print(f"{user_id=}")

            # создаем фильм
            movie_json = {
                "kinopoisk_id": kinopoisk_id,
                "imdb_id": imdb_id,
                "name_ru": movie['result'].get('nameRu'),
                "name_original": movie['result'].get('nameOriginal'),
                "poster_url": poster_save,
                "slug": new_url,
                "rating_kinopoisk_id": rating_kinopoisk,
                "rating_imdb_id": rating_imdb,
                "rating_critics_id": rating_critics,
                "year_id": release,
                "film_length_id": film_length,
                "slogan": movie['result'].get('slogan'),
                "description": movie['result'].get('description'),
                "short_description": movie['result'].get('shortDescription'),
                "type_video_id": type_video,
                "age_limits_id": age_limit,
                "last_syncs": converting_date_time(movie['result'].get('lastSync')),
                "user_id": user_id,
                "created_on": current_datetime()
            }

            new_movie_id = db.add_row(table_name="movies", attrs=movie_json)
            print(f"{new_movie_id=}")

            #  сохраняем данные в связанные таблицы many-to-many

            db.related_table(
                relate_table="genre_movie", second_table="genres",
                movie_id=new_movie_id, list_data=genres,
                col_second="genre_id", fk_second="genres.id"
                )

            db.related_table(
                relate_table="country_movie", second_table="countries",
                movie_id=new_movie_id, list_data=country,
                col_second="country_id", fk_second="countries.id"
                )

            db.related_table(
                relate_table="director_movie", second_table="directors",
                movie_id=new_movie_id, list_data=director,
                col_second="director_id", fk_second="directors.id"
                )

            db.related_table(
                relate_table="actor_movie", second_table="actors",
                movie_id=new_movie_id, list_data=filter_popular_actor,
                col_second="actor_id", fk_second="actors.id"
                )
            
            db.related_table(
                relate_table="creator_movie", second_table="creators",
                movie_id=new_movie_id, list_data=creator,
                col_second="creator_id", fk_second="creators.id"
                )

            db.related_table(
                relate_table="screenshot_movie", second_table="screenshots",
                movie_id=new_movie_id, list_data=screenshots,
                col_second="screenshot_id", fk_second="screenshots.id"
                )

            db.related_table(
                relate_table="similar_movie", second_table="similars",
                movie_id=new_movie_id, list_data=similar,
                col_second="similar_id", fk_second="similars.id"
                )

        else:
            print('\n Фильм уже существует\n')
        print('\n--------- Finish ----------\n\n\n')
