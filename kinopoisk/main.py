from time import sleep

from parser.kinopoisk import KinopoiskApi
from parser.imdb import IMDBMovie
from tools.postgres_orm import PostgresDB
from tools.loguru_logger import logger
from tools.file_manager import FileImage
from settings import Settings


keys = Settings.api_keys[1] + Settings.api_keys[2] + Settings.api_keys[3] + Settings.api_keys[4]


db = PostgresDB(
    host=Settings.host,
    db_name=Settings.database,
    user=Settings.user,
    password=Settings.password
)

image = FileImage(Settings.static_path)

# path_save_file = image.generate_movie_path(path_names=['media', 'files'])
# save_kinopoist_ids = db.get_all_kinopoisk_ids(path_file=path_save_file, file_name='saved_ids.txt')
read_ids_from_file = image.get_list_line_file(file_path=['media', 'files', 'saved_ids.txt'])
# sleep(500)

api_kinopoisk = KinopoiskApi(list_api_key=keys)
imdb_movie = IMDBMovie()

# проверяем статус подключения к серверу
server_status, message = api_kinopoisk.check_resource_status(api_kinopoisk.base_api_url)
logger.info(message)

user_id = db.get_user(name='admin')
if user_id:
    user_id = user_id.get("id")
else:
    while True:
        logger.error("not user in db: create admin user")
        sleep(5)
        user_id = db.get_user(name='admin')
        if user_id:
            user_id = user_id.get("id")
            break

# min id = 298
# start_id = 84320
# end_id = 85_000

# sleep(1_000_000)

if server_status == 200:
    # получение данных с api
    # for idd in range(start_id, end_id):
    for _idd in read_ids_from_file:
        idd = int(_idd)
        logger.info(f'\n\n----> kinopoisk id: {idd} <-----')
        # проверяем нет ли в базе фильма с kinopoisk_id = movie_id
        if not db.get_id_by_name(table_name='movies', where_key_name='kinopoisk_id', where_key_data=idd):
            # получаем фильм
            movie = api_kinopoisk.get_data_movie(kinopoisk_id=idd, start_from_year=1965)
            if movie['status_code'] == 200 and movie['filter'] and movie['data']:
                # получаем все данные для фильма
                movie_data = movie['data']

                logger.info('\n----------  Получение данных для фильма ----------\n')
                logger.info(f"movie:data: {movie_data}")

                _kinopoisk_id = int(movie_data.get('kinopoiskId'))
                _kinopoisk_hd_id = movie_data.get('kinopoiskHDId')
                _imdb_id = movie_data.get('imdbId', None)
                _reviews_count = movie_data.get('reviewsCount', None)
                _rating_good_review = movie_data.get('ratingGoodReview', None)
                _rating_good_review_vote_count = movie_data.get('ratingGoodReviewVoteCount', None)
                _rating_kinopoisk_vote_count = movie_data.get('ratingKinopoiskVoteCount', None)
                _rating_imdb_vote_count = movie_data.get('ratingImdbVoteCount', None)
                _rating_critics = movie_data.get('ratingFilmCritics', None)
                _rating_critics_vote_count = movie_data.get('ratingFilmCriticsVoteCount', None)
                _rating_await = movie_data.get('ratingAwait', None)
                _rating_await_count = movie_data.get('ratingAwaitCount', None)
                _editor_annotation = movie_data.get('editorAnnotation', None)
                _is_tickets_available = movie_data.get('isTicketsAvailable', None)
                _production_status = movie_data.get('productionStatus', None)
                _rating_mpaa = movie_data.get('ratingMpaa', None)
                _year = movie_data.get('year', None)
                _start_year = movie_data.get('startYear', None)
                _end_year = movie_data.get('endYear', None)
                _serial = movie_data.get('serial', False)
                _completed = movie_data.get('completed', False)
                _poster = movie_data.get('posterUrl', None)
                _rating_kinopoisk = movie_data.get('ratingKinopoisk', None)
                _rating_imdb = movie_data.get('ratingImdb', None)
                _film_length = movie_data.get('filmLength', None)
                _type_video = movie_data.get('type', None)
                _genres = movie_data.get('genres', [])
                _countries = movie_data.get('countries', [])
                _name_ru = movie_data.get('nameRu', None)
                _name_en = movie_data.get('nameEn', None)
                _name_original = movie_data.get('nameOriginal', None)
                _slogan = movie_data.get('slogan', None)
                _description = movie_data.get('description', None)
                _short_description = movie_data.get('shortDescription')
                _age_limit = db.get_digit_age_limit(movie_data.get('ratingAgeLimits', None))
                _last_syncs = db.converting_date_time(movie_data.get('lastSync'))
                _has_3d = movie_data.get('has3D', False)
                _has_imax = movie_data.get('hasImax', False)
                _short_film = movie_data.get('shortFilm', False)

                # get actors, creators, writers
                people = api_kinopoisk.get_data_people(kinopoisk_id=_kinopoisk_id, count_actor_save=15)
                _directors = people.get('director', [])
                _writers = people.get('writer', [])
                _actors = people.get('actor', [])

                logger.info(f"director: {_directors}")
                logger.info(f"writer: {_writers}")
                logger.info(f"actor: {_actors}")

                # get similars movie
                _similars = api_kinopoisk.get_data_similar(kinopoisk_id=_kinopoisk_id)
                logger.info(f"similars: {_similars}")

                # get videos
                _videos = api_kinopoisk.get_data_video(kinopoisk_id=_kinopoisk_id)
                logger.info(f"videos: {_videos}")

                similars = _similars.get('data', None)
                similar_ids = db.get_or_create_similar(similars)

                # get movie screen
                screenshots = imdb_movie.get_movie_photos(_imdb_id)
                logger.info(f"screenshots: {screenshots}")

                # save head movie mage and return lint
                poster_url = image.web_save_image(
                    web_url_image=_poster,
                    name='postr',
                    path_names=['media', 'movie', str(_year), str(_kinopoisk_id)]
                )
                logger.info(f"poster_url: {poster_url}")

                # save screen movie and return link list
                screenshots_save = image.web_save_image(
                    web_url_image=screenshots['data'],
                    name='image',
                    path_names=['media', 'movie', str(_year), str(_kinopoisk_id)]
                )

                videos = db.create_video(list_video=_videos)
                print("created videos:", videos)
                videos_ids = db.get_obj_ids(videos)

                screenshots = db.create_screen_movie(kinopoisk_id=_kinopoisk_id, list_value=screenshots_save)

                rating_kinopoisk_id = db.get_or_create(
                    table_name='rating_kinopoisk',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=_rating_kinopoisk,
                    insert_keys=('publish', 'sorting', 'star', 'created_on'),
                    insert_values=(True, 100, _rating_kinopoisk, db.get_current_datetime())
                )
                if rating_kinopoisk_id:
                    rating_kinopoisk_id = rating_kinopoisk_id.get('id')

                rating_imdb_id = db.get_or_create(
                    table_name='rating_imdb',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=_rating_imdb,
                    insert_keys=('publish', 'sorting', 'star', 'created_on'),
                    insert_values=(True, 100, _rating_imdb, db.get_current_datetime())
                )
                if rating_imdb_id:
                    rating_imdb_id = rating_imdb_id.get('id')

                rating_critics_id = db.get_or_create(
                    table_name='rating_critics',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=_rating_critics,
                    insert_keys=('publish', 'sorting', 'star', 'created_on'),
                    insert_values=(True, 100, _rating_critics, db.get_current_datetime())
                )
                if rating_critics_id:
                    rating_critics_id = rating_critics_id.get('id')

                year_id = db.get_or_create(
                    table_name='releases',
                    select_key='id, year',
                    where_key_name='year',
                    where_key_data=_year,
                    insert_keys=('publish', 'sorting', 'year', 'created_on'),
                    insert_values=(True, 100, _year, db.get_current_datetime())
                )
                if year_id:
                    year_id = year_id.get('id')

                start_year_id = db.get_or_create(
                    table_name='releases',
                    select_key='id, year',
                    where_key_name='year',
                    where_key_data=_start_year,
                    insert_keys=('publish', 'sorting', 'year', 'created_on'),
                    insert_values=(True, 100, _start_year, db.get_current_datetime())
                )
                if start_year_id:
                    start_year_id = start_year_id.get('id')

                end_year_id = db.get_or_create(
                    table_name='releases',
                    select_key='id, year',
                    where_key_name='year',
                    where_key_data=_end_year,
                    insert_keys=('publish', 'sorting', 'year', 'created_on'),
                    insert_values=(True, 100, _end_year, db.get_current_datetime())
                )
                if end_year_id:
                    end_year_id = end_year_id.get('id')

                film_length_id = db.get_or_create(
                    table_name='film_length',
                    select_key='id, length',
                    where_key_name='length',
                    where_key_data=_film_length,
                    insert_keys=('publish', 'sorting', 'length', 'created_on'),
                    insert_values=(True, 100, _film_length, db.get_current_datetime())
                )
                if film_length_id:
                    film_length_id = film_length_id.get('id')

                type_video_id = db.get_or_create(
                    table_name='type_videos',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=_type_video,
                    insert_keys=('publish', 'sorting', 'name', 'created_on'),
                    insert_values=(True, 100, _type_video, db.get_current_datetime())
                )
                if type_video_id:
                    type_video_id = type_video_id.get('id')

                age_limit_id = db.get_or_create(
                    table_name='age_limits',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=_age_limit,
                    insert_keys=('publish', 'sorting', 'name', 'created_on'),
                    insert_values=(True, 100, _age_limit, db.get_current_datetime())
                )
                if age_limit_id:
                    age_limit_id = age_limit_id.get('id')

                genres = db.get_or_create_from_list(
                    table_name='genres',
                    select_key='id, name',
                    where_key_name='name',
                    key_names=('publish', 'sorting', 'name', 'created_on'),
                    values_data=(True, 100, _genres, db.get_current_datetime),
                )
                genres_ids = db.get_obj_ids(genres)

                country = db.get_or_create_from_list(
                    table_name='countries',
                    select_key='id, name',
                    where_key_name='name',
                    key_names=('publish', 'sorting', 'name', 'created_on'),
                    values_data=(True, 100, _countries, db.get_current_datetime),
                )
                country_ids = db.get_obj_ids(country)

                director_ids = db.create_person(list_obj=_directors, instance=image, path_names=['media', 'people', str(_year), str(_kinopoisk_id)])
                print("director_ids:", director_ids)

                creator_ids = db.create_person(list_obj=_writers, instance=image, path_names=['media', 'people', str(_year), str(_kinopoisk_id)])
                print("creator_ids:", creator_ids)

                # Popular actor add db
                # popular_actor = db.popular_actor(_actors, count_actor_save=20)
                actor_ids = db.create_person(list_obj=_actors, instance=image, path_names=['media', 'people', str(_year), str(_kinopoisk_id)])
                print("actor_ids:", actor_ids)

                production_status_id = db.get_or_create(
                    table_name='production_status',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=_production_status,
                    insert_keys=('publish', 'sorting', 'name', 'created_on'),
                    insert_values=(True, 100, _production_status, db.get_current_datetime())
                )
                if production_status_id:
                    production_status_id = production_status_id.get('id')

                rating_mpaa_id = db.get_or_create(
                    table_name='rating_mpaa',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=_rating_mpaa,
                    insert_keys=('publish', 'sorting', 'star', 'created_on'),
                    insert_values=(True, 100, _rating_mpaa, db.get_current_datetime())
                )
                if rating_mpaa_id:
                    rating_mpaa_id = rating_mpaa_id.get('id')

                rating_await_id = db.get_or_create(
                    table_name='rating_await',
                    select_key='id, star',
                    where_key_name='star',
                    where_key_data=_rating_await,
                    insert_keys=('publish', 'sorting', 'star', 'created_on'),
                    insert_values=(True, 100, _rating_await, db.get_current_datetime())
                )
                if rating_await_id:
                    rating_await_id = rating_await_id.get('id')

                new_url = db.generate_url_by_first_name(
                    names=[_name_ru, _name_en, _name_original],
                    movie_id=db.get_last_id(table_name='movies')
                )

                new_movie = db.create_movie(
                    kinopoisk_id = _kinopoisk_id,
                    kinopoisk_hd_id=_kinopoisk_hd_id,
                    imdb_id=_imdb_id,
                    editor_annotation=_editor_annotation,
                    is_tickets_available=_is_tickets_available,
                    production_status_id=production_status_id,
                    name_ru=_name_ru,
                    name_en=_name_en,
                    name_uk=None,
                    name_original=_name_original,
                    poster_url=poster_url,
                    slug=new_url,
                    reviews_count=_reviews_count,
                    rating_mpaa_id=rating_mpaa_id,
                    rating_good_review=_rating_good_review,
                    rating_good_review_vote_count=_rating_good_review_vote_count,

                    trailer_id=None, # comming soon

                    rating_kinopoisk_id = rating_kinopoisk_id,
                    rating_kinopoisk_vote_count=_rating_kinopoisk_vote_count,
                    rating_imdb_id = rating_imdb_id,
                    rating_imdb_vote_count=_rating_imdb_vote_count,
                    rating_critics_id=rating_critics_id,
                    rating_critics_vote_count=_rating_critics_vote_count,
                    year_id=year_id,
                    start_year_id=start_year_id,
                    end_year_id=end_year_id,
                    film_length_id=film_length_id,
                    slogan=_slogan,
                    description=_description,
                    short_description=_short_description,
                    type_video_id=type_video_id,
                    age_limits_id=age_limit_id,
                    last_syncs=_last_syncs,
                    has_3d=_has_3d,
                    has_imax=_has_imax,
                    short_film=_short_film,
                    user_id=user_id,
                    created_on=db.get_current_datetime(),
                    serial=_serial,
                    completed=_completed,
                    publish=True,
                    rating_await_id = rating_await_id,
                    rating_await_count = _rating_await_count,
                    sorting = 100
                )

                # many-to-many
                db.related_table(table_name='country_movie', movie_id=new_movie, list_data=country_ids)
                db.related_table(table_name='genre_movie', movie_id=new_movie, list_data=genres_ids)
                db.related_table(table_name='director_movie', movie_id=new_movie, list_data=director_ids)
                db.related_table(table_name='creator_movie', movie_id=new_movie, list_data=creator_ids)
                db.related_table(table_name='actor_movie', movie_id=new_movie, list_data=actor_ids)
                db.related_table(table_name='screenshot_movie', movie_id=new_movie, list_data=screenshots)
                db.related_table(table_name='similar_movie', movie_id=new_movie, list_data=similar_ids)
                db.related_table(table_name='video_movie', movie_id=new_movie, list_data=videos_ids)

            elif movie['status_code'] == 402:
                break
        else:
            logger.info('\n Фильм уже существует\n')
        logger.info('\n--------- Finish ----------\n\n\n')
