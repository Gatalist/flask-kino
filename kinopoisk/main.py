from api import OperationDataBase
import time
import os
from dotenv import dotenv_values



this_path = os.getcwd()
env_file = os.path.join(os.path.split(this_path)[0], 'app', '.env')
env_key = dotenv_values(env_file)


db = OperationDataBase()
base_api_url = "https://kinopoiskapiunofficial.tech/api/"
list_problem = []


# start id -> 298
# end id -> 4647040 +-
# получение данных с api


list_key: list = [
    env_key.get('key_1'), 
    env_key.get('key_2'), 
    env_key.get('key_3'), 
    env_key.get('key_4'), 
    env_key.get('key_5'), 
    env_key.get('key_6'), 
    env_key.get('key_7'),
    ]


status_code = None
for key in list_key:
    print('key:', key)
    for movie in range(10048, 11000):
        # получаем данные фильма
        movie_id = f"{base_api_url}v2.2/films/{movie}"
        request_data = db.request_data(url=movie_id, proxi=False, key=key)

        if not request_data.status_code:
            print(f'kinopoisk id: {movie}')
            print(request_data)
            break
        if request_data.status_code == 401:
            status_code = request_data.status_code
            print('You dont authorization to API service')
            print(request_data)
            break
        print('\n\nstatus_code: ', request_data.status_code)
        if request_data.status_code == 402:
            print('Превышен лимит запросов')
            print(f'kinopoisk id: {movie}')
            break
        if request_data.status_code == 200:
            print(request_data.json())
            # проверяем kinopoiskId в нашей базе
            get_movie = db.get_movie(request_data.json().get('kinopoiskId'))
            if get_movie:
                print(f"movie {[ movie ]} already axsist")
                continue
            
            # получаем актеров, режисеров и директоров  
            movie_man = f"{base_api_url}v1/staff?filmId={movie}"
            request_man = db.request_data(url=movie_man, proxi=False, key=key)
            print('\n\nstatus_code: ', request_man.status_code)
            if request_man.status_code == 402:
                print('Превышен лимит запросов')
                print(f'kinopoisk id: {movie}')
                break
            if request_man.status_code == 200:
                print(request_man.json())
            else:
                print('Нет актеров, режисеров и директоров')

            # получаем kinopoiskId похожих фильмов
            similar_movie = f"{base_api_url}v2.2/films/{movie}/similars"
            request_similar = db.request_data(url=similar_movie, proxi=False, key=key)
            print('\n\nstatus_code: ', request_similar.status_code)
            if request_similar.status_code == 402:
                print('Превышен лимит запросов')
                print(f'kinopoisk id: {movie}')
                break
            if request_similar.status_code == 200:
                print(request_similar.json())
            else:
                print('Нет похожих фильмов')
            
            try:
                # сохраняеме главное фото
                title_image_save = db.request_and_save_title_image(data=request_data)
                # сохраняем кадры к фильму
                screen_image_parse = db.get_list_image_screen(request_data)
                screen_image_save = db.request_and_save_screen_image(data=request_data, list_image=screen_image_parse)

                # актеров, режисер, директор 
                person = db.get_person(request_man)
                directors = person['director']
                actors = person['actor']
                creators = person['creator']
                print(person)

                # получаем kinopoiskId похожих
                similar = db.get_similar(request_similar)
                print('kinopoiskId похожих фильмов', similar)
                
                # сохраняем фильм
                new_movie = db.create_movie(request_data, title_image_save, screen_image_save, directors, actors, creators, similar)
                
                #создаем связи между таблицами
                db.create_connection_many_to_many(new_movie)

                time.sleep(7)
            except:
                print(f"--------> movie - [{movie}]", 'error read <--------')
                list_problem.append(movie)
                time.sleep(2)

        else:
            print(f"request api movie id: {movie}, status_code={request_data.status_code}")

    if status_code:
        break
    print('problem movie ID: ', list_problem)