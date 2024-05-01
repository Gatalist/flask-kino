from parser import Processing, list_api_key_1, list_api_key_2


print("Enter number list key 1 or 2")
number = int(input("\nEnter number: "))
if number == 1:
    list_keys = list_api_key_1
elif number == 2:
    list_keys = list_api_key_2
elif number == 3:
    list_keys = list_api_key_1 + list_api_key_2
else:
    list_keys = []


processing = Processing(list_keys)


# 18000
start = int(input("\nEnter number start: "))
end = int(input("\nEnter number end: "))
processing.parse_and_create_movie_to_range(start_id=start, end_id=end)


#  if database clear
#  before start first parser need next step
#  add role, add user Admin, add tag popular-actor, run create_popular_actor
# processing.create_popular_actor(file_actor_name='actor/actor.txt', tag_id=1)
# processing.create_popular_actor(file_actor_name='actor/1965.txt', tag_id=2)  # 1965


# получаем все идд фильмов кинопоиск_ид
# type_top = 'TOP_250_MOVIES'
# type_top = 'TOP_250_TV_SHOWS'
# type_top = 'TOP_POPULAR_MOVIES'
# list_movie = processing.parser_top_movie(type_top=type_top, pages=35)
# list_movie = [571335]


# добавляем все фильмы (парсим)
# processing.parse_and_create_movie_to_list(list_kinopoisk_id=list_movie)
# получаем добавленные идд фильмов
# top_movie_id = processing.get_idd_from_kinopoisk_idd(list_movie)
# # создаем сегмент с нашими фильмами
# processing.create_top_250_movie(table_name='segment_movie', list_id=top_movie_id, tag_id=3)
