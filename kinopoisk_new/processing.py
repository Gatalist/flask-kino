from datetime import datetime
from pathlib import Path
import os
from typing import Union, List
import requests
from io import BytesIO
from flask import Response, jsonify
from PIL import Image

from parser.base_parser import WebRequester


class FileImage(WebRequester):
    def __init__(self, static_path):
        self.static_path = static_path

    @staticmethod
    def save_file(name, image_path, request_data, webp=False) -> str | None:
        """Сохраняем файл и возвращаем путь"""
        new_name = str(os.path.join(image_path, name))
        print(new_name)
        try:
            if webp:
                image = Image.open(BytesIO(request_data.content))
                image.save(new_name, format='WEBP', quality=90)
            else:
                with open(new_name, 'wb') as file:
                    file.write(request_data.content)

            print("save")
            new_path = new_name.split('static')
            return '/static' + new_path[1]
        except Exception as error:
            print(error)

    @staticmethod
    def get_or_create_path(my_path) -> str:
        """Проверяем путь к файлу, если его нет то создаем"""
        if os.path.exists(my_path):
            return my_path
        Path(my_path).mkdir(parents=True)
        return my_path

    def generate_movie_path(self, kinopoisk_id, year) -> str:
        """Генерируем путь к папке фильма"""
        new_path = os.path.join(self.static_path, 'media', 'images', str(year), str(kinopoisk_id))
        return self.get_or_create_path(new_path)

    @staticmethod
    def get_new_date_time() -> str:
        """Генерируем часть названия для картинки из даты и времени"""
        current_date = str(datetime.now().date()) + '-'
        current_time = str(datetime.now().time()).split('.')[0].replace(':', '-')
        date_time = current_date + current_time
        return date_time

    def generate_new_image_name(self, name, image_url: str, webp_image) -> str:
        """Генерируем полное название картинки"""
        date_time = self.get_new_date_time()
        if webp_image:
            type_img = ".webp"
        else:
            type_img = '.' + image_url.split('.')[-1]
        new_name_image = f"{name}-{date_time}{type_img}"
        return new_name_image

    def get_image(self, web_url_image, save_path, name, webp_image=True) -> str:
        new_name = self.generate_new_image_name(name=name, image_url=web_url_image, webp_image=webp_image)
        response_image = self.request_data(url=web_url_image, headers=self.get_user_agent())
        new_save = self.save_file(name=new_name, image_path=save_path, request_data=response_image['data'], webp=webp_image)
        return new_save

    def web_save_image(self, web_url_image: Union[str, List[str]], name: str, kinopoisk_id: int, year: int) -> Union[str, List[str]]:
        """Сохраняем изображения и возвращаем путь к файлу.
        Формат выходных данных равен формату входных данных str->str, list->list"""
        path = self.generate_movie_path(kinopoisk_id=kinopoisk_id, year=year)
        if isinstance(web_url_image, str):
            return self.get_image(web_url_image=web_url_image, save_path=path, name=name)
        elif isinstance(web_url_image, list):
            new_image_save_path = []
            for url in web_url_image:
                new_name = self.get_image(web_url_image=url, save_path=path, name=name)
                new_image_save_path.append(new_name)
            return new_image_save_path
        else:
            return []

    # def web_save_image(self, web_url_image: Union[str, List[str]], name: str, kinopoisk_id: int, year: int) -> Union[str, List[str]]:
    #     """Сохраняем изображения и возвращаем путь к файлу.
    #     Формат выходных данных равен формату входных данных str->str, list->list"""
    #     path = self.generate_movie_path(kinopoisk_id=kinopoisk_id, year=year)
    #     if isinstance(web_url_image, str):
    #         new_name = self.generate_new_image_name(name=name, image_url=web_url_image)
    #         response_image = self.request_data(url=web_url_image, headers=self.get_user_agent())
    #         new_save = self.save_file(name=new_name, image_path=path, request_data=response_image['data'],
    #                                   webp=True)
    #         return new_save
    #
    #     if isinstance(web_url_image, list):
    #         new_image_save_path = []
    #         for url in web_url_image:
    #             new_name = self.generate_new_image_name(name=name, image_url=url)
    #             response_image = self.request_data(url=url, headers=self.get_user_agent())
    #             new_save = self.save_file(name=new_name, image_path=path, request_data=response_image['data'],
    #                                       webp=True)
    #             new_image_save_path.append(new_save)
    #         return new_image_save_path