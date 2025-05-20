import random
import requests
from settings import Settings


class WebRequester:
    """Базовый клас получения данных с сервера"""
    timeout = 7  # мах время ожидания ответа сервера

    @staticmethod
    def new_base_response_dict():
        """Создаем новый словарь с которого будем формировать ответ сервера"""
        base_response = {
            "status_code": 0,
            "status": False,
            "status_message": '',
            "data": None,
        }
        return base_response

    @staticmethod
    def get_user_agent() -> dict:
        """Получение рандомный User-Agent"""
        user = random.choice(Settings.user_agents)
        return {'User-Agent': user}

    def check_request_status(self, code):
        """Формируем новый словарь статус с полученными данными"""
        print("status_code =", code, '\n')
        response = self.new_base_response_dict()

        if code == 200:
            response["status"] = True

        response["status_code"] = code
        response["status_message"] = Settings.status_codes.get(code, "Error not info")
        return response

    def check_resource_status(self):
        """Проверка доступа к ресурсу kinopoisk api"""
        try:
            requests.head(Settings.base_kinopoisk_api_url, timeout=self.timeout)
            return 200, "[+] The server is ready to connect [ 200 ]"
        except requests.ConnectionError:
            return 400, "[-] Connection error to server [ 400 ]\nUse the VPN..."
        except requests.Timeout:
            return 400, "[-] Timeout connect to server [ 400 ]\nUse the VPN..."

    def request_data(self, url: str, headers: dict):
        """Получаем данные с ответа сервера"""
        try:
            request_data = requests.get(url, headers=headers, timeout=self.timeout)
            if hasattr(request_data, 'status_code'):
                new_request = self.check_request_status(request_data.status_code)
                if new_request["status_code"] == 200:
                    new_request["data"] = request_data

                return new_request

            else:
                code = 400
                new_request = self.check_request_status(code)
                return new_request

        except requests.ConnectionError:
            raise '[-] Ошибка подключения...'

        except requests.Timeout:
            raise '[-] Время ожидания истекло, нет доступа к ресурсу...'
