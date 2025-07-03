import hashlib
import time
from pathlib import Path
import os
import random
from typing import Union, List, Tuple
import requests
from io import BytesIO
from PIL import Image
from tools.loguru_logger import logger
from parser.base_parser import WebRequester
from settings import Settings


class FileImage(WebRequester):
    def __init__(self, static_path):
        self.static_path = static_path
        self.placeholder_hashes = Settings.placeholder_hashes

    @staticmethod
    def save_file(name, image_path, request_data, webp=False) -> str | None:
        """Сохраняем файл и возвращаем путь"""
        new_name = str(os.path.join(image_path, name))
        try:
            if webp:
                image = Image.open(BytesIO(request_data.content))
                image.save(new_name, format='WEBP', quality=90)
            else:
                with open(new_name, 'wb') as file:
                    file.write(request_data.content)

            new_path = new_name.split('static')
            return '/static' + new_path[1]
        except Exception as error:
            logger.error(error)

    @staticmethod
    def get_or_create_path(my_path) -> str:
        """Проверяем путь к файлу, если его нет то создаем"""
        if os.path.exists(my_path):
            return my_path
        Path(my_path).mkdir(parents=True)
        return my_path

    def generate_movie_path(self, path_names: list) -> str:
        """Генерируем путь к папке фильма"""
        new_path = os.path.join(self.static_path, *path_names)
        return self.get_or_create_path(new_path)

    @staticmethod
    def get_random_int() -> int:
        """Генерируем часть названия для картинки из даты и времени"""
        return int(time.time()) + random.randint(1, 100)

    def generate_new_image_name(self, name, image_url: str, webp_image) -> str:
        """Генерируем полное название картинки"""
        date_time = self.get_random_int()
        if webp_image:
            type_img = ".webp"
        else:
            type_img = '.' + image_url.split('.')[-1]
        new_name_image = f"{name}-{date_time}{type_img}"
        return new_name_image

    def fetch_images(self, urls: List[str] | str) -> List[Tuple[str, requests.Response]] | Tuple[str, requests.Response] | None:
        """Скачиваем все изображения и возвращаем список кортежей (url, response)"""
        if isinstance(urls, str):
            response = self.request_data(url=urls, headers=self.get_user_agent())
            return urls, response['data']
        elif isinstance(urls, list):
            responses = []
            for url in urls:
                try:
                    response = self.request_data(url=url, headers=self.get_user_agent())
                    responses.append((url, response['data']))
                except Exception as e:
                    raise ConnectionError(f"[-] HTTP ошибка: Ошибка при загрузке {url}: {e}")
            return responses

    def web_save_image(self, web_url_image: Union[str, List[str]], name: str, path_names: list) -> Union[str, List[str], None]:
        """Сохраняем изображения только после полной загрузки"""
        path = self.generate_movie_path(path_names=path_names)

        if isinstance(web_url_image, str):
            url, response_data = self.fetch_images(web_url_image)
            image_hash = hashlib.sha256(response_data.content).hexdigest()
            if image_hash in self.placeholder_hashes:
                return None
            new_name = self.generate_new_image_name(name=name, image_url=url, webp_image=True)
            new_save = self.save_file(name=new_name, image_path=path, request_data=response_data, webp=True)
            return new_save

        elif isinstance(web_url_image, list):
            responses = self.fetch_images(web_url_image)
            new_image_save_paths = []
            i = 1
            for url, response_data in responses:
                if response_data:
                    image_hash = hashlib.sha256(response_data.content).hexdigest()
                    if image_hash in self.placeholder_hashes:
                        continue
                    new_name = self.generate_new_image_name(name=f"{i}_{name}", image_url=url, webp_image=True)
                    new_path = self.save_file(name=new_name, image_path=path, request_data=response_data, webp=True)
                    new_image_save_paths.append(new_path)
                    i += 1

            return new_image_save_paths
        return []


def read_line_file(actor_file):
    with open(actor_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]