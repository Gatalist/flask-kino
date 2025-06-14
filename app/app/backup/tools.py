
import os
from datetime import datetime
from dotenv import dotenv_values
from pathlib import Path
import csv
from app import db
from app.movies.models import (
    RatingKinopoisk, RatingImdb, RatingCritic, Release, FilmLength, Genre, AgeLimit, TypeVideo, Person,
    Screenshot, Similar, Country, Tag, Segment, Movie, genre_movie, country_movie, director_movie, creator_movie,
    actor_movie, screenshot_movie, similar_movie, user_movie, segment_movie, tag_person
)


env_file = dotenv_values(os.path.join(os.getcwd(), '.env'))


class Backup:
    model_list = [
        RatingKinopoisk, RatingImdb, RatingCritic, Release, FilmLength, Genre, AgeLimit, TypeVideo, Person,
        Screenshot, Similar, Country, Tag, Segment, Movie,
    ]

    link_list = [
        genre_movie,
        country_movie, director_movie, creator_movie, actor_movie, screenshot_movie, similar_movie,
        user_movie, segment_movie, tag_person, actor_movie
    ]

    @staticmethod
    def get_or_create_path(my_path) -> str:
        if os.path.exists(my_path):
            return my_path
        Path(my_path).mkdir(parents=True)
        return my_path

    @staticmethod
    def get_all_tables_from_db() -> list:
        # Получение объекта MetaData из экземпляра SQLAlchemy
        metadata = db.metadata
        # Получение списка всех таблиц в базе данных
        tables = metadata.tables.keys()
        # Вывод названий всех таблиц
        for table_name in tables:
            print(table_name)
        return tables

    @staticmethod
    def get_name_and_columns_from_table(model) -> tuple:
        table = None
        if model.__dict__.get('__tablename__', None):
            # простые таблицы
            table = True
            name = model.__dict__.get('__tablename__', None)
            columns = [column.key for column in model.__table__.columns if column.key != '_sa_instance_state']
        else:
            # many to many
            name = model.__dict__.get('name', None)
            columns = [column.name for column in model.columns]

        return table, name, columns

    @staticmethod
    def write_data_model(file_name, model, columns, data):
        # Функция для записи данных в CSV файл
        with open(f'{file_name}', 'w', newline='') as csvfile:
            # Устанавливаем заголовки CSV
            csv_writer = csv.DictWriter(csvfile, fieldnames=columns)
            csv_writer.writeheader()
            # Записываем данные
            for record in data:
                # Создаем словарь для записи, исключая _sa_instance_state
                data = {column.key: getattr(record, column.key) for column in model.__table__.columns if
                        column.key != '_sa_instance_state'}
                csv_writer.writerow(data)

    @staticmethod
    def write_data_link_table(file_name, columns, data):
        # Открываем файл CSV для записи
        with open(file_name, 'w', newline='') as csvfile:
            # Создаем объект writer
            csv_writer = csv.writer(csvfile)
            # Записываем заголовки (если нужно)
            csv_writer.writerow(columns)
            # Записываем данные
            for relationship in data:
                csv_writer.writerow(relationship)

    def create_backup_table(self) -> list:
        result_list = []
        type_file = '.csv'
        current_date = datetime.now().strftime("%d-%m-%Y")
        print(current_date)
        save_path = self.get_or_create_path(f"/home/backup/{current_date}")
        list_table = self.model_list + self.link_list

        for Model in list_table:
            table, f_name, columns = self.get_name_and_columns_from_table(Model)
            print(f_name)
            filename_path = f"{save_path}/{f_name}{type_file}"

            # получаем все данные с таблицы модели
            model_data = db.session.query(Model).all()

            # Открываем файл CSV для записи
            if table:
                self.write_data_model(filename_path, Model, columns, model_data)
            else:
                self.write_data_link_table(filename_path, columns, model_data)
            result_list.append(f_name)

        return result_list

    def restore_backup_table(self):
        type_file = '.csv'
        current_date = datetime.now().strftime("%d-%m-%Y")
        print(current_date)
        save_path = self.get_or_create_path(f"/home/backup/{current_date}")
        list_table = self.model_list + self.link_list

        for Model in list_table:
            table, f_name, columns = self.get_name_and_columns_from_table(Model)
            # print(f_name)
            filename_path = f"{save_path}/{f_name}{type_file}"

            # Открываем файл CSV для чтения
            with open(filename_path, 'r', newline='') as csvfile:
                # Создаем объект DictReader
                csv_reader = csv.DictReader(csvfile)
                # Читаем данные и добавляем их в базу данных
                for row in csv_reader:
                    print(row)
                    # Создаем объект модели и заполняем его атрибуты данными из файла CSV
                    # new_record = Model(**row)
                    # # Добавляем объект в сессию
                    # db.session.add(new_record)

                    # Пропускаем заголовки
                    # next(reader)

                    # Получение максимального значения id в таблице базы данных
                    # max_id = db.session.query(db.func.max(Model.id)).scalar()
                    #
                    # print("Максимальное значение id:", max_id)

                    # Новое значение для счетчика автоинкремента
                    # new_value = 1000  # Замените на нужное вам значение

                    # Выполните сырой SQL-запрос для обновления счетчика автоинкремента
                    # query = f"SELECT setval(pg_get_serial_sequence('{table_name}', 'id'), {new_value}, false);"
                    # db.engine.execute(query)


        # Коммитим изменения в базу данных
        # db.session.commit()
        return ['Yes']
