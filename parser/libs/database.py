from sqlalchemy import create_engine, MetaData, Table, Column, Integer, ForeignKey ,asc, desc
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError
import functools
from datetime import datetime
from slugify import slugify
import time
from settings import Settings
from .utils import current_datetime, generate_url, get_digit_age_limit, converting_date_time, create_dict


class Database:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
        return cls._instance

    def __init__(self, host: str, db_name: str, user: str, password: str):
        self.host: str = host
        self.db_name: str = db_name
        self.user: str = user
        self.password: str = password
        self.engine = None
        self.Session = None
        self.metadata = None
        self.create_connection()

    def create_connection(self):
        try:
            database_url = f"postgresql://{self.user}:{self.password}@{self.host}/{self.db_name}"
            self.engine = create_engine(database_url)
            self.Session = sessionmaker(bind=self.engine)
            # self.session = Session()
            self.metadata = MetaData()  # Для метаданных
            print("[+] Подключение к базе PostgreSQL successful")

        except OperationalError as error:
            print(f"[-] Ошибка подключения к базе PostgreSQL:\n{error}")
            return None

    def db_session(func) -> callable:
        @functools.wraps(func)
        def wrapper_db_session(self, *args, **kwargs):
            session = self.Session()
            try:
                result = func(self, session=session, *args, **kwargs)
                session.commit()
            except Exception as e:
                print("DB error:", e)
                session.rollback()
                result = None
            finally:
                session.close()  # Закрываем сессию
            return result
        return wrapper_db_session

    @db_session
    def add_row(self, table_name: str, attrs: dict, session=None):
        _table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = _table.insert().values(attrs).returning(_table.c.id)
        result = session.execute(stmt).fetchone()
        if result:
            print('add:', result)
            return result[0]

    @db_session
    def get_row(self, table_name: str, attrs: dict, session=None) -> int | None:
        if attrs.get("created_on"):
            attrs.pop("created_on")
        if attrs.get("updated_on"):
            attrs.pop("updated_on")

        _table = Table(table_name, self.metadata, autoload_with=self.engine)
        conditions = [getattr(_table.c, key) == value for key, value in attrs.items()]
        stmt = _table.select().where(*conditions)
        result = session.execute(stmt).fetchone()
        if result:
            print('get:', result)
            return result[0]

    @db_session
    def get_row_full(self, table_name: str, attrs: dict, session=None) -> dict | None:
        _table = Table(table_name, self.metadata, autoload_with=self.engine)
        conditions = [getattr(_table.c, key) == value for key, value in attrs.items()]
        stmt = _table.select().where(*conditions)
        mapping = session.execute(stmt).mappings()  # Возвращаем результаты как словари
        result = [create_dict(**row) for row in mapping]
        if result:
            return result[0]

    @db_session
    def get_rows(self, table_name: str, limit=None, sorted: str = None, attrs: dict=None, session=None):
        _table = Table(table_name, self.metadata, autoload_with=self.engine)
        if sorted:
            stmt = _table.select(attrs).order_by(desc(sorted)) if attrs else _table.select().order_by(asc(sorted))
        else:
            stmt = _table.select(attrs) if attrs else _table.select()

        stmt = stmt.limit(limit) if limit else stmt
        result = session.execute(stmt).fetchall()
        return result

    @db_session
    def get_or_create(self, table_name: str, attrs: dict, session=None):
        if result:= self.get_row(table_name, attrs):
            return result
        return self.add_row(table_name, attrs)
    
    @db_session
    def get_or_create_list(self, table_name: str, data: list, attrs: dict, session=None):
        print(f"{data=}")
        new_list = []
        for item in data:
            attrs["name"] = item
            attrs["created_on"] = current_datetime()
            elem = self.get_or_create(table_name, attrs)
            new_list.append(elem)
        return new_list

    @db_session
    def add_rows(self, table_name: str, list_atrs: list[dict], session=None):
        _table = Table(table_name, self.metadata, autoload_with=self.engine)
        stmt = _table.insert().values(list_atrs)
        result = session.execute(stmt)
        return result

    @db_session
    def get_or_create_similar(self, table_name: str, data: list, attrs: dict, session=None) -> list:
        print("\n---------- Similar add db ----------")
        print(f"{data=}")
        new_list = []
        for key, value in data.items():
            attrs["kinopoisk_id"] = key
            attrs["name"] = value
            attrs["created_on"] = current_datetime()
            elem = self.get_or_create(table_name, attrs)
            new_list.append(elem)
        return new_list
    
    @db_session
    def get_last_id(self, table_name: str, session=None):
        """Получаем последний id фильма с базы"""
        _table = Table(table_name, self.metadata, autoload_with=self.engine)
        # Сортируем по id в обратном порядке и выбираем первую запись
        stmt = _table.select().order_by(_table.c.id.desc()).limit(1)
        # Выполняем запрос
        result = session.execute(stmt).fetchone()
        if result:
            print('get:', result)
            return result[0]

    @db_session
    def get_popular_actor(self, list_actor, count_actor_save, session=None):
        # Загружаем необходимые таблицы
        if list_actor:
            actors_table = Table('actors', self.metadata, autoload_with=self.engine)
            tag_actor_table = Table('tag_actor', self.metadata, autoload_with=self.engine)
            tags_table = Table('tags', self.metadata, autoload_with=self.engine)

            stmt = (
                actors_table.select()
                .join(tag_actor_table, actors_table.c.id == tag_actor_table.c.actor_id)
                .join(tags_table, tag_actor_table.c.tag_id == tags_table.c.id)
                .where(tags_table.c.name == "popular")
                .with_only_columns(actors_table.c.name)
            )

            # Выполняем запрос
            result = session.execute(stmt).fetchall()
            # Возвращаем список имен актеров
            popular_actor =  [row.name for row in result]

            # выбираем с входящего списка популярных актеров и ставим на первое место
            new_list_actor = []
            for actor in list_actor:
                if actor in popular_actor:
                    new_list_actor.append(actor)

            # до заполняем список актеров если нужно
            len_list = len(new_list_actor)
            if len_list < count_actor_save:
                # получаем простых актеров с входящего списка
                other_list_actor = [item for item in list_actor if item not in new_list_actor]
                add_actor = count_actor_save - len_list
                res = new_list_actor + other_list_actor
                return res[:add_actor]

                for actor in list_actor:
                    if len_list == count_actor_save:
                        break
                    if actor not in new_list_actor:
                        new_list_actor.append(actor)
                        len_list += 1
                
                return new_list_actor
            return new_list_actor[:count_actor_save]
        return []

    @db_session
    def create_screen_movie(self, table_name: str, data: list, attrs: dict, session=None) -> list:
        print("\n---------- Screenshot add db ----------")
        screen = []
        if data:
            i = 1
            for src in data:
                values = {
                    "kinopoisk_id": attrs["kinopoisk_id"], 
                    "name": f'{i}_screenshot', 
                    "url": src, 
                    "created_on": current_datetime()
                    }
                idd = self.add_row(table_name, values)
                screen.append(idd)
                print(idd)
                i += 1
        return screen

    @db_session
    def related_table(self, relate_table: str, second_table: str, movie_id: int, col_second: str, fk_second: str, list_data: list, session=None) -> list:

        _relate_table = Table(
            relate_table, self.metadata,
            Column("movie_id", Integer, ForeignKey("movies.id")),
            Column(col_second, Integer, ForeignKey(fk_second)),
            extend_existing=True,
            autoload_with=self.engine
        )

        _second_table = Table(second_table, self.metadata, autoload_with=self.engine)

        links_table = [{"movie_id": movie_id, col_second: idd} for idd in list_data]
        print(f"{links_table=}")
        session.execute(_relate_table.insert(), links_table)

