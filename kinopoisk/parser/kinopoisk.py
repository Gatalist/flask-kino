import requests
from PIL import Image
import hashlib

from settings import Settings
from .base_parser import WebRequester


class WebRequesterKinopoisk(WebRequester):
    """Получаем по API данные сервера Kinopoisk"""

    def __init__(self, list_api_key):
        self.list_api_key = list_api_key
        self.iter_key = iter(self.list_api_key)
        self.current_key = None
        self.get_next_api_key()

    def get_next_api_key(self):
        """Получаем следующий api ключ из списка"""
        try:
            self.current_key = next(self.iter_key)
        except StopIteration:
            self.current_key = None

    def check_current_key(self):
        """Проверяем если закончились ключи то возвращаем 402 ошибку"""
        if self.current_key is None:
            print("[-] Больше нет API ключей\n")
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
        """Получаем по API kinopoisk"""
        print(f'\n----------- {message} ----------')
        print('api_key:', self.current_key, '\n')

        status = self.check_current_key()
        if status:
            return status

        request_data = self.request_data(parse_url, self.new_headers())

        if request_data["status_code"] == 402 or request_data["status_code"] == 401:
            if request_data["status_code"] == 401:
                print("[-] Не действительный API ключ\n")
            if request_data["status_code"] == 401:
                print("Превышен лимит запросов по ключу\n")
            self.get_next_api_key()

            status = self.check_current_key()
            if status:
                return status

            return self.request_data_from_api(parse_url, message)
        return request_data


class WebRequesterKinopoiskMovie(WebRequesterKinopoisk):
    """Получаем данные о фильм по API с сервера Kinopoisk"""

    def __init__(self, list_api_key, start_from_year):
        super().__init__(list_api_key)
        self.film_kinopoisk_api_url = f"{Settings.base_kinopoisk_api_url}/api/v2.2/films/"
        self.start_from_year = start_from_year
        self.placeholder_hashes = [
            'fbf36d5f304807e57113972f88ab9170f428fc57d27607bf1bd889b974513fde',
        ] # SHA256 хеш изображения-заглушки

    def is_placeholder_image(self, image_url) -> bool:
        # Проверка по хешу
        response = requests.get(image_url, timeout=10)
        if response.status_code == 200:
            image_hash = hashlib.sha256(response.content).hexdigest()
            print("poster_hash:", image_hash, "\n")
            if image_hash in self.placeholder_hashes:
                return True
        return False

    def request_data_api(self, kinopoisk_id: int) -> dict:
        """Получаем данные по API kinopoisk"""
        parse_url = f"{self.film_kinopoisk_api_url}{kinopoisk_id}"
        return self.request_data_from_api(parse_url, "Movie parsing")

    def checking_data(self, request_data) -> dict:
        """Проверяем наличие названия, постера и год выпуска.
         Год выпуска должен быть больше или равно 'from_year'.
         Если фильм соответствует всем параметрам, добавляем в ответ 'filter' """

        request_data['filter'] = False

        if request_data.get("data"):
            movie_data = request_data["data"].json()

            name = movie_data.get('nameRu', '')
            poster = movie_data.get('posterUrl', '')
            year = movie_data.get('year', 0)
            request_data['filter'] = True if year and year >= self.start_from_year else False

            print("nameRu |", "True  |" if name else "False |", name)
            print("year   |", f"True  | {year}" if request_data['filter'] else f"False | {year} < {self.start_from_year}")
            print("poster |", "True  |" if poster else "False |", poster)
            
            if name and poster and request_data["filter"]:
                if self.is_placeholder_image(poster):
                    request_data['filter'] = False
                    print("poster (plug)\n")
                    request_data["data"] = {}
                    return request_data

                request_data["data"] = request_data["data"].json()
                return request_data

        request_data["data"] = {}
        return request_data

    def get_ready_api_data(self, kinopoisk_id: int) -> dict:
        """Получаем готовые данные со статусами и фильтрами"""
        response = self.request_data_api(kinopoisk_id)
        dict_data = self.checking_data(response)
        return dict_data


class WebRequesterKinopoiskPeople(WebRequesterKinopoisk):
    """Получаем фильма по API Kinopoisk: режиссеров, актеров, сценаристов"""

    def __init__(self, list_api_key):
        super().__init__(list_api_key)
        self.film_kinopoisk_api_url = f"{Settings.base_kinopoisk_api_url}/api/v1/staff?filmId="

    def request_data_api(self, kinopoisk_id: int) -> dict:
        """Получаем данные по API kinopoisk"""
        parse_url = f"{self.film_kinopoisk_api_url}{kinopoisk_id}"
        return self.request_data_from_api(parse_url, "People parsing")

    @staticmethod
    def checking_data(request) -> dict:
        """Проверяем наличие данных"""
        director = []
        writer = []
        actor = []

        if request.get("data"):
            for elem in request["data"].json():
                if elem.get('professionKey') == 'DIRECTOR' and elem.get('nameRu') != '':
                    director.append(elem.get('nameRu'))

                if elem.get('professionKey') == 'ACTOR' and elem.get('nameRu') != '':
                    actor.append(elem.get('nameRu'))

                if elem.get('professionKey') == 'WRITER' and elem.get('nameRu') != '':
                    writer.append(elem.get('nameRu'))

            request["data"] = {'director': director, 'writer': writer, 'actor': actor}
            return request

        request["data"] = {}
        return request

    def get_ready_api_data(self, kinopoisk_id: int) -> dict:
        """Получаем готовые данные"""
        response = self.request_data_api(kinopoisk_id)
        dict_data = self.checking_data(response)
        return dict_data


class WebRequesterKinopoiskSimilar(WebRequesterKinopoisk):
    """Получаем похожие фильмы по API Kinopoisk"""

    def __init__(self, list_api_key):
        super().__init__(list_api_key)
        self.film_kinopoisk_api_url = f"{Settings.base_kinopoisk_api_url}/api/v2.2/films/"

    def request_data_api(self, kinopoisk_id: int) -> dict:
        """Получаем данные по API kinopoisk"""
        parse_url = f"{self.film_kinopoisk_api_url}{kinopoisk_id}/similars"
        return self.request_data_from_api(parse_url, "Similar parsing")

    @staticmethod
    def checking_data(request) -> dict:
        if request.get("data"):
            similar_data = request["data"].json()
            similar = {}

            for elem in similar_data.get('items', {}):
                film_id = elem.get('filmId')
                if film_id and film_id != '':
                    similar[film_id] = elem.get('nameRu')

            request["data"] = similar
            return request

        request["data"] = {}
        return request

    def get_ready_api_data(self, kinopoisk_id: int) -> dict:
        """Получаем готовые данные"""
        response = self.request_data_api(kinopoisk_id)
        dict_data = self.checking_data(response)
        return dict_data


class WebRequesterKinopoiskTopMovie(WebRequesterKinopoisk):
    """Получаем топ фильмов по API Kinopoisk"""

    def __init__(self, list_api_key):
        super().__init__(list_api_key)
        self.film_kinopoisk_api_url = f"{Settings.base_kinopoisk_api_url}/api/v2.2/films/collections?type="

    def request_top_movie(self, type_top, pages) -> dict:
        top_movie_id = []
        last_response = None

        for page in range(1, pages):
            parse_url = f"{self.film_kinopoisk_api_url}{type_top}&page={page}"
            top_movie_data = self.request_data_from_api(parse_url, "TOP MOVIES parsing")

            if top_movie_data.get("data"):
                data = top_movie_data.get("data").json()
                for film in data['items']:
                    top_movie_id.append(film['kinopoiskId'])

                last_response = top_movie_data

        last_response["data"] = top_movie_id
        return last_response
