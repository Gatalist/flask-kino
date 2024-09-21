import random
import requests
from fake_useragent import UserAgent
from typing import Union


class WebRequester:
    """Базовый клас получения данных с сервера"""
    timeout = 5  # мах время ожидания ответа сервера
    random_user_agent = UserAgent()

    status_codes = {
        # status 2хх
        200: "OK: Запрос успешно выполнен",

        # status 4хх
        400: "Bad Request («неправильный, некорректный запрос»)",
        401: "Unauthorized («не авторизован (не представился)»)",
        402: "Payment Required («превышен лимит запросов»)",
        403: "Forbidden («запрещено (не уполномочен)»)",
        404: "Not Found («не найдено»)",
        408: "Request Timeout («истекло время ожидания»)",
        423: "Locked («заблокировано»);",
        429: "Too Many Requests («слишком много запросов»)",
        499: "Client Closed Request (клиент закрыл соединение)",

        # status 5хх
        500: "Internal Server Error («внутренняя ошибка сервера»)",
        502: "Bad Gateway («плохой, ошибочный шлюз»)",
        503: "Service Unavailable («сервис недоступен»)",
        504: "Gateway Timeout («шлюз не отвечает»)",
        520: "Unknown Error («неизвестная ошибка»)",
        521: "Web Server Is Down («веб-сервер не работает»)",
        522: "Connection Timed Out («соединение не отвечает»)",
        523: "Origin Is Unreachable («источник недоступен»)",
        524: "A Timeout Occurred («время ожидания истекло»)",
    }

    def get_user_agent(self) -> dict:
        """Получение рандомный User-Agent"""
        return {'User-Agent': self.random_user_agent.random}

    def is_resource_availability(self, url: str):
        """checking resource availability"""
        try:
            requests.head(url, timeout=self.timeout)
            print("[+] The server is ready to connect [ 200 ]")
            return True
        except requests.ConnectionError:
            print("[-] Connection error to server [ 400 ]\nResource not available or try use the VPN")
            return False
        except requests.Timeout:
            print("[-] Timeout connect to server [ 400 ]\nResource not available or try use the VPN")
            return False

    def check_response(func):
        def wrapper(self, *args, **kwargs):
            try:
                # Вызов функции для отправки запроса
                response = func(self, *args, **kwargs)
                new_request = {}
                # Проверяем статус кода ответа
                if hasattr(response, "status_code"):
                    status_code = response.status_code
                    if status_code == 200:
                        # Проверяем статус ответа через метод self.check_request_status
                        if kwargs.get("response_type") == "json":
                            new_request["result"] = response.json()
                        elif kwargs.get("response_type") == "text":
                            new_request["result"] = response.text
                        elif kwargs.get("response_type") == "content":
                            new_request["result"] = response.content
                        else:
                            new_request["result"] = response
                    else:
                        new_request["error"] = self.status_codes.get(status_code, "No info error")
                    new_request["status_code"] = status_code
                else:
                    new_request["status_code"] = 400  # Если ответа нет, возвращаем код 400
                    new_request["error"] = self.status_codes.get(status_code, "No info error")
                
                return new_request

            except requests.ConnectionError:
                return {"error": "ConnectionError", "status_code": 400}

            except requests.Timeout:
                return {"error": "TimeoutError", "status_code": 400}

        return wrapper

    @check_response
    def request_data(self, url: str, headers: dict, response_type: str = None, timeout: Union[int, float] = None):
        """
        header - may be User-agent, proxy ..
        response_type: json | text | content - out response type
        timeout - defoult 5 s
        """
        return requests.get(url=url, headers=headers, timeout=timeout)
