
def get_popular_actor_from_file(actor_file):
    with open(actor_file, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]
