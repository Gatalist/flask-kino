from datetime import datetime
from slugify import slugify
import time


def current_datetime():
    return datetime.now()


def generate_url(name_ru: str, name_original: str, last_movie_id: int) -> str:
    """Генерируем url к новому фильму"""
    new_movie_id = str(last_movie_id + 1)
    if name_ru:
        slug = slugify(name_ru + ' ' + new_movie_id)
    else:
        slug = slugify(name_original + ' ' + new_movie_id)
    return slug


def get_digit_age_limit(text) -> str:
    if isinstance(text, str):
        val = "".join(c for c in text if c.isdecimal())
        return val


def converting_date_time(date_string) -> datetime:
    if date_string:
        # Формат строки даты и времени
        date_format = "%Y-%m-%dT%H:%M:%S.%f"
        # Преобразование строки в объект datetime
        return datetime.strptime(date_string, date_format)

def create_dict(**kwargs):
    obj = {}
    for key, value in kwargs.items():
        obj[key] = value
    return obj
