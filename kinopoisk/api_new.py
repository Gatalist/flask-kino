import random, os, requests, psycopg2, re, json
from dotenv import dotenv_values
from datetime import datetime
from bs4 import BeautifulSoup as bs
from pathlib import Path
from slugify import slugify
from user_agent import UserAgent
from status_code import codes


class Base:
    base_kinopoisk_api_url = "https://kinopoiskapiunofficial.tech"
    base_imdb_url = "https://m.imdb.com/title/"
    static_path = os.path.join(os.path.split(os.getcwd())[0], 'app', 'app', 'static')
    env_file = dotenv_values(os.path.join(os.path.split(os.getcwd())[0], 'app', '.env'))
    list_key = [
        env_file.get('key_1'), env_file.get('key_2'),
        env_file.get('key_3'), env_file.get('key_4'),
        env_file.get('key_5'), env_file.get('key_6'),
        env_file.get('key_7'), env_file.get('key_8'),
        env_file.get('key_9'), env_file.get('key_10'),
        env_file.get('key_11'), env_file.get('key_12'),
        env_file.get('key_13'), env_file.get('key_14'),
        env_file.get('key_15'), env_file.get('key_16'),
    ]
    key_iter = iter(list_key)
    key = None


class Tools(Base, UserAgent):
    # получение рандомного User-Agent
    def get_user_agent(self) -> json:
        user = random.choice(self.list_user_agent)
        return {'User-Agent': user,}

    # получение данных с сервера по ссылке (и API-key если нужен)
    def request_data(self, url: str, api_key: str = None) -> json:
        header = self.get_user_agent()
        if api_key:
            header["X-API-KEY"] = api_key
            header["Content-Type"] = "application/json"

        try:
            return requests.get(url, headers=header)

        except requests.exceptions.ConnectionError:
            print({'error': 'ConnectionError'})
            self.request_data(url, api_key)

    # сохраняем файл
    def save_file(self, image_path, name, request_data) -> str:
        new_name = str(os.path.join(image_path, name))
        try:
            with open (new_name, 'wb') as file:
                file.write(request_data.content)
            print("save")
            new_path = new_name.split('static')
            return '/static' + new_path[1]
        except Exception as error:
            print(error)

    # проверяем путь к файлу, если его нет то создаем
    def get_or_create_path(self, path) -> str:
        if os.path.exists(path):
            return path
        Path(path).mkdir(parents=True)
        return path
    
    # генерируем путь к папке фильма
    def generate_path(self, data_json) -> str:
        year = str(data_json['year'])
        kinopoiskId = str(data_json['kinopoiskId'])
        new_path = os.path.join(self.static_path, 'media', 'images', year, kinopoiskId)
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
        return None
    
    # сохраняем изображение перебором в цыкле
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
    
    # получаем следующий ключ из списка
    def get_next_api_key(self):
        return next(self.key_iter)
        # self.key = self.get_next_api_key()
    
    def status_key(self):
        print('api_key:', self.key)
        if self.key == None:
            self.key = self.get_next_api_key()
            print('api_key:', self.key)
    
    def print_api_key(self):
        print('api_key:', self.key)

    # считываем всех актеров с файла и возвращаем список
    def read_file_actor_name(self, file_name: str):
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
        
        self.status_key()

        parse_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/{kinopoisk_id}"
        request = self.request_data(url=parse_url, api_key=self.key)
        
        # проверяем если статус ОК то возвращаем данные, если нет то возвращаем None
        response = self.processing_request_status(request)
        if response not in codes.keys():
            result = request.json()
            if result.get('nameRu') and result.get('posterUrl') and result.get('year') > 1965:
                return result
        if response == 402:
            self.key = self.get_next_api_key()
            return self.request_data_movie(kinopoisk_id)

    # получаем по API kinopoisk режисеров, актеров, сценаристов
    def request_data_piople(self, kinopoisk_id) -> json:
        print(f'\n----------- Piople parsing ----------')

        self.status_key()

        parse_url = f"{self.base_kinopoisk_api_url}/api/v1/staff?filmId={kinopoisk_id}"
        request = self.request_data(url=parse_url, api_key=self.key)
        
        # проверяем если статус ОК то возвращаем данные, если нет то возвращаем None
        response = self.processing_request_status(request)
        if response not in codes.keys():
            data = request.json()
            director = []
            creator = []
            actor = []
            
            for elem in data:
                if elem.get('professionKey') == 'DIRECTOR' and elem.get('nameRu') != '':
                    director.append(elem.get('nameRu'))
                if elem.get('professionKey') == 'ACTOR' and elem.get('nameRu') != '':
                    actor.append(elem.get('nameRu'))
                if elem.get('professionKey') == 'WRITER' and elem.get('nameRu') != '':
                    creator.append(elem.get('nameRu'))
            
            person = {}
            person['creator'] = creator
            person['actor'] = actor
            person['director'] = director
            # print(person)
            return person
        if response == 402:
            self.key = self.get_next_api_key()
            return self.request_data_piople(kinopoisk_id)

    # получаем по API kinopoisk похожие фильмы
    def request_data_similar(self, kinopoisk_id) -> json:
        print(f'\n----------- Similar parsing ----------')
        
        self.status_key()

        parse_url = f"{self.base_kinopoisk_api_url}/api/v2.2/films/{kinopoisk_id}/similars"
        request = self.request_data(url=parse_url, api_key=self.key)
        
        # проверяем если статус ОК то возвращаем данные, если нет то возвращаем None
        response = self.processing_request_status(request)
        if response not in codes.keys():
            data = request.json()
            if data:
                similar = {}
                for elem in data.get('items'):
                    filmId = elem.get('filmId')
                    if filmId and filmId != '':
                        similar[filmId] = elem.get('nameRu')
                    if len(similar) > 6:
                        return similar
                print('GET SIMILAR:', similar)
                return similar
            return []
        if response == 402:
            self.key = self.get_next_api_key()
            return self.request_data_similar(kinopoisk_id)

        # return request.json()
    
    # парсим сайт IMDB и получаем кадры с фильма, трейлер
    def request_data_screenshot_and_trailer(self, imdb_id) -> json:
        print(f'\n----------- IMDB parsing ----------')
        parse_url = f"{self.base_imdb_url}{imdb_id}"
        request = self.request_data(url=parse_url, api_key=False)

        # проверяем если статус ОК то возвращаем данные, если нет то возвращаем None
        response = self.processing_request_status(request)
        
        if response not in codes.keys():
            soup = bs(response.text, 'html.parser')

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

            # [print(scre) for scre in screenshot]

            data_trailers = {}
            # В скрипте в данные json - ищем трейлеры
            script_data = soup.find('script', id='__NEXT_DATA__').text
            txt_to_json = json.loads(script_data)
            # получаем все блоки с трейлерами
            trailers = txt_to_json.get('props').get('pageProps').get('aboveTheFoldData').get('primaryVideos').get('edges')
            for trailer in trailers:
                elem = {}
                elem['name'] = trailer['node']['name']['value']
                playbackURLs = trailer['node']['playbackURLs']
                elem['background'] = (trailer['node']['thumbnail']['url']).split(',')[0]
                if playbackURLs: # берем последний елемент - найлучшее качество
                    elem['type'] = playbackURLs[-1]['displayName']['value']
                    elem['url'] = playbackURLs[-1]['url']
                    data_trailers[f'trailer'] = elem

            screen_trailer = {}
            screen_trailer['screenshots'] = set(screenshot)  # возвращаем картинки
            screen_trailer['trailers'] = data_trailers  # возвращаем трейлеры

            # print(screen_trailer)
            return screen_trailer
        else:
            screen_trailer = {}
            screen_trailer['screenshots'] = []  # возвращаем картинки
            screen_trailer['trailers'] = []  # возвращаем трейлеры
            return screen_trailer

    # проверяем и обрабатываем статус код полученых данных
    def processing_request_status(self, request) -> object:
        if hasattr(request, 'status_code'):
            print("request.status_code =", request.status_code)

            if request.ok:
                print("request.ok =", request.ok)
                return request
            else:
                print("request.ok =", request.ok)
                return request.status_code
        else:
            print("request.status_code =", 'None')
            return 400


class DataBase(Base):
    # подключаемся к базе данных
    def connect_db(self) -> object:
        return psycopg2.connect(
            host="localhost",
            database=self.env_file.get('db_name'),
            user=self.env_file.get('db_user'),
            password=self.env_file.get('db_pass'))      

    # конвертируем дату
    def converting_date_time(self, date_string) -> datetime:
        if date_string:
            # Формат строки даты и времени
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            # Преобразование строки в объект datetime
            return datetime.strptime(date_string, date_format)
        return None

    # получаем запись с базы данных (id)
    def select_data(self, table_name: str, select_keys: str, where_key_name: str, where_key_data) -> int:
        with self.connect_db() as conn:
            with conn.cursor() as cursor:
                # ранзакция в базу
                cursor.execute(f"SELECT {select_keys} FROM {table_name} WHERE {where_key_name} = %s;", (where_key_data,))
                # получаем обьект пример: (1, Админ)
                result_select = cursor.fetchall()
                if result_select:
                    admin_user = result_select[-1]
                    return admin_user[0]
    
    # создаем запись в базе данных и получаем (id)
    def insert_data(self, table_name: str, keys_name: set, values_data: set) -> int:
        with self.connect_db() as conn:
            with conn.cursor() as cursor:
                keys_ = ', '.join(keys_name)  # преобразовываем set в str
                values_ = ', '.join(['%s' for _ in keys_name])  # # преобразовываем set в str и заменяем на %s
                # ранзакция в базу
                cursor.execute(f"INSERT INTO {table_name} ({keys_}) VALUES ({values_});", values_data)
                conn.commit()
                # получаем обьект пример: (1, Админ)
                cursor.execute("SELECT lastval();")
                created_obj = cursor.fetchone()
                # Возвращаем ID
                return created_obj[0]

    # записываем данные или получаем и возвращаем (id)
    def get_or_create(self, table_name: str, select_key: str, where_key_name: str, where_key_data: any, insert_keys: set, insert_values: set) -> int:
        get_val = self.select_data(table_name=table_name, select_keys=select_key, where_key_name=where_key_name, where_key_data=where_key_data)
        if get_val:
            return get_val
        create_val = self.insert_data(table_name=table_name, keys_name=insert_keys, values_data=insert_values)
        return create_val
    
    # связываем таблицы
    def related_table(self, table_name, movie_id, list_data) -> None:
        print('\n-------- related table ------------')
        print(table_name, list_data)
        if list_data:
            with self.connect_db() as conn:
                with conn.cursor() as cursor:
                    for gen_id in list_data:
                        cursor.execute(f"INSERT INTO {table_name} VALUES (%s, %s);", (movie_id, gen_id))
                    conn.commit()

    # проверяем актеров, сортируем по популярности и возвращаем список
    def popular_actor(self, list_actor):
        if list_actor:
            actor_len_list = 12  # длина списка актеров
            # получаем всем актеров с тегом - 'popular' c db
            with self.connect_db() as conn:
                with conn.cursor() as cursor:                
                    cursor.execute("""
                        SELECT actor.name
                        FROM actor
                        JOIN tag_actor ON actor.id = tag_actor.actor_id
                        JOIN tagactor ON tag_actor.tagactor_id = tagactor.id
                        WHERE tagactor.name = 'popular';
                    """)
                    popular_actor = cursor.fetchall()
                    popular_actor = [item[0] for item in popular_actor]
                    # print(popular_actor)
            
            # выбираем с входящего списка популярных актеров и ставим на первое место
            new_list_actor = []
            for actor in list_actor:
                if actor in popular_actor:
                    new_list_actor.append(actor)

            # получаем простых актеров с входящего списка
            other_list_actor = [item for item in list_actor if item not in new_list_actor]
            # дозаполняем список актеров если нужно
            len_list = len(new_list_actor)
            if len_list < actor_len_list:
                add_actor = actor_len_list - len_list
                res = new_list_actor + other_list_actor[:add_actor]
                # print(res)
                return res

            # print(new_list_actor)
            return new_list_actor
        return []


class Processing(DataBase):
    # записываем ссылки на кадры к фильму и получаем (id)
    def create_screen_movie(self, kinopoisk_id, list_value) -> list:
        print("\n---------- Screensoot add db ----------")
        if list_value:
            screen = []
            i = 1
            for srс in list_value:
                keys = ('kinopoisk_id', 'name', 'url', 'created_on')
                values = (kinopoisk_id, f'{i}_screenshot', srс, datetime.now())
                idd = self.insert_data(table_name='screenshot', keys_name=keys, values_data=values)
                screen.append(idd)
                i += 1
            print(idd)
            return screen
        return None
    
    # записываем похожие фильмов и возвращаем (id)
    def get_or_create_similar(self, list_value) -> list:
        print("\n---------- Similars add db ----------")
        if list_value:
            lict_obj_id = []
            for key, val in list_value.items():
                keys = ('kinopoisk_id', 'name', 'created_on')
                values = (key, val, datetime.now())
                idd = self.get_or_create(table_name='similars',
                    select_key='id, kinopoisk_id', where_key_name='kinopoisk_id', where_key_data=key,
                    insert_keys=keys, insert_values=values)
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
        return None
    
    # записываем трейлеры к фильму и возвращаем (id)
    def create_trailer(self, list_value) -> list:
        print("\n---------- Trailer add db ----------")
        print(list_value)
        if list_value:
            video = []
            for key, value in list_value.items():
                keys = ('name', 'type', 'url', 'background', 'created_on')
                values = (value.get('name'), value.get('type'), value.get('url'), value.get('background'), datetime.now())
                idd = self.insert_data(table_name='trailer', keys_name=keys, values_data=values)

                video.append(idd)
            print(video)
            return video
        return None
    
    # записываем данные через цыкл если их нет и получаем (id)
    def get_or_create_creator(self, elem_list) -> list:
        print("\n---------- Creator add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                keys = ('name', 'created_on')
                values = (val, datetime.now())
                idd = self.get_or_create(table_name='creator',
                    select_key='id, name', where_key_name='name', where_key_data=val,
                    insert_keys=keys, insert_values=values)
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
        return None
    
    # записываем данные через цыкл если их нет и получаем (id)
    def get_or_create_actor(self, elem_list) -> list:
        print("\n---------- Actor add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                keys = ('name', 'created_on')
                values = (val, datetime.now())
                idd = self.get_or_create(table_name='actor',
                    select_key='id, name', where_key_name='name', where_key_data=val,
                    insert_keys=keys, insert_values=values)
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
        return None
    
    # записываем данные через цыкл если их нет и получаем (id)
    def get_or_create_director(self, elem_list) -> list:
        print("\n---------- Director add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                keys = ('name', 'created_on')
                values = (val, datetime.now())
                idd = self.get_or_create(table_name='director',
                    select_key='id, name', where_key_name='name', where_key_data=val,
                    insert_keys=keys, insert_values=values)
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
        return None
    
    # записываем данные через цыкл если их нет и получаем (id)
    def get_or_create_country(self, elem_list) -> list:
        print("\n---------- Country add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                val_key = val['country']
                keys = ('name', 'created_on')
                values = (val_key, datetime.now())
                idd = self.get_or_create(table_name='country',
                    select_key='id, name', where_key_name='name', where_key_data=val_key,
                    insert_keys=keys, insert_values=values)
                lict_obj_id.append(idd)

            print(lict_obj_id)
            return lict_obj_id
        return None
    
    # записываем данные через цыкл если их нет и получаем (id)
    def get_or_create_genre(self, elem_list) -> list:
        print("\n---------- Genre add db ----------")
        if elem_list:
            lict_obj_id = []
            for val in elem_list:
                val_key = val['genre']
                keys = ('name', 'created_on')
                values = (val_key, datetime.now())

                idd = self.get_or_create(table_name='genre',
                    select_key='id, name', where_key_name='name', where_key_data=val_key,
                    insert_keys=keys, insert_values=values)
                lict_obj_id.append(idd)
            
            print(lict_obj_id)
            return lict_obj_id
        return None

    # записываем данные и получаем (id)
    def get_or_create_agelimit(self, elem) -> int:
        print("\n---------- Agelimit add db ----------")
        if type(elem) == str:
            val = "".join(c for c in elem if c.isdecimal())

            keys = ('name', 'created_on')
            values = (val, datetime.now())
            idd =  self.get_or_create(table_name='agelimit',
                select_key='id, name', where_key_name='name', where_key_data=val,
                insert_keys=keys, insert_values=values)
            print(idd)
            return idd
        return None

    # записываем данные и получаем (id)
    def get_or_create_typevideo(self, elem) -> int:
        print("\n---------- Typevideo add db ----------")
        if elem:
            keys = ('name', 'created_on')
            values = (elem, datetime.now())
            idd = self.get_or_create(table_name='typevideo',
                select_key='id, name', where_key_name='name', where_key_data=elem,
                insert_keys=keys, insert_values=values)
            print(idd)
            return idd
        return None

    # записываем данные и получаем (id)
    def get_or_create_filmlength(self, elem) -> int:
        print("\n---------- filmlength add db ----------")
        if elem:
            keys = ('length', 'created_on')
            values = (elem, datetime.now())
            idd = self.get_or_create(table_name='filmlength',
                select_key='id, length', where_key_name='length', where_key_data=elem,
                insert_keys=keys, insert_values=values)
            print(idd)
            return idd
        return None

    # записываем данные и получаем (id)
    def get_or_create_reliase(self, elem) -> int:
        print("\n---------- Reliase add db ----------")
        if elem:
            keys = ('year', 'created_on')
            values = (elem, datetime.now())
            idd = self.get_or_create(table_name='reliase',
                select_key='id, year', where_key_name='year', where_key_data=elem,
                insert_keys=keys, insert_values=values)
            print(idd)
            return idd
        return None

    # записываем данные и получаем (id)
    def get_or_create_rating_critics(self, elem) -> int:
        print("\n---------- Ratingfilmcritics add db ----------")
        if elem:
            keys = ('star', 'created_on')
            values = (elem, datetime.now())
            idd = self.get_or_create(table_name='ratingfilmcritics',
                select_key='id, star', where_key_name='star', where_key_data=elem,
                insert_keys=keys, insert_values=values)
            print(idd)
            return idd
        return None

    # записываем данные и получаем (id)
    def get_or_create_rating_kinopoisk(self, elem) -> int:
        print("\n---------- Ratingkinopoisk add db ----------")
        if elem:
            keys = ('star', 'created_on')
            values = (elem, datetime.now())
            idd = self.get_or_create(table_name='ratingkinopoisk',
                select_key='id, star', where_key_name='star', where_key_data=elem,
                insert_keys=keys, insert_values=values)
            print(idd)
            return idd
        return None

    # записываем данные и получаем (id)
    def get_or_create_rating_imdb(self, elem) -> int:
        print("\n---------- Ratingimdb add db ----------")
        if elem:
            keys = ('star', 'created_on')
            values = (elem, datetime.now())
            idd = self.get_or_create(table_name='ratingimdb',
                select_key='id, star', where_key_name='star', where_key_data=elem,
                insert_keys=keys, insert_values=values)
            print(idd)
            return idd
        return None

    # проверяем фильм в базе, если находим то пропускаем данный фильм
    def get_movie(self, kinopoisk_id) -> object:
        print(f'\n---- проверяем фильм в базе----')
        get_val = self.select_data(table_name='movie', select_keys='id, kinopoisk_id', where_key_name='kinopoisk_id', where_key_data=kinopoisk_id)
        if get_val:
            print('\nmovie уже существует\n')
            return False
        print('\nобработка данных для записи\n')
        return True
    
    # получаем пользователя для записи данных
    def get_user(self, name) -> object:
        print('\n------- User ----------')
        get_val = self.select_data(table_name='users', select_keys='id, username', where_key_name='username', where_key_data=name)
        if get_val:
            print(get_val)
            return get_val

    # генерируем url к новому фильму
    def generate_url(self, data_json) -> str:
        with self.connect_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute('SELECT id FROM movie ORDER BY id DESC LIMIT 1')
                result_select = cursor.fetchone()
                if result_select:
                    movie_id = result_select[0]
                else:
                    movie_id = 0
        
        new_movie_id = str(movie_id + 1)
        if data_json['nameOriginal']:
            slug = slugify(new_movie_id + ' ' + data_json['nameOriginal'])
        else:
            slug = slugify(new_movie_id + ' ' + data_json['nameRu'])
        return slug

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

        insert = f"INSERT INTO movie ({keys}) VALUES ({join_value[:-2]});"
        with self.connect_db() as conn:
            with conn.cursor() as cursor:              
                # add movie
                cursor.execute(insert, values)
                conn.commit()

                # get new movie id
                cursor.execute("SELECT lastval();")
                new_movie_id = cursor.fetchone()[0]

        print('--- add movie ---')
        return new_movie_id
    