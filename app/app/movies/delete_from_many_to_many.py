from .models import (
    segment_movie, actor_movie, country_movie, creator_movie,
    director_movie, genre_movie, screenshot_movie, similar_movie, user_movie
)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.settings import ProdConfig

# Создаем соединение с базой данных PostgreSQL
engine = create_engine(ProdConfig.SQLALCHEMY_DATABASE_URI)
print(ProdConfig.SQLALCHEMY_DATABASE_URI)
# Создание сессии
Session = sessionmaker(bind=engine)
session = Session()

def query_get_many_to_many(table, model):
    return session.query(table).filter_by(movie_id=model.id).all()

def delete_movie(model):
    # try:
    # получаем записи из таблиц many to many
    list_many_to_many = [
        query_get_many_to_many(segment_movie, model),
        query_get_many_to_many(country_movie, model),
        query_get_many_to_many(actor_movie, model),
        query_get_many_to_many(creator_movie, model),
        query_get_many_to_many(director_movie, model),
        query_get_many_to_many(genre_movie, model),
        query_get_many_to_many(screenshot_movie, model),
        query_get_many_to_many(similar_movie, model),
        query_get_many_to_many(user_movie, model),
    ]

    # Удаление записи
    for table in list_many_to_many:
        print(table)
        for item in table:
            print(table)
            session.delete(item)


    # # Сохраняем изменения
    # session.commit()
    #
    # # Закрытие сессии
    # session.close()
    print("Deleted successfully")
