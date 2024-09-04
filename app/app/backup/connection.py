import psycopg2
import os
from datetime import datetime
from dotenv import dotenv_values
from pathlib import Path
import csv


env_file = dotenv_values(os.path.join(os.getcwd(), '.env'))


# Подключение к базе данных PostgreSQL
def connect_db() -> object:
    return psycopg2.connect(
        host=env_file.get('DB_ADDR'),
        database=env_file.get('DB_NAME'),
        user=env_file.get('DB_USER'),
        password=env_file.get('DB_PASS')
    )


def get_or_create_path(my_path) -> str:
    if os.path.exists(my_path):
        return my_path
    Path(my_path).mkdir(parents=True)
    return my_path


def get_all_tables() -> list:
    # Получение списка всех таблиц
    sql_query = """SELECT table_name FROM information_schema.tables WHERE table_schema = 'public'"""
    with connect_db() as conn:
        with conn.cursor() as cursor:
            # Выполнение SQL-запроса
            cursor.execute(sql_query)
            # Получение результатов запроса
            obj_list = cursor.fetchall()
            return [name[0] for name in obj_list]


def create_backup_table() -> list:
    table_names = get_all_tables()
    result_list = []
    type_file = '.csv'

    for name in table_names:
        f_name = f"{name}{type_file}"
        current_date = datetime.now().strftime("%d-%m-%Y")
        save_path = get_or_create_path(f"/home/backup/{current_date}")
        filename_path = f"{save_path}/{f_name}"
        with connect_db() as conn:
            with conn.cursor() as cursor:
                # Открытие бекап файла для записи
                with open(filename_path, 'w') as backup_file:
                    # Выполнение SQL-запроса для создания бекап
                    cursor.copy_to(backup_file, name)
                    result_list.append(f"{f_name}")
    return result_list


def restore_backup_table():
    type_file = '.csv'
    date_restore = '29-04-2024'
    get_path = f"/home/backup/{date_restore}"

    files_ = os.listdir(get_path)
    # Получаем названия файлов без расширений
    files = [os.path.splitext(file)[0] for file in files_]

    list_good = []
    list_error = []

    if os.path.exists(get_path):
        for name in files:
            f_name = f"{name}{type_file}"
            filename_path = os.path.join(get_path, f_name)
            print(filename_path)
            if os.path.exists(filename_path):
                with connect_db() as conn:
                    with conn.cursor() as cursor:
                        # Открытие файла с данными для загрузки в таблицу
                        with open(filename_path, 'r') as f:
                            # загрузить данные из файла 'данные.csv' в таблицу 'my_table'
                            cursor.copy_from(f, name)
                            list_good.append(name)

                        # нужно обновить индекс таблиц в базе после восстановления кроме таблиц many to many

                        # Чтение данных из файла CSV и определение максимального значения id
                        # max_id_in_csv = 0
                        # with open(filename_path, 'r') as csvfile:
                        #     reader = csv.reader(csvfile, delimiter='\t')
                        #     next(reader)  # Пропускаем заголовки
                        #     for row in reader:
                        #         max_id_in_csv = max(max_id_in_csv, int(
                        #             row[0]))  # Предполагается, что id находится в первом столбце
                        #
                        # # Получение максимального значения id в таблице базы данных
                        # cursor.execute(f"SELECT MAX(id) FROM {name}")
                        # max_id_in_db = cursor.fetchone()[0] or 0
                        #
                        # # Обновление счетчика автоинкремента в базе данных
                        # new_autoincrement_value = max(max_id_in_csv, max_id_in_db) + 1
                        # cursor.execute(f"ALTER SEQUENCE {name}_id_seq RESTART WITH {new_autoincrement_value}")
                        # print("--------new_autoincrement_value: ", new_autoincrement_value)
                        # # Фиксация изменений и закрытие соединения
                        # conn.commit()
                        # cursor.close()
                        # conn.close()

            else:
                list_error.append(name)

        if list_error:
            return list_error

        return list_good
    else:
        return ["Not directory"]
