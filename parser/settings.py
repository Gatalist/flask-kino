from dotenv import load_dotenv
import os
# from libs.user_agent import list_user_agent


# Загрузка переменных окружения из .env файла
load_dotenv()


class Settings:
    host = "localhost"
    database = os.getenv('DB_NAME')
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASS')

    static_path = os.path.join(os.path.split(os.getcwd())[0], 'app', 'app', 'static', 'media')

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
