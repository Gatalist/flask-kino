from parser import Processing, list_api_key_1, list_api_key_2


#  if database clear
#  before start first parser need next step
#  add role, add user Admin, add tag popular-actor, run create_popular_actor
# processing.create_popular_actor(file_actor_name='actor/actor.txt', tag_id=1)
# processing.create_popular_actor(file_actor_name='actor/1965.txt', tag_id=2)  # 1965

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


#  5160 - 5500 - 5660
start = int(input("\nEnter number start: "))
end = int(input("\nEnter number end: "))

processing = Processing(list_keys)
processing.parse_and_create_movie(start_id=start, end_id=end)
