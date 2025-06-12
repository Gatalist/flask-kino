from datetime import datetime
import psycopg2
from psycopg2 import OperationalError
from slugify import slugify
from libs.services import logger


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
        try:
            connection = psycopg2.connect(
                host=self.host,
                database=self.db_name,
                user=self.user,
                password=self.password
            )
            logger.info("[+] Подключение к базе PostgreSQL successful")
            return connection

        except OperationalError as error:
            logger.debug(f"[-] Ошибка подключения к базе PostgreSQL: {error}")
            return None

    @staticmethod
    def current_datetime():
        return datetime.now()

    @staticmethod
    def generate_url(name_ru: str, name_original: str, last_movie_id: int) -> str:
        """Генерируем url к новому фильму"""
        new_movie_id = str(last_movie_id + 1)
        if name_ru:
            return slugify(name_ru + ' ' + new_movie_id)
        return slugify(name_original + ' ' + new_movie_id)

    @staticmethod
    def get_digit_age_limit(text) -> str:
        if isinstance(text, str):
            val = "".join(c for c in text if c.isdecimal())
            return val

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
        with self.connection as conn:
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
        with self.connection as conn:
            with conn.cursor() as cursor:
                keys_ = ', '.join(keys_name)  # преобразовываем tuple в str
                values_ = ', '.join(['%s' for _ in keys_name])  # # преобразовываем tuple в str и заменяем на %s
                # транзакция в базу
                cursor.execute(
                    f"INSERT INTO {table_name} ({keys_}) VALUES ({values_});", values_data
                )
                conn.commit()

    # записываем данные или получаем и возвращаем (id)
    def get_or_create(
            self, table_name: str, select_key: str, where_key_name: str,
            where_key_data: any, insert_keys: tuple, insert_values: tuple) -> int | None:

        if where_key_data:
            get_val = self.select_data(
                table_name=table_name,
                select_keys=select_key,
                where_key_name=where_key_name,
                where_key_data=where_key_data
            )

            if get_val:
                logger.info(f"[+] GET----> [{get_val}]")
                return get_val
            else:
                logger.info(f"[+] INSERT----> [{get_val}]")
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
        return None

    def create_screen_movie(self, kinopoisk_id: int, list_value: list) -> list:
        logger.info("\n---------- Screenshot add db ----------")
        logger.info(list_value)
        screen = []
        if list_value:
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
                i += 1
        return screen

    def get_or_create_similar(self, list_value) -> list | None:
        logger.info("\n---------- Similar add db ----------")
        logger.info(list_value)
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

            logger.info(lict_obj_id)
            return lict_obj_id

    def get_or_create_from_list(self, table_name: str, select_key: str, where_key_name: str, where_key_data_list: list,
                                insert_keys: tuple, dict_key_name: str) -> list | None:
        if where_key_data_list:
            new_obj_list_id = []
            for val in where_key_data_list:
                if dict_key_name:
                    val_key = val[dict_key_name]
                    values = (val_key, self.current_datetime())
                else:
                    val_key = val
                    values = (val, self.current_datetime())

                idd = self.get_or_create(
                    table_name=table_name,
                    select_key=select_key,
                    where_key_name=where_key_name,
                    where_key_data=val_key,
                    insert_keys=insert_keys,
                    insert_values=values
                )
                new_obj_list_id.append(idd)

            logger.info(new_obj_list_id)
            return new_obj_list_id

    def get_last_movie_id(self):
        """Получаем последний id фильма с базы"""
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT id FROM movies ORDER BY id DESC LIMIT 1"""
                )
                result_select = cursor.fetchone()
                movie_id = 0
                if result_select:
                    movie_id = result_select[0]
                return movie_id

    def get_tag_id(self, name: str) -> int | None:
        """Получаем последний id фильма с базы"""
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    f"SELECT id FROM tags WHERE name='{name}' LIMIT 1"
                )
                result_select = cursor.fetchone()
                if result_select:
                    return result_select[0]

    # связываем таблицы
    def related_table(self, table_name: str, movie_id: int, list_data: list) -> None:
        logger.info('\n-------- Related table ------------')

        if list_data:
            logger.info(f"{table_name}, {list_data}")
            with self.connection as conn:
                with conn.cursor() as cursor:
                    for gen_id in list_data:
                        cursor.execute(
                            f"INSERT INTO {table_name} VALUES (%s, %s);", (movie_id, gen_id)
                        )
                    conn.commit()
        else:
            logger.info(f"{table_name}: []")

    # проверяем актеров, сортируем по популярности и возвращаем список
    def popular_actor(self, list_actor: list, count_actor_save: None | int = None) -> list:
        if list_actor:
            # получаем всех актеров с тегом - 'popular' c db
            with self.connection as conn:
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
            all_actors = new_list_actor + other_list_actor
            if count_actor_save:
                len_list = len(all_actors)
                if len_list > count_actor_save:
                    return all_actors[:count_actor_save]
            return all_actors
        return []

    def get_all_ids(self, table_name: str):
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(f"SELECT id FROM {table_name};")
                return [row[0] for row in cursor.fetchall()]

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
            kwargs['created_on'],
            kwargs['has_3d'],
            kwargs['has_imax'],
            kwargs['short_film'],
            kwargs['publish']
        )

        # генерируем '%s' для value по длине заполняемых полей
        split_value = keys.split(',')
        replace_value = ['%s, ' for _ in split_value]
        join_value = ' '.join(replace_value)
        # add movie
        insert = f"INSERT INTO movies ({keys}) VALUES ({join_value[:-2]});"
        with self.connection as conn:
            with conn.cursor() as cursor:
                cursor.execute(insert, values)
                conn.commit()

        # get added movie id
        new_movie_id = self.select_data(
            table_name='movies',
            select_keys='id, kinopoisk_id',
            where_key_name='kinopoisk_id',
            where_key_data=kwargs['kinopoisk_id'])
        logger.info(f'--- Movie add [+] id = {new_movie_id} ---')
        return new_movie_id
