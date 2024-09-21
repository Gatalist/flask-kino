from .parser import WebRequester


class WebRequesterKinopoisk(WebRequester):
    """Получаем по API данные сервера Kinopoisk"""

    def __init__(self, list_api_key, start_from_year = 1965):
        self.base_kinopoisk_api_url = "https://kinopoiskapiunofficial.tech"
        self.film_kinopoisk_api_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/"
        self.people_kinopoisk_api_url = f"{self.base_kinopoisk_api_url}/api/v1/staff?filmId="
        self.similar_kinopoisk_api_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/"
        self.top_movie_kinopoisk_api_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/collections?type="
        self.start_from_year = start_from_year
        self.list_api_key = list_api_key
        self.iter_key = iter(self.list_api_key)
        self.current_key = None
        self.get_next_api_key()

    def get_next_api_key(self) -> str:
        """Получаем следующий api ключ из списка"""
        try:
            self.current_key = next(self.iter_key)
        except StopIteration:
            self.current_key = None

    def is_not_current_key(self) -> bool:
        """Проверяем если закончились ключи то возвращаем 402 ошибку"""
        if not self.current_key:
            # print("[-] Больше нет API ключей\n")
            response = {}
            response["status_code"] = 402
            response["error"] = "API key not found"
            return response

    def collect_new_headers(self) -> dict:
        """Генерируем новый заголовок при запросе"""
        header = self.get_user_agent()
        header["Content-Type"] = "application/json"
        header["X-API-KEY"] = self.current_key
        return header

    def dict_to_list(self, data: list):
        new_list = []
        for item in data:
            new_list.append(next(iter(item.values())))
        return new_list
    
    @staticmethod
    def get_digit_age_limit(text) -> str:
        if isinstance(text, str):
            val = "".join(c for c in text if c.isdecimal())
            return val

    def request_data_from_api(self, parse_url: str, response_type: str, message: str) -> dict:
        """Получаем по API kinopoisk"""
        print(f'\n----------- {message} ----------')
        print('api_key:', self.current_key, '\n')

        if result:= self.is_not_current_key():
            return result

        response = self.request_data(url=parse_url, headers=self.collect_new_headers(), response_type=response_type)
        print(f"{response=}")
        if response.get("status_code") in (401, 402):
            print("[-] Не действительный API ключ или превышен лимит запросов\n")
            self.get_next_api_key()

            if result:= self.is_not_current_key():
                return result
            
            return self.request_data_from_api(parse_url=parse_url, response_type=response_type, message=message)
        return response

    def response_movie(self, kinopoisk_id: int, response_type: str) -> dict:
        parse_url = f"{self.film_kinopoisk_api_url}{kinopoisk_id}"
        response = self.request_data_from_api(parse_url=parse_url, response_type="json", message="Movie parsing")

        if movie_data:= response.get("result"):
            response["result"]["genres"] = self.dict_to_list(response.get("result").get("genres", []))
            response["result"]["countries"] = self.dict_to_list(response.get("result").get("countries", []))
            response["result"]["ratingAgeLimits"] = self.get_digit_age_limit(response.get("result").get("ratingAgeLimits"))

            name = movie_data.get('nameRu', '')
            poster = movie_data.get('posterUrl', '')
            year = movie_data.get('year', 0)

            is_name = True if name else False
            is_poster = True if poster else False
            is_year = True if year > self.start_from_year else False
            
            print(f"\nnameRu | {is_name}   | {name}")
            print(f"poster | {is_poster}   | {poster}")
            print(f"year   | {is_year}   | {year}\n")

            if is_name and is_poster and is_year:
                return response
        return {}

    def response_people(self, kinopoisk_id: int, response_type: str) -> dict:
        parse_url = f"{self.people_kinopoisk_api_url}{kinopoisk_id}"
        response = self.request_data_from_api(parse_url=parse_url, response_type="json", message="People parsing")

        result = {
            'director': [], 
            'writer': [], 
            'actor': []
        }

        if people_data:= response.get("result"):            
            for elem in people_data:
                if elem.get('professionKey') == 'DIRECTOR' and elem.get('nameRu') != '':
                    result["director"].append(elem.get('nameRu'))

                if elem.get('professionKey') == 'ACTOR' and elem.get('nameRu') != '':
                    result["actor"].append(elem.get('nameRu'))

                if elem.get('professionKey') == 'WRITER' and elem.get('nameRu') != '':
                    result["writer"].append(elem.get('nameRu'))

        response["result"] = result
        return response
    
    def response_similar(self, kinopoisk_id: int, response_type: str) -> dict:
        parse_url = f"{self.similar_kinopoisk_api_url}{kinopoisk_id}/similars"
        response = self.request_data_from_api(parse_url=parse_url, response_type="json", message="Similar parsing")
        similar = {}

        if similar_data:= response.get("result"): 
            for elem in similar_data.get('items', {}):
                film_id = elem.get('filmId')
                if film_id and film_id != '':
                    similar[film_id] = elem.get('nameRu')

        response["result"] = similar
        return response

    def response_top_movie(self, type_top: int, pages: int, response_type: str) -> dict:
        top_movie_id = []

        for page in range(1, pages):
            parse_url = f"{self.top_movie_kinopoisk_api_url}{type_top}&page={page}"
            response = self.request_data_from_api(parse_url=parse_url, response_type="json", message="TOP MOVIES parsing")

            if top_movie:= response.get("result"):
                for film in top_movie:
                    top_movie_id.append(film['kinopoiskId'])

        response["result"] = top_movie_id
        return response
