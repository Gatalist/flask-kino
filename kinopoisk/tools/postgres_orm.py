from datetime import datetime

import psycopg2
from functools import wraps
from slugify import slugify
from tools.loguru_logger import logger


def with_cursor(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        with self.connection as conn:
            with conn.cursor() as cursor:
                return method(self, conn, cursor, *args, **kwargs)
    return wrapper


class PostgresDB:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(PostgresDB, cls).__new__(cls)
        return cls._instance

    def __init__(self, host, db_name, user, password):
        if not hasattr(self, 'connection'):
            self.host = host
            self.db_name = db_name
            self.user = user
            self.password = password

            self.connection = self.create_connection()

    def create_connection(self):
        """ Create connecting to DataBase"""
        try:
            connection = psycopg2.connect(
                host=self.host,
                database=self.db_name,
                user=self.user,
                password=self.password
            )
            logger.success("[+] Connect to DataBase successful")
            return connection

        except psycopg2.OperationalError as error:
            logger.error(f"[-] Error connecting to DataBase: {error}")
            return None

    @staticmethod
    def get_current_datetime():
        return datetime.now()

    @staticmethod
    def generate_url_by_first_name(names: list, movie_id: int) -> str | None:
        """ Генерируем url к новому фильму """
        for name in names:
            if name:
                new_name = f"{name} {movie_id}"
                new_url = slugify(new_name)
                logger.info(f"new url: {new_url}")
                return new_url

    @staticmethod
    def get_digit_age_limit(text) -> str | None:
        """ Get digit age from string"""
        if isinstance(text, str):
            val = "".join(c for c in text if c.isdecimal())
            return val

    @staticmethod
    def converting_date_time(date_string) -> datetime | None:
        """ Converting string to datetime """
        if date_string:
            return datetime.strptime(date_string, "%Y-%m-%dT%H:%M:%S.%f")

    @with_cursor
    def select_data(self, conn, cursor, table_name: str, select_keys: str, where_key_name: str, where_key_data) -> dict | None:
        """ Get record id from the database """
        query = f"SELECT {select_keys} FROM {table_name} WHERE {where_key_name} = %s;"
        cursor.execute(query, (where_key_data,))
        row = cursor.fetchone()
        conn.commit()

        if not row:
            return None
        res = self.fetch_one_dict(cursor, row)
        logger.info(f"[+] GET----> {res}")
        return res

    @with_cursor
    def insert_data(self, conn, cursor, table_name: str, keys_name: tuple, values_data: tuple) -> dict | None:
        """ Create a record in the database and get (id) """
        _keys = ', '.join(keys_name)  # tuple to str
        _values = ', '.join(['%s' for _ in keys_name])  # create %s

        query = f"INSERT INTO {table_name} ({_keys}) VALUES ({_values}) RETURNING id;"
        cursor.execute(query, values_data)
        row = cursor.fetchone()
        # print("row", row)
        conn.commit()

        if not row:
            return None
        res = self.fetch_one_dict(cursor, row)
        logger.info(f"[+] INSERT----> {res}")
        return res

    @with_cursor
    def update_data(self, conn, cursor, table_name: str, keys_name: tuple, values_data: tuple, where_key: str, where_value) -> dict | None:
        """ Update a record in the database and return the updated row as dict """

        # Формируем строку SET field1 = %s, field2 = %s и т.д.
        set_clause = ', '.join([f"{key} = %s" for key in keys_name])

        query = f"UPDATE {table_name} SET {set_clause} WHERE {where_key} = %s RETURNING *;"

        values = values_data + (where_value,)

        cursor.execute(query, values)
        row = cursor.fetchone()
        conn.commit()

        if not row:
            return None

        res = self.fetch_one_dict(cursor, row)
        logger.info(f"[+] UPDATE----> {res}")
        return res

    def get_or_create(
            self, table_name: str, select_key: str, where_key_name: str,
            where_key_data: any, insert_keys: tuple, insert_values: tuple) -> dict | None:
        """ Get or create record id from table """

        if where_key_data:
            get_val = self.select_data(
                table_name=table_name,
                select_keys=select_key,
                where_key_name=where_key_name,
                where_key_data=where_key_data
            )

            if get_val:
                return get_val
            else:
                return self.insert_data(
                    table_name=table_name,
                    keys_name=insert_keys,
                    values_data=insert_values
                )

    @with_cursor
    def get_last_id(self, conn, cursor, table_name: str) -> int:
        """ Get last record id from table """
        query = f"SELECT id FROM {table_name} ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else 0

    @with_cursor
    def get_id_by_name(self, conn, cursor, table_name: str, where_key_name: str, where_key_data: str) -> int | None:
        """ Get tag id by name """
        query = f"SELECT id FROM {table_name} WHERE {where_key_name}='{where_key_data}' LIMIT 1"
        cursor.execute(query)
        result = cursor.fetchone()
        return result[0] if result else None

    @with_cursor
    def get_all_ids(self, conn, cursor, table_name: str) -> list:
        """ Get all record ids from table """
        query = f"SELECT id FROM {table_name};"
        cursor.execute(query)
        result = cursor.fetchall()
        if result:
            return [row[0] for row in result]
        else:
            return []

    @with_cursor
    def related_table(self, conn, cursor, table_name: str, movie_id: int, list_data: list) -> None:
        """ Related record_id with movie_id (many to many)"""
        logger.info('\n-------- Related table ------------')

        if list_data:
            logger.info(f"{table_name}, {list_data}")
            for gen_id in list_data:
                cursor.execute(
                    f"INSERT INTO {table_name} VALUES (%s, %s);", (movie_id, gen_id)
                )
            conn.commit()
        else:
            logger.info(f"{table_name}: []")

    @staticmethod
    def get_obj_ids(list_dict) -> list[int]:
        return [obj['id'] for obj in list_dict]

    def get_or_create_from_list(self, table_name: str, select_key: str, where_key_name: str, key_names: tuple, values_data: tuple) -> list[dict] | None:

        count_elem_list = 0
        new_obj_list = []

        for key in values_data:
            if type(key) is list:
                count_elem_list = len(key)
                break

        for _number in range(0, count_elem_list):
            _insert_list_values = []
            _where_key_data = ''
            for _index, _key in enumerate(key_names):
                if isinstance(values_data[_index], list):
                    if isinstance(values_data[_index][_number], dict):
                        _elem = next(iter(values_data[_index][_number].values())).capitalize()
                        _insert_list_values.append(_elem)
                        _where_key_data = _elem
                    else:
                        _elem = values_data[_index][_number]
                        _insert_list_values.append(_elem)
                        _where_key_data = _elem

                elif callable(values_data[_index]):
                    _insert_list_values.append(values_data[_index]())

                elif isinstance(values_data[_index], str):
                    _insert_list_values.append(values_data[_index])

                elif type(values_data[_index]) is int:
                    _insert_list_values.append(values_data[_index])

                elif type(values_data[_index]) is bool:
                    _insert_list_values.append(values_data[_index])

            obj = self.get_or_create(
                table_name=table_name,
                select_key=select_key,
                where_key_name=where_key_name,
                where_key_data=_where_key_data,
                insert_keys=tuple(key_names),
                insert_values=tuple(_insert_list_values)
            )
            if obj:
                new_obj_list.append(obj)

        return new_obj_list

    def create_screen_movie(self, kinopoisk_id: int, list_value: list) -> list:
        logger.info("\n---------- Screenshot add db ----------")
        logger.info(list_value)
        screen = []
        if list_value:
            for src in list_value:
                screen_name = src.split('/')[-1] or src.split('\\')[-1]
                keys = ('publish', 'sorting', 'kinopoisk_id', 'name', 'url', 'created_on')
                values = (True, 100, kinopoisk_id, screen_name, src, datetime.now())

                obj = self.insert_data(
                    table_name='screenshots',
                    keys_name=keys,
                    values_data=values
                )
                idd = obj.get('id')
                screen.append(idd)

        return screen

    def get_or_create_similar(self, list_value) -> list | None:
        logger.info("\n---------- Similar add db ----------")
        logger.info(list_value)
        if list_value:
            lict_obj_id = []
            for key, val in list_value.items():
                keys = ('publish', 'sorting', 'kinopoisk_id', 'name', 'created_on')
                values = (True, 100, key, val, datetime.now())

                obj = self.get_or_create(
                    table_name='similars',
                    select_key='id, kinopoisk_id',
                    where_key_name='kinopoisk_id',
                    where_key_data=key,
                    insert_keys=keys,
                    insert_values=values
                )
                idd = obj.get('id')
                lict_obj_id.append(idd)

            return lict_obj_id

    @with_cursor
    def popular_actor(self, conn, cursor, list_actor: list, count_actor_save: None | int = None) -> list:
        """ проверяем актеров, сортируем по популярности и возвращаем список """
        if list_actor:
            # получаем всех актеров с тегом - 'popular' c db
            query = """SELECT persons.name_ru FROM persons 
                   JOIN tag_person ON persons.id = tag_person.person_id 
                   JOIN tags ON tag_person.tag_id = tags.id 
                   WHERE tags.name = 'popular';"""
            cursor.execute(query)
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
            all_actors = new_list_actor + other_list_actor
            if count_actor_save:
                len_list = len(all_actors)
                if len_list > count_actor_save:
                    return all_actors[:count_actor_save]
            return all_actors
        return []

    def create_video(self, list_video: list) -> list:
        if list_video:
            scip_source = ["KINOPOISK_WIDGET", "UNKNOWN"]
            videos = []
            for video in list_video:
                site = video.get('site')
                if site in scip_source:
                    continue
                name = video.get('name')
                url = video.get('url')

                source = self.get_or_create(
                    table_name='video_sources',
                    select_key='id, name',
                    where_key_name='name',
                    where_key_data=site,
                    insert_keys=('publish', 'sorting', 'name', 'created_on'),
                    insert_values=(True, 100, site, self.get_current_datetime())
                )

                obj = self.insert_data(
                    table_name='videos',
                    keys_name=('publish', 'sorting', 'name', 'url', 'source_id', 'created_on'),
                    values_data=(True, 100, name, str(url), source.get('id'), self.get_current_datetime())
                )
                videos.append(obj)

            return videos
        return []

    @staticmethod
    def fetch_one_dict(cursor, row):
        columns = [desc[0] for desc in cursor.description]
        return dict(zip(columns, row))

    @with_cursor
    def create_movie(self, conn, cursor, *args, **kwargs) -> int:
        _keys = ', '.join(kwargs.keys())  # tuple to str
        _values = ', '.join(['%s' for _ in kwargs.keys()])  # create %s
        _data = tuple(kwargs.values())
        print(f"{_keys=}, {_values=}, {_data=}")
        query = f"INSERT INTO movies ({_keys}) VALUES ({_values}) RETURNING id;"
        cursor.execute(query, _data)
        row = cursor.fetchone()
        conn.commit()

        res =  self.fetch_one_dict(cursor, row)
        movie_id = res.get('id')
        logger.info(f"--- Movie add [+] id = {movie_id} ---")
        logger.info(f"[+] INSERT Movie ----> {res}")
        return movie_id