from bs4 import BeautifulSoup as bs
from dotenv import dotenv_values
from datetime import datetime
from pathlib import Path
from slugify import slugify
import requests
import psycopg2
import random
import time
import json
import os
import re
from user_agent import list_user_agent
from status_code import bade_status_codes


env_file = dotenv_values(os.path.join(os.path.split(os.getcwd())[0], 'app', '.env'))

list_api_key_1 = [
    env_file.get('KEY_1'),
    env_file.get('KEY_2'),
    env_file.get('KEY_3'),
    env_file.get('KEY_4'),
    env_file.get('KEY_5'),
    env_file.get('KEY_6'),
    env_file.get('KEY_7'),


]

list_api_key_2 = [
    env_file.get('KEY_23'),
    env_file.get('KEY_11'),
    env_file.get('KEY_12'),
    env_file.get('KEY_21'),
    env_file.get('KEY_22'),

    env_file.get('KEY_8'),
    env_file.get('KEY_9'),
    env_file.get('KEY_10'),

    # env_file.get('KEY_13'),
    # env_file.get('KEY_14'),
    # env_file.get('KEY_15'),
    # env_file.get('KEY_16'),
    # env_file.get('KEY_17'),
    # env_file.get('KEY_18'),
    # env_file.get('KEY_19'),
    # env_file.get('KEY_20'),
]


class Parser:
    def __init__(self, list_api_key):
        self.base_kinopoisk_api_url = "https://kinopoiskapiunofficial.tech"
        self.base_imdb_url = "https://m.imdb.com/title/"
        self.static_path = os.path.join(os.path.split(os.getcwd())[0], 'app', 'app', 'static')
        self.list_api_key = list_api_key
        self.iter_key = iter(self.list_api_key)
        self.current_key = self.get_next_api_key()

    # получаем следующий api ключ из списка
    def get_next_api_key(self):
        try:
            self.current_key = next(self.iter_key)
        except StopIteration:
            self.current_key = None

        return self.current_key

    def status_key(self):
        print('api_key:', self.current_key)

    # Получение рандомный User-Agent
    @staticmethod
    def get_user_agent() -> json:
        user = random.choice(list_user_agent)
        return {'User-Agent': user}

    def request_data(self, url: str, api_key: str = None) -> json:
        header = self.get_user_agent()
        if api_key:
            self.status_key()
            header["Content-Type"] = "application/json"
            header["X-API-KEY"] = api_key
        try:
            request = requests.get(url, headers=header)
            if hasattr(request, 'status_code'):
                print("request.status_code =", request.status_code)
                if request.status_code == 402:
                    print("Get next api key")
                    self.get_next_api_key()
                    self.request_data(url, self.current_key)
                if request.status_code == 403:
                    print("Forbidden «Доступ запрещен или не действительный API ключ»")
                    return 403
                if request.status_code == 404:
                    return 404
                return request
            else:
                return 400

        except requests.exceptions.ConnectionError:
            print('\nRetry Connection...')
            self.request_data(url, api_key)
        except RecursionError:
            raise ConnectionError


class Tools(Parser):
    # сохраняем файл
    @staticmethod
    def save_file(image_path, name, request_data) -> str:
        new_name = str(os.path.join(image_path, name))
        try:
            with open(new_name, 'wb') as file:
                file.write(request_data.content)
            print("save")
            new_path = new_name.split('static')
            return '/static' + new_path[1]
        except Exception as error:
            print(error)

    # проверяем путь к файлу, если его нет то создаем
    @staticmethod
    def get_or_create_path(my_path) -> str:
        if os.path.exists(my_path):
            return my_path
        Path(my_path).mkdir(parents=True)
        return my_path
    
    # генерируем путь к папке фильма
    def generate_path(self, data_json) -> str:
        year = str(data_json['year'])
        kinopoisk_id = str(data_json['kinopoiskId'])
        new_path = os.path.join(self.static_path, 'media', 'images', year, kinopoisk_id)
        return self.get_or_create_path(new_path)    

    # сохраняем изображение и возвращаем путь    
    def save_image(self, name, path_image, image_url) -> str:
        current_date = str(datetime.now().date()) + '-'
        current_time = str(datetime.now().time()).split('.')[0].replace(':', '-')
        date_time = current_date + current_time
        if image_url:
            type_img = '.' + image_url.split('.')[-1]
            new_name_image = f"{name}-{date_time}{type_img}"

            data_image = self.request_data(url=image_url)
            return self.save_file(path_image, new_name_image, data_image)

    # сохраняем изображение перебором в цикле
    def save_image_list(self, name, path_image, image_list) -> list:
        print("\n----------- Save File ----------")
        image_path = []
        i = 1
        if image_list:
            for image in image_list:
                new_name = f"{i}_{name}"
                new_path = self.save_image(new_name, path_image, image)
                image_path.append(new_path)
                i += 1
        return image_path

    # считываем всех актеров с файла и возвращаем список
    @staticmethod
    def read_file_actor_name(file_name: str) -> list:
        actor_list = []
        with open(file_name) as reader:
            for line in reader.readlines():
                read_line = line.strip()
                actor_list.append(read_line)
        return actor_list


class ParserKinopoiskIMDB(Tools):
    # получаем по API kinopoisk фильм
    def request_data_movie(self, kinopoisk_id) -> json:
        print(f'\n----------- Movie parsing ----------')
        parse_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/{kinopoisk_id}"
        request = self.request_data(url=parse_url, api_key=self.current_key)

        if request == 403:
            return "Forbidden"
        if request not in bade_status_codes.keys():
            result = request.json()
            # print(result)
            name = result.get('nameRu', '')
            poster = result.get('posterUrl', '')
            year = result.get('year', 0)

            if name:
                print('name', "  |", "True", " |", name)
            else:
                print('name', "  |", "False", "|", name)

            if poster:
                print('poster', "|", "True", " |", poster)
            else:
                print('poster', "|", "False", "|", poster)

            if year >= 1965:
                print('year', "  |", "True", " |", year, ">= 1965")
                if name and poster:
                    return result
            else:
                print('year', "  |", "False", "|", year, "< 1965")
                return None

    # получаем по API kinopoisk режиссеров, актеров, сценаристов
    def request_data_people(self, kinopoisk_id) -> json:
        print(f'\n----------- People parsing ----------')
        parse_url = f"{self.base_kinopoisk_api_url}/api/v1/staff?filmId={kinopoisk_id}"
        request = self.request_data(url=parse_url, api_key=self.current_key)

        director = []
        creator = []
        actor = []

        if request not in bade_status_codes.keys():
            data = request.json()
            for elem in data:
                if elem.get('professionKey') == 'DIRECTOR' and elem.get('nameRu') != '':
                    director.append(elem.get('nameRu'))
                if elem.get('professionKey') == 'ACTOR' and elem.get('nameRu') != '':
                    actor.append(elem.get('nameRu'))
                if elem.get('professionKey') == 'WRITER' and elem.get('nameRu') != '':
                    creator.append(elem.get('nameRu'))
        return {
            'creator': creator,
            'actor': actor,
            'director': director}

    # Получаем по API kinopoisk похожие фильмы
    def request_data_similar(self, kinopoisk_id) -> json:
        print(f'\n----------- Similar parsing ----------')
        parse_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/{kinopoisk_id}/similars"
        request = self.request_data(url=parse_url, api_key=self.current_key)

        if request not in bade_status_codes.keys():
            data = request.json()
            if data:
                similar = {}
                for elem in data.get('items', {}):
                    film_id = elem.get('filmId')
                    if film_id and film_id != '':
                        similar[film_id] = elem.get('nameRu')
                    if len(similar) > 6:
                        return similar
                print('GET SIMILAR:', similar)
                return similar
            return []
    
    # Парсим сайт IMDB и получаем кадры с фильма
    def request_movie_screenshot(self, imdb_id) -> json:
        print(f'\n----------- IMDB parsing ----------')
        parse_url = f"{self.base_imdb_url}{imdb_id}"
        if parse_url:
            request = self.request_data(url=parse_url, api_key=None)

            if request not in bade_status_codes.keys():
                soup = bs(request.text, 'html.parser')

                screenshot = []
                # get fragments from movie
                div_tags = soup.find('div', class_='ipc-shoveler ipc-shoveler--base ipc-shoveler--page0')
                pattern = re.compile(r'https://.*?\.jpg')
                if div_tags:
                    for img_tag in div_tags.find_all('img', class_='ipc-image'):
                        img_url = img_tag.get('srcset')
                        if img_url:
                            matches = pattern.findall(img_url)
                            screenshot.append(matches[-1])

                #  возвращаем картинки
                screen_trailer = {'screenshots': list(set(screenshot))}
                return screen_trailer
            else:
                return {'screenshots': []}

    def parser_top_movie(self, type_top, pages):
        top_movie_id = []
        # type_top = 'TOP_250_MOVIES'
        for page in range(1, pages):
            print(f'\n----------- parsing page: {page} ----------')
            parse_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/collections?type={type_top}&page={page}"
            # print(parse_url)
            request = self.request_data(url=parse_url, api_key=self.current_key)
            if request not in bade_status_codes.keys():
                data = request.json()
                if data:
                    print(data)
                    for film in data['items']:
                        top_movie_id.append(film['kinopoiskId'])
        print(top_movie_id)
        return top_movie_id


class DataBase(Tools):
    @staticmethod
    # подключаемся к базе данных
    def connect_db() -> object:
        return psycopg2.connect(
            host="localhost",
            database=env_file.get('DB_NAME'),
            user=env_file.get('DB_USER'),
            password=env_file.get('DB_PASS')
        )

    # конвертируем дату
    @staticmethod
    def converting_date_time(date_string) -> datetime:
        if date_string:
            # Формат строки даты и времени
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            # Преобразование строки в объект datetime
            return datetime.strptime(date_string, date_format)

    # получаем запись с базы данных (id)
    def select_data(self, table_name: str, select_keys: str, where_key_name: str, where_key_data) -> int:
        with self.connect_db() as conn:
            with conn.cursor() as cursor:
                # транзакция в базу
                cursor.execute(
                    f"SELECT {select_keys} FROM {table_name} WHERE {where_key_name} = %s;", (where_key_data,)
                )
                # получаем объект пример: (1, Админ)
                result_select = cursor.fetchone()
                if result_select:
                    return result_select[0]
    
    # создаем запись в базе данных и получаем (id)
    def insert_data(self, table_name: str, keys_name: tuple, values_data: tuple):
        with self.connect_db() as conn:
            with conn.cursor() as cursor:
                keys_ = ', '.join(keys_name)  # преобразовываем tuple в str
                values_ = ', '.join(['%s' for _ in keys_name])  # # преобразовываем tuple в str и заменяем на %s
                # транзакция в базу
                cursor.execute(
                    f"INSERT INTO {table_name} ({keys_}) VALUES ({values_});", values_data
                )
                conn.commit()

    # записываем данные или получаем и возвращаем (id)
    def get_or_create(self, table_name: str, select_key: str, where_key_name: str, where_key_data: any,
                      insert_keys: tuple, insert_values: tuple) -> int:

        get_val = self.select_data(
            table_name=table_name,
            select_keys=select_key,
            where_key_name=where_key_name,
            where_key_data=where_key_data
        )

        if get_val:
            print("GET---->")
            return get_val
        else:
            print("INSERT---->")
            self.insert_data(
                table_name=table_name,
                keys_name=insert_keys,
                values_data=insert_values
            )

            return self.select_data(
                table_name=table_name,
                select_keys=select_key,
                where_key_name=where_key_name,
                where_key_data=where_key_data
            )

    # генерируем url к новому фильму
    def generate_url(self, data_json) -> str:
        # Получаем последний id фильма с базы
        with self.connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    'SELECT id FROM movies ORDER BY id DESC LIMIT 1'
                )
                result_select = cursor.fetchone()
                if result_select:
                    movie_id = result_select[0]
                else:
                    movie_id = 0

        new_movie_id = str(movie_id + 1)
        if data_json['nameRu']:
            slug = slugify(data_json['nameRu'] + ' ' + new_movie_id)
        else:
            slug = slugify(data_json['nameOriginal'] + ' ' + new_movie_id)
        return slug
    
    # связываем таблицы
    def related_table(self, table_name, movie_id, list_data) -> None:
        print('\n-------- Related table ------------')
        print(table_name, list_data)
        if list_data:
            with self.connect_db() as conn:
                with conn.cursor() as cursor:
                    for gen_id in list_data:
                        cursor.execute(
                            f"INSERT INTO {table_name} VALUES (%s, %s);", (movie_id, gen_id)
                        )
                    conn.commit()

    # получаем пользователя для записи данных
    def get_user(self, name) -> object:
        print('\n------- User ----------')
        get_val = self.select_data(
            table_name='users',
            select_keys='id, username',
            where_key_name='username',
            where_key_data=name
        )

        if get_val:
            print(get_val)
            return get_val

    # проверяем фильм в базе, если находим то пропускаем данный фильм
    def get_movie(self, kinopoisk_id) -> int:
        print(f'\n----------  Поиск фильм в базе ----------')
        get_val = self.select_data(
            table_name='movies',
            select_keys='id, kinopoisk_id',
            where_key_name='kinopoisk_id',
            where_key_data=kinopoisk_id
        )
        if get_val:
            return get_val

    # проверяем актеров, сортируем по популярности и возвращаем список
    def popular_actor(self, list_actor, count_actor_save):
        if list_actor:
            actor_len_list = count_actor_save  # длина списка актеров
            # получаем всех актеров с тегом - 'popular' c db
            with self.connect_db() as conn:
                with conn.cursor() as cursor:                
                    cursor.execute(
                        """SELECT actors.name FROM actors 
                           JOIN tag_actor ON actors.id = tag_actor.actor_id 
                           JOIN tags ON tag_actor.tag_id = tags.id 
                           WHERE tags.name = 'popular';"""
                    )
                    popular_actor = cursor.fetchall()
                    popular_actor = [item[0] for item in popular_actor]
            
            # выбираем с входящего списка популярных актеров и ставим на первое место
            new_list_actor = []
            for actor in list_actor:
                if actor in popular_actor:
                    new_list_actor.append(actor)

            # получаем простых актеров с входящего списка
            other_list_actor = [item for item in list_actor if item not in new_list_actor]
            # до заполняем список актеров если нужно
            len_list = len(new_list_actor)
            if len_list < actor_len_list:
                add_actor = actor_len_list - len_list
                res = new_list_actor + other_list_actor[:add_actor]
                return res
            return new_list_actor
        return []

    def get_idd_from_kinopoisk_idd(self, list_kinopoisk_ld: list):
        list_id = []
        for idd in list_kinopoisk_ld:
            list_id.append(self.get_movie(idd))
        print(list_id)
        return list_id


class Processing(ParserKinopoiskIMDB, DataBase):
    # записываем ссылки на кадры к фильму и получаем (id)
    def create_screen_movie(self, kinopoisk_id, list_value) -> list:
        print("\n---------- Screenshot add db ----------")
        if list_value:
            screen = []
            i = 1
            for src in list_value:
                screen_name = f'{i}_screenshot'

                keys = ('kinopoisk_id', 'name', 'url', 'created_on')
                values = (kinopoisk_id, screen_name, src, datetime.now())

                idd = self.get_or_create(
                    table_name='screenshots',
                    select_key='id, url',
                    where_key_name='url',
                    where_key_data=src,
                    insert_keys=keys,
                    insert_values=values
                )
                screen.append(idd)
                print(idd)
                i += 1
            return screen
    
    # записываем похожие фильмов и возвращаем (id)
    def get_or_create_similar(self, list_value) -> list:
        print("\n---------- Similar add db ----------")
        if list_value:
            lict_obj_id = []
            for key, val in list_value.items():
                keys = ('kinopoisk_id', 'name', 'created_on')
                values = (key, val, datetime.now())

                idd = self.get_or_create(
                    table_name='similars',
                    select_key='id, kinopoisk_id',
                    where_key_name='kinopoisk_id',
                    where_key_data=key,
                    insert_keys=keys,
                    insert_values=values
                )
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
    
    # записываем данные через цикл если их нет и получаем (id)
    def get_or_create_creator(self, elem_list) -> list:
        print("\n---------- Creator add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                keys = ('name', 'created_on')
                values = (val, datetime.now())

                idd = self.get_or_create(
                    table_name='creators',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=val,
                    insert_keys=keys,
                    insert_values=values
                )
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
    
    # записываем данные через цикл если их нет и получаем (id)
    def get_or_create_actor(self, list_actor) -> list:
        print("\n---------- Actor add db ----------")
        if list_actor:
            lict_obj_id = []
            for val in list_actor:
                keys = ('name', 'created_on')
                values = (val, datetime.now())

                idd = self.get_or_create(
                    table_name='actors',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=val,
                    insert_keys=keys,
                    insert_values=values
                )
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id

    def create_popular_actor(self, file_actor_name, tag_id):
        file_actor = self.read_file_actor_name(file_actor_name)
        add_popular_actor = self.get_or_create_actor(list_actor=file_actor)

        self.related_table(table_name='tag_actor', movie_id=tag_id, list_data=add_popular_actor)

    def create_top_250_movie(self, table_name, list_id, tag_id):
        for idd in list_id:
            self.related_table(table_name=table_name, movie_id=idd, list_data=[tag_id])

    # записываем данные через цикл если их нет и получаем (id)
    def get_or_create_director(self, elem_list) -> list:
        print("\n---------- Director add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                keys = ('name', 'created_on')
                values = (val, datetime.now())
                idd = self.get_or_create(
                    table_name='directors',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=val,
                    insert_keys=keys,
                    insert_values=values
                )
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
    
    # записываем данные через цикл если их нет и получаем (id)
    def get_or_create_country(self, elem_list) -> list:
        print("\n---------- Country add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                val_key = val['country']
                keys = ('name', 'created_on')
                values = (val_key, datetime.now())

                idd = self.get_or_create(
                    table_name='countries',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=val_key,
                    insert_keys=keys,
                    insert_values=values
                )
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
    
    # записываем данные через цикл если их нет и получаем (id)
    def get_or_create_genre(self, elem_list) -> list:
        print("\n---------- Genre add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                val_key = val['genre']
                keys = ('name', 'created_on')
                values = (val_key, datetime.now())

                idd = self.get_or_create(
                    table_name='genres',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=val_key,
                    insert_keys=keys,
                    insert_values=values
                )
                lict_obj_id.append(idd)
            
            print(lict_obj_id)
            return lict_obj_id

    # записываем данные и получаем (id)
    def get_or_create_age_limit(self, elem) -> int:
        print("\n---------- Age limit add db ----------")
        # if type(elem) == str:
        if isinstance(elem, str):
            val = "".join(c for c in elem if c.isdecimal())

            keys = ('name', 'created_on')
            values = (val, datetime.now())

            idd = self.get_or_create(
                table_name='age_limits',
                select_key='id, name',
                where_key_name='name',
                where_key_data=val,
                insert_keys=keys,
                insert_values=values
            )
            print(idd)
            return idd

    # записываем данные и получаем (id)
    def get_or_create_type_video(self, elem) -> int:
        print("\n---------- Type video add db ----------")
        if elem:
            keys = ('name', 'created_on')
            values = (elem, datetime.now())

            idd = self.get_or_create(
                table_name='type_videos',
                select_key='id, name',
                where_key_name='name',
                where_key_data=elem,
                insert_keys=keys,
                insert_values=values
            )
            print(idd)
            return idd

    # записываем данные и получаем (id)
    def get_or_create_film_length(self, elem) -> int:
        print("\n---------- Film length add db ----------")
        if elem:
            keys = ('length', 'created_on')
            values = (elem, datetime.now())

            idd = self.get_or_create(
                table_name='film_length',
                select_key='id, length',
                where_key_name='length',
                where_key_data=elem,
                insert_keys=keys,
                insert_values=values
            )
            print(idd)
            return idd

    # записываем данные и получаем (id)
    def get_or_create_release(self, elem) -> int:
        print("\n---------- Release add db ----------")
        if elem:
            keys = ('year', 'created_on')
            values = (elem, datetime.now())

            idd = self.get_or_create(
                table_name='releases',
                select_key='id, year',
                where_key_name='year',
                where_key_data=elem,
                insert_keys=keys,
                insert_values=values
            )
            print(idd)
            return idd

    # записываем данные и получаем (id)
    def get_or_create_rating_critics(self, elem) -> int:
        print("\n---------- Rating film critics add db ----------")
        if elem:
            keys = ('star', 'created_on')
            values = (elem, datetime.now())

            idd = self.get_or_create(
                table_name='rating_critics',
                select_key='id, star',
                where_key_name='star',
                where_key_data=elem,
                insert_keys=keys,
                insert_values=values
            )
            print(idd)
            return idd

    # записываем данные и получаем (id)
    def get_or_create_rating_kinopoisk(self, elem) -> int:
        print("\n---------- Rating_kinopoisk add db ----------")
        if elem:
            keys = ('star', 'created_on')
            values = (elem, datetime.now())

            idd = self.get_or_create(
                table_name='rating_kinopoisk',
                select_key='id, star',
                where_key_name='star',
                where_key_data=elem,
                insert_keys=keys,
                insert_values=values
            )
            print(idd)
            return idd

    # записываем данные и получаем (id)
    def get_or_create_rating_imdb(self, elem) -> int:
        print("\n---------- Rating_Imdb add db ----------")
        if elem:
            keys = ('star', 'created_on')
            values = (elem, datetime.now())

            idd = self.get_or_create(
                table_name='rating_imdb',
                select_key='id, star',
                where_key_name='star',
                where_key_data=elem,
                insert_keys=keys,
                insert_values=values
            )
            print(idd)
            return idd

    # добавляем фильм
    def create_movie(self, *args, **kwargs) -> int:
        keys = ', '.join([f'{i}' for i in kwargs.keys()])
        values = (
            kwargs['kinopoisk_id'],
            kwargs['imdb_id'],
            kwargs['name_ru'],
            kwargs['name_original'],
            kwargs['poster_url'],
            kwargs['slug'],
            kwargs['rating_kinopoisk_id'],
            kwargs['rating_imdb_id'],
            kwargs['rating_critics_id'], 
            kwargs['year_id'],
            kwargs['film_length_id'],
            kwargs['slogan'],
            kwargs['description'],
            kwargs['short_description'],
            kwargs['type_video_id'],
            kwargs['age_limits_id'],
            kwargs['last_syncs'],
            kwargs['user_id'],
            kwargs['created_on']
        )

        # генерируем '%s' для value по длине заполняемых полей
        split_value = keys.split(',')
        replace_value = ['%s, ' for _ in split_value]
        join_value = ' '.join(replace_value)
        # add movie
        insert = f"INSERT INTO movies ({keys}) VALUES ({join_value[:-2]});"
        with self.connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert, values)
                conn.commit()

        # get added movie id
        new_movie_id = self.get_movie(kwargs['kinopoisk_id'])
        print(f'--- Movie add [+] id = {new_movie_id} ---')
        return new_movie_id

    # parse random kinopoisk idd list [234, 3252, 352145, 22]
    def parse_and_create_movie_to_list(self, list_kinopoisk_id: list):
        # получение данных с api
        for movie_id in list_kinopoisk_id:
            print(f'\n\n----> kinopoisk id: {movie_id} <-----')
            # проверяем нет ли в базе фильма с kinopoisk_id = movie_id
            if not self.get_movie(movie_id):
                # получаем все данные для фильма
                print('\n----------  Получение данных для фильма ----------\n')
                movie = self.request_data_movie(kinopoisk_id=movie_id)
                if movie == "Forbidden":
                    break
                if not self.current_key:
                    print("Not API key")
                    break
                if movie and movie != 404:
                    self.build_data_movie(movie)
            else:
                print('\n Фильм уже существует\n')
            print('\n--------- Finish ----------\n\n\n')
            time.sleep(1.5)

    # parse range id -> 298 -> 4 647 040 +-
    def parse_and_create_movie_to_range(self, start_id: int, end_id: int):
        # получение данных с api
        for movie_id in range(start_id, end_id):
            print(f'\n\n----> kinopoisk id: {movie_id} <-----')
            # проверяем нет ли в базе фильма с kinopoisk_id = movie_id
            if not self.get_movie(movie_id):
                # получаем все данные для фильма
                print('\n----------  Получение данных для фильма ----------\n')
                movie = self.request_data_movie(kinopoisk_id=movie_id)
                if movie == "Forbidden":
                    break
                if not self.current_key:
                    print("Not API key")
                    break
                if movie and movie != 404:
                    self.build_data_movie(movie)
            else:
                print('\n Фильм уже существует\n')
            print('\n--------- Finish ----------\n\n\n')
            time.sleep(1.5)

    def build_data_movie(self, movie):
        people = self.request_data_people(kinopoisk_id=movie.get('kinopoiskId'))
        popular_actor = self.popular_actor(people.get('actor'), count_actor_save=12)
        similar = self.request_data_similar(kinopoisk_id=movie.get('kinopoiskId'))
        screen_and_trailer = self.request_movie_screenshot(imdb_id=movie.get('imdbId'))

        # сохраняем картинки и возвращаем ссылки на них
        path = self.generate_path(movie)
        poster = self.save_image(name='postr', path_image=path, image_url=movie.get('posterUrl'))
        screenshot_path = self.save_image_list(
            name='image', path_image=path, image_list=screen_and_trailer.get('screenshots', None))

        # записываем данные в таблицы
        rating_kinopoisk = self.get_or_create_rating_kinopoisk(movie.get('ratingKinopoisk'))
        rating_imdb = self.get_or_create_rating_imdb(movie.get('ratingImdb'))
        rating_critics = self.get_or_create_rating_critics(movie.get('ratingFilmCritics'))
        release = self.get_or_create_release(movie.get('year'))
        film_length = self.get_or_create_film_length(movie.get('filmLength'))
        type_video = self.get_or_create_type_video(movie.get('type'))
        age_limit = self.get_or_create_age_limit(movie.get('ratingAgeLimits'))
        genre = self.get_or_create_genre(elem_list=movie.get('genres'))
        country = self.get_or_create_country(elem_list=movie.get('countries'))
        director = self.get_or_create_director(elem_list=people.get('director'))
        actor = self.get_or_create_actor(list_actor=popular_actor)
        creator = self.get_or_create_creator(elem_list=people.get('creator'))
        screenshot = self.create_screen_movie(movie.get('kinopoiskId', None), screenshot_path)
        similar = self.get_or_create_similar(similar)
        new_url = self.generate_url(movie)

        # создаем фильм
        new_movie = self.create_movie(
            kinopoisk_id=movie.get('kinopoiskId', None),
            imdb_id=movie.get('imdbId', None),
            name_ru=movie.get('nameRu'),
            name_original=movie.get('nameOriginal'),
            poster_url=poster,
            slug=new_url,
            rating_kinopoisk_id=rating_kinopoisk,
            rating_imdb_id=rating_imdb,
            rating_critics_id=rating_critics,
            year_id=release,
            film_length_id=film_length,
            slogan=movie.get('slogan'),
            description=movie.get('description'),
            short_description=movie.get('shortDescription'),
            type_video_id=type_video,
            age_limits_id=age_limit,
            last_syncs=self.converting_date_time(movie.get('lastSync')),
            user_id=self.get_user('Admin'),
            created_on=datetime.now()
        )

        #  сохраняем данные в связанные таблицы many-to-many
        self.related_table(table_name='genre_movie', movie_id=new_movie, list_data=genre)
        self.related_table(table_name='country_movie', movie_id=new_movie, list_data=country)
        self.related_table(table_name='director_movie', movie_id=new_movie, list_data=director)
        self.related_table(table_name='actor_movie', movie_id=new_movie, list_data=actor)
        self.related_table(table_name='creator_movie', movie_id=new_movie, list_data=creator)
        self.related_table(table_name='screenshot_movie', movie_id=new_movie, list_data=screenshot)
        self.related_table(table_name='similar_movie', movie_id=new_movie, list_data=similar)
