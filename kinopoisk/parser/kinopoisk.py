import requests
import hashlib

from settings import Settings
from .base_parser import WebRequester
from tools.loguru_logger import logger
from tools.file_manager import read_line_file


class KinopoiskApi(WebRequester):
    """Получаем по API данные сервера Kinopoisk"""

    def __init__(self, list_api_key):
        self.base_api_url = "https://kinopoiskapiunofficial.tech"
        self.film_api_url = f"{self.base_api_url}/api/v2.2/films/"
        self.staff_api_url = f"{self.base_api_url}/api/v1/staff?filmId="
        self.similar_api_url = f"{self.base_api_url}/api/v2.2/films/"
        self.video_api_url = f"{self.base_api_url}/api/v2.2/films/"
        self.top_movie_api_url = f"{self.base_api_url}/api/v2.2/films/collections?type="
        self.list_api_key = list_api_key
        self.iter_key = iter(self.list_api_key)
        self.current_key = None
        self.get_next_api_key()
        self.placeholder_hashes = Settings.placeholder_hashes

    def get_next_api_key(self):
        """Получаем следующий api ключ из списка"""
        try:
            self.current_key = next(self.iter_key)
        except StopIteration:
            self.current_key = None

    def check_current_key(self):
        """Проверяем если закончились ключи то возвращаем 402 ошибку"""
        if self.current_key is None:
            logger.info("[-] Больше нет API ключей\n")
            response = self.new_base_response_dict()
            response["status_code"] = 402
            response["status"] = False
            response["status_message"] = Settings.status_codes.get(402, "Error not info")
            response["data"] = None
            return response

    def new_headers(self):
        """Генерируем новый заголовок при запросе"""
        header = self.get_user_agent()
        header["Content-Type"] = "application/json"
        header["X-API-KEY"] = self.current_key
        return header

    def request_data_from_api(self, parse_url, message) -> dict:
        logger.info(f'----------- {message} ----------\napi_key: {self.current_key}\n')

        status = self.check_current_key()
        if status:
            return status

        request_data = self.request_data(parse_url, self.new_headers())

        if request_data["status_code"] == 402 or request_data["status_code"] == 401:
            if request_data["status_code"] == 401:
                logger.info("[-] Не действительный API ключ\n")
            if request_data["status_code"] == 401:
                logger.info("Превышен лимит запросов по ключу\n")
            self.get_next_api_key()

            status = self.check_current_key()
            if status:
                return status

            return self.request_data_from_api(parse_url, message)
        return request_data

    def is_placeholder_image(self, image_url) -> bool:
        """Проверка изображение по хешу, если это заглушка то возвращаем True"""
        response = self.request_data(image_url, self.new_headers())
        logger.info(f"image_data: {response.get('data')}\n")
        if response.get('status_code') == 200:
            image_hash = hashlib.sha256(response.get('data').content).hexdigest()
            logger.info(f"image_hash: {image_hash}\n")
            if image_hash in self.placeholder_hashes:
                return True
        return False

    @staticmethod
    def sorting_actors(list_actors: list[dict], count_actor_save) -> list:
        popular_actors = read_line_file('./actor/actors.txt')

        if list_actors:
            popular = []
            other = []
            for actor in list_actors:
                if actor.get('nameRu') in popular_actors:
                    popular.append(actor)
                else:
                    other.append(actor)
            popular = popular + other
            len_list = len(popular)
            if len_list > count_actor_save:
                return popular[:count_actor_save]
            return popular
        return list_actors

    def get_data_movie(self, kinopoisk_id: int, start_from_year: int) -> dict:
        """
        Получаем данные о фильме, фильтруем по названию, изображению и год выпуска.
        Год выпуска должен быть больше или равно 'start_from_year'.
        """

        parse_url = f"{self.film_api_url}{kinopoisk_id}"
        request_data = self.request_data_from_api(parse_url, "Movie parsing")
        request_data["filter"] = False

        if request_data.get("data"):
            movie_data = request_data.get("data").json()
            print("movie_data: ", movie_data)
            name_ru = movie_data.get('nameRu', None)
            name_orig = movie_data.get('nameOriginal', None)
            poster = movie_data.get('posterUrl', None)
            year = movie_data.get('year') if movie_data.get('year') and type(movie_data.get('year')) == int else 0

            request_data['filter'] = True if year >= start_from_year else False

            logger.info(f'nameRu       | {"True  |" if name_ru else "False |"} {name_ru}')
            logger.info(f'nameOriginal | {"True  |" if name_orig else "False |"} {name_orig}')
            logger.info(f'year         | {"True  |" if request_data["filter"] else "False |"} {year}')
            logger.info(f'poster       | {"True  |" if poster else "False |"} {poster}')

            if name_ru and poster and request_data["filter"] and (name_ru or name_orig):
                if self.is_placeholder_image(poster):
                    request_data['filter'] = False
                    logger.info("poster (plug)\n")
                    request_data["data"] = {}
                    return request_data

                request_data["data"] = movie_data
                return request_data

        request_data["data"] = {}
        return request_data

    def get_data_people(self, kinopoisk_id: int, count_actor_save) -> dict:
        """Получаем режиссеров, актеров, сценаристов"""
        parse_url = f"{self.staff_api_url}{kinopoisk_id}"
        request_data = self.request_data_from_api(parse_url, "People parsing")

        director = []
        creator = []
        actor = []

        res_data = request_data.get("data")
        if res_data:
            for elem in res_data.json():
                _person = {
                    "person_id": elem.get('staffId', None),
                    "name_ru": elem.get('nameRu', None),
                    "name_en": elem.get('nameEn', None),
                    "description": elem.get('description', None),
                    "image_url": elem.get('posterUrl', None),
                }
                if elem.get('nameRu') != '' or elem.get('nameEn') != '':
                    if elem.get('professionKey') == 'DIRECTOR':
                        _person['director'] = True
                        director.append(_person)

                    if elem.get('professionKey') == 'ACTOR':
                        _person['actor'] = True
                        actor.append(_person)

                    if elem.get('professionKey') == 'WRITER':
                        _person['creator'] = True
                        creator.append(_person)

            slice_actor = self.sorting_actors(list_actors=actor, count_actor_save=count_actor_save)
            request_data["data"] = {'director': director, 'creator': creator, 'actor': slice_actor}
        return request_data

    def get_data_similar(self, kinopoisk_id: int) -> dict:
        """Получаем похожие фильмы"""
        parse_url = f"{self.similar_api_url}{kinopoisk_id}/similars"
        response = self.request_data_from_api(parse_url, "Similar parsing")

        if response.get("data"):
            similar_data = response["data"].json()
            similar = {}

            for elem in similar_data.get('items', {}):
                film_id = elem.get('filmId')
                if film_id and film_id != '':
                    similar[film_id] = elem.get('nameRu')

            response["data"] = similar

        return response

    def get_data_video(self, kinopoisk_id) -> list:
        """Получаем трейлеры, тизеры, видео для фильма"""
        parse_url = f"{self.video_api_url}{kinopoisk_id}/videos"
        video_movie_data = self.request_data_from_api(parse_url, "VIDEO MOVIES parsing")

        scip_source = ["KINOPOISK_WIDGET", "UNKNOWN", "YANDEX_DISK"]
        videos = []
        if video_movie_data.get("data"):
            data = video_movie_data.get("data").json()
            for elem in data['items']:
                site = elem.get('site')
                if site in scip_source:
                    continue
                videos.append(elem)

        return videos

    def get_data_top_movie(self, type_top, pages) -> dict:
        """Получаем топ фильмов"""

        top_movie_id = []
        last_response = None

        for page in range(1, pages):
            parse_url = f"{self.top_movie_api_url}{type_top}&page={page}"
            top_movie_data = self.request_data_from_api(parse_url, "TOP MOVIES parsing")

            if top_movie_data.get("data"):
                data = top_movie_data.get("data").json()
                for film in data['items']:
                    top_movie_id.append(film['kinopoiskId'])

                last_response = top_movie_data

        last_response["data"] = top_movie_id
        return last_response
