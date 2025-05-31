from dotenv import load_dotenv
import os


# Загрузка переменных окружения из .env файла
load_dotenv()


class Settings:
    # host = "localhost"
    host = os.getenv('DB_ADDR')
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    base_kinopoisk_api_url = "https://kinopoiskapiunofficial.tech"
    base_imdb_url = "https://m.imdb.com/"

    # static_path = os.path.join(os.path.split(os.getcwd())[0], 'app', 'app', 'static', 'movie')
    static_path = os.path.join(os.path.split(os.getcwd())[0], 'app', 'static', 'movie')

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

    api_keys = {
        1: [
            os.getenv('KEY_1'), os.getenv('KEY_2'),
            os.getenv('KEY_3'), os.getenv('KEY_4'),
        ],

        2: [
            os.getenv('KEY_5'), os.getenv('KEY_6'),
            os.getenv('KEY_7'), os.getenv('KEY_8'),
        ],

        3: [
            os.getenv('KEY_9'), os.getenv('KEY_10'),
            os.getenv('KEY_11'), os.getenv('KEY_12'),
        ],

        4: [
            os.getenv('KEY_13'), os.getenv('KEY_14'),
            os.getenv('KEY_15'), os.getenv('KEY_16'),
        ],

        5: [
            os.getenv('KEY_17'), os.getenv('KEY_18'),
            os.getenv('KEY_19'), os.getenv('KEY_20'),
        ],

        6: [
            os.getenv('KEY_21'), os.getenv('KEY_22'),
            os.getenv('KEY_23'), os.getenv('KEY_24'),
        ],
    }
