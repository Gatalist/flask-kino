from datetime import datetime
import psycopg2
from functools import wraps
from slugify import slugify
from libs.services import logger


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
                return slugify(new_name)

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
    def select_data(self, conn, cursor, table_name: str, select_keys: str, where_key_name: str, where_key_data) -> int | None:
        """ Get record id from the database """
        query = f"SELECT {select_keys} FROM {table_name} WHERE {where_key_name} = %s;"
        cursor.execute(query, (where_key_data,))
        result = cursor.fetchone()
        if result:
            idd = result[0] # (1, Админ)
            logger.info(f"[+] GET----> [{idd}]")
            return idd
        else:
            return None

    @with_cursor
    def insert_data(self, conn, cursor, table_name: str, keys_name: tuple, values_data: tuple) -> int | None:
        """ Create a record in the database and get (id) """
        _keys = ', '.join(keys_name)  # tuple to str
        _values = ', '.join(['%s' for _ in keys_name])  # create %s

        query = f"INSERT INTO {table_name} ({_keys}) VALUES ({_values}) RETURNING id;"
        cursor.execute(query, values_data)
        inserted_id = cursor.fetchone()
        conn.commit()

        if inserted_id:
            idd = inserted_id[0]
            logger.info(f"[+] INSERT----> [{idd}]")
            return idd
        else:
            return None

    @with_cursor
    def update_data(self, conn, cursor, table_name: str, keys_name: tuple, values_data: tuple, where_key: str, where_value) -> bool:
        """ Update a record in the database"""
        _keys = ', '.join([f"{key} = %s" for key in keys_name])
        query = f"UPDATE {table_name} SET {_keys} WHERE {where_key} = %s;"

        values = values_data + (where_value,)  # добавляем значение для WHERE
        cursor.execute(query, values)
        conn.commit()

        return cursor.rowcount > 0  # True если была обновлена хотя бы одна строка

    def get_or_create(
            self, table_name: str, select_key: str, where_key_name: str,
            where_key_data: any, insert_keys: tuple, insert_values: tuple) -> int | None:
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




    def get_or_create_from_list(self, table_name: str, select_key: str, where_key_name: str, where_key_data_list: list,
                                insert_keys: tuple, dict_key_name: str) -> list | None:
        if where_key_data_list:
            new_obj_list_id = []
            for val in where_key_data_list:
                if dict_key_name:
                    val_key = val[dict_key_name]
                    values = (val_key, self.get_current_datetime())
                else:
                    val_key = val
                    values = (val, self.get_current_datetime())

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

                idd = self.insert_data(
                    table_name='screenshots',
                    keys_name=keys,
                    values_data=values
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

    @with_cursor
    def create_movie(self, conn, cursor, *args, **kwargs) -> int:
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

        # generate '%s' for value
        split_value = keys.split(',')
        replace_value = ['%s, ' for _ in split_value]
        join_value = ' '.join(replace_value)

        # add movie
        query = f"INSERT INTO movies ({keys}) VALUES ({join_value[:-2]}) RETURNING id;"
        cursor.execute(query, values)
        new_movie_id = cursor.fetchone()[0]
        conn.commit()

        logger.info(f'--- Movie add [+] id = {new_movie_id} ---')
        return new_movie_id
