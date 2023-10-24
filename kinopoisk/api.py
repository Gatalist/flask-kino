import random, os, requests, psycopg2
from datetime import datetime
from pathlib import Path
from bs4 import BeautifulSoup as bs
from slugify import slugify
from googleapiclient.discovery import build



class UserAgent:
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13.5; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (X11; Ubuntu; Linux i686; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/116.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.5 Safari/605.1.15",
        "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Trident/6.0)",
        "Mozilla/5.0 (Windows NT 10.0; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.203",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/102.0.0.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/102.0.0.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 OPR/102.0.0.0",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Vivaldi/6.1.3035.257",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Vivaldi/6.1.3035.257",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Vivaldi/6.1.3035.257",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Vivaldi/6.1.3035.257",
        "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Vivaldi/6.1.3035.257",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 YaBrowser/23.7.0.2564 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 YaBrowser/23.7.0.2564 Yowser/2.5 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 13_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 YaBrowser/23.7.0.2564 Yowser/2.5 Safari/537.36",
    ]

    HTTP_PROXIES = [
        '217.21.148.70:8080',
    ]

    HTTPS_PROXIES = [
        '182.53.29.81:8080',
    ]

    def get_user_agent(self):
        user = random.choice(self.user_agents)
        # print("User-Agent:", user)
        return {'User-Agent': user,}

    def get_proxies(self):
        http_proxi = f"http://{random.choice(self.HTTP_PROXIES)}"
        https_proxi = f"http://{random.choice(self.HTTPS_PROXIES)}"
        # print("http_proxi:", http_proxi,"\nhttps_proxi:", https_proxi)
        return {
            'http': http_proxi, 
            'https': https_proxi
            }

    def request_data(self, url: str, proxi: bool = None, key: bool = None):
        header = self.get_user_agent()
        if key:
            header["X-API-KEY"] = key
            header["Content-Type"] = "application/json"

        try:
            if proxi:
                session = requests.Session()
                session.headers = header
                session.proxies = self.get_proxies()
                page = session.get(url)
            else:
                page = requests.get(url, headers=header)
            
            return page
    
        except requests.exceptions.ConnectionError as error:
            return {'error': error}


class KinopoiskApi(UserAgent):
    @property
    def get_static_path(self) -> str:
        folder = os.getcwd()
        split_path = folder.split('/')
        split_path.pop()
        split_path.append('app')
        split_path.append('app')
        split_path.append('static')
        return '/'.join(split_path)

    # request and save image        
    def request_and_save_screen_image(self, data, list_image):
        data_json = data.json()

        media = 'media'
        base_folder = 'images'
        year = str(data_json['year'])
        kinopoiskId = str(data_json['kinopoiskId'])

        list_image_screen = list()
        for img in enumerate(list_image):
            img_id = img[0]
            img_url = img[1]
            name_poster = f"id_{img_id}-" + self.get_date_time() + self.get_type_image(img_url)
            create_path = self.get_or_create_path(os.path.join(self.get_static_path, media, base_folder, year, kinopoiskId))

            # save first image
            get_poster_url = self.request_data(url=img_url, proxi=False)
            image_path = self.save_image(create_path, name_poster, get_poster_url)
            # print(image_path)
            list_image_screen.append(image_path)
        print('save screen imageы')
        return list_image_screen

    # request and save image        
    def request_and_save_title_image(self, data):
        data_json = data.json()

        media = 'media'
        base_folder = 'images'
        year = str(data_json['year'])
        kinopoiskId = str(data_json['kinopoiskId'])
       
        name_poster = "poster-" + self.get_date_time() + self.get_type_image(data_json['posterUrlPreview'])
        create_path = self.get_or_create_path(os.path.join(self.get_static_path, media, base_folder, year, kinopoiskId))

        # save first image
        get_poster_url = self.request_data(url=data_json['posterUrlPreview'], proxi=False)
        image_path = self.save_image(create_path, name_poster, get_poster_url)
        # print(image_path)
        return image_path

    def get_date_time(self) -> str:
        current_date = str(datetime.now().date()) + '-'
        current_time = str(datetime.now().time()).split('.')[0].replace(':', '-')
        return current_date + current_time

    def get_type_image(self, image_url):
        return '.' + image_url.split('.')[-1]

    def save_image(self, image_path, name, requvest_data):
        new_name = str(os.path.join(image_path, name))
        try:
            with open (new_name, 'wb') as file:
                file.write(requvest_data.content)
            # print("\nfile save", new_name)
            return self.prune_path(new_name)
        except Exception as error:
            print(error)

    def get_or_create_path(self, path):
        if os.path.exists(path):
            return path
        Path(path).mkdir(parents=True)
        return path

    def prune_path(self, this_path):
        split_path = this_path.split('static')
        return '/static' + split_path[1]

    def get_list_image_screen(self, data=None):
        if data:
            data_json = data.json()
        url = f"https://m.imdb.com/title/{data_json['imdbId']}"  # Замените на URL вашей веб-страницы
        request_json = self.request_data(url=url, proxi=False, key=False)
        soup = bs(request_json.text, 'html.parser')
        stills_from_the_film = []
        div_tags = soup.find('div', class_='ipc-shoveler ipc-shoveler--base ipc-shoveler--page0')
        if div_tags:
            image_tags = div_tags.find_all('img', class_='ipc-image')

            for img_tag in image_tags:
                img_url = img_tag.get('src')
                if img_url:
                    stills_from_the_film.append(img_url)
            print(f'Image URLS: {len(stills_from_the_film)}')
            return set(stills_from_the_film)
        return stills_from_the_film

    def get_person(self, data):
        data_json = data.json()
        
        director = []
        creator = []
        actor = []
        person = {}

        for elem in data_json:
            if elem.get('professionKey') == 'DIRECTOR' and elem.get('nameRu') != '':
                director.append(elem.get('nameRu'))
            if elem.get('professionKey') == 'ACTOR' and elem.get('nameRu') != '':
                actor.append(elem.get('nameRu'))
            if elem.get('professionKey') == 'WRITER' and elem.get('nameRu') != '':
                creator.append(elem.get('nameRu'))
        
        if len(actor) > 10:
            actor = actor[:10]

        person['creator'] = creator
        person['actor'] = actor
        person['director'] = director

        return person

    def get_similar(self, data):
        data_json = data.json()
        similar = []
        for elem in data_json.get('items'):
            if elem.get('filmId') and elem.get('filmId') != '':
                key = []
                key.append(elem.get('filmId'))
                key.append(elem.get('nameRu'))
                similar.append(key)
        return similar


class YoutubeApi:
    api_key_youtube = 'AIzaSyDJ1t1D-fmqwhfCZua33y6XJJ2RbwG-i2Q'

    youtube = build('youtube', 'v3', developerKey=api_key_youtube)

    def get_first_video_for_youtube(self, search_name) -> str:
        # Выполняем запрос к YouTube API для получения первого видео по ключевому запросу
        search_response = self.youtube.search().list(
            q= search_name, # 'матрица 1999 трейлер',  # Здесь укажите ваш запрос
            type='video',
            part='id',
            maxResults=1  # Указываем, что хотим получить только одно видео
        ).execute()

        # Получаем ID первого видео из результатов поиска
        first_video_id = search_response['items'][0]['id']['videoId']

        # Теперь, если вам нужно получить дополнительную информацию о видео
        # (например, его название и описание), вы можете выполнить следующий запрос:
        video_response = self.youtube.videos().list(
            id=first_video_id,
            part='snippet'
        ).execute()

        # Извлекаем информацию о первом видео
        first_video = video_response['items'][0]
        id_video = first_video['id']
        print(id_video)
        return id_video


class OperationDataBase(KinopoiskApi, YoutubeApi):
    def connect_db(self) -> object:
        return psycopg2.connect(
            host="localhost",
            database="nix_db",
            user="user_db",
            password="xEhs5hU26nDNdeC")
    
    def converting_date_time(self, date_string):
        if date_string:
            # Формат строки даты и времени
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            # Преобразование строки в объект datetime
            return datetime.strptime(date_string, date_format)
        return None
    
    def get_element(self, name, request_to_db, value) -> int:
        conn = self.connect_db()
        cursor = conn.cursor()
        cursor.execute(request_to_db, value)
        result_select = cursor.fetchall()
        if result_select:
            print(f"alredy exist {name}: {result_select[-1]}")
            cursor.close()
            conn.close()
            return result_select[-1][0]
        
    def create_element(self, name, request_to_db, value) -> int:
        if value:
            conn = self.connect_db()
            cursor = conn.cursor()
            cursor.execute(request_to_db, value)
            print(request_to_db, value)
            conn.commit()
            cursor.execute("SELECT lastval();")
            create_val = cursor.fetchone()
            print(f"create {name}: {create_val}")
            cursor.close()
            conn.close()
            return create_val[0]
        return None
    
    def get_or_create_rating_kinopoisk(self, value) -> int:
        if value:
            get_val = self.get_element("reliase", f"SELECT id, star FROM ratingkinopoisk WHERE star = %s;", (value,))
            if get_val:
                return get_val
            
            create_val = self.create_element("reliase", f"INSERT INTO ratingkinopoisk (star) VALUES (%s);", (value,))
            return create_val
        return None
    
    def get_or_create_rating_imdb(self, value) -> int:
        if value:
            get_val = self.get_element("reliase", f"SELECT id, star FROM ratingimdb WHERE star = %s;", (value,))
            if get_val:
                return get_val
            
            create_val = self.create_element("reliase", f"INSERT INTO ratingimdb (star) VALUES (%s);", (value,))
            return create_val
        return None

    def get_or_create_rating_critics(self, value) -> int:
        if value:
            get_val = self.get_element("reliase", f"SELECT id, star FROM ratingfilmcritics WHERE star = %s;", (value,))
            if get_val:
                return get_val
            
            create_val = self.create_element("reliase", f"INSERT INTO ratingfilmcritics (star) VALUES (%s);", (value,))
            return create_val
        return None
    
    def get_movie(self, kinopoisk_id):
        get_val = self.get_element("movie", f"SELECT id, kinopoisk_id, name_ru FROM movie WHERE kinopoisk_id = %s;", (kinopoisk_id,))
        if get_val:
            return get_val

    def get_or_create_year(self, value) -> int:
        if value:
            get_val = self.get_element("reliase", f"SELECT id, year FROM reliase WHERE year = %s;", (value,))
            if get_val:
                return get_val
            
            create_val = self.create_element("reliase", f"INSERT INTO reliase (year) VALUES (%s);", (value,))
            return create_val
        return None
    
    def get_or_create_film_length(self, value) -> int:
        if value:
            get_val = self.get_element("filmlength", f"SELECT id, length FROM filmlength WHERE length = %s;", (value,))
            if get_val:
                return get_val
            
            create_val = self.create_element("filmlength", f"INSERT INTO filmlength (length) VALUES (%s);", (value,))
            return create_val
        return None
    
    def get_or_create_type(self, value) -> int:
        if value:
            get_val = self.get_element("typevideo", f"SELECT id, name FROM typevideo WHERE name = %s;", (value,))
            if get_val:
                return get_val
            
            create_val = self.create_element("typevideo", f"INSERT INTO typevideo (name) VALUES (%s);", (value,))
            return create_val
        return None

    def get_or_create_age_limits(self, value) -> int:
        if value:
            if type(value) == str:
                new_value = "".join(c for c in value if c.isdecimal())
            else:
                new_value = value
            get_val = self.get_element("age", f"SELECT id, name FROM agelimit WHERE name = %s;", (new_value,))
            if get_val:
                return get_val
        
            create_val = self.create_element("age", f"INSERT INTO agelimit (name) VALUES (%s);", (new_value,))
            return create_val
        return None
    
    def get_or_create_genre(self, list_value) -> list:
        genres = []
        for genre in list_value:
            name = genre['genre']
            get_val = self.get_element("genre", f"SELECT id, name FROM genre WHERE name = %s;", (name,))
            if get_val:
                genres.append(get_val)
            else:
                create_val = self.create_element("genre", f"INSERT INTO genre (name) VALUES (%s);", (name,))
                genres.append(create_val)
        return genres

    def get_or_create_country(self, list_value) -> list:
        countries = []
        for country in list_value:
            name = country['country']
            get_val = self.get_element("country", f"SELECT id, name FROM countryreliase WHERE name = %s;", (name,))
            if get_val:
                countries.append(get_val)
            else:
                create_val = self.create_element("country", f"INSERT INTO countryreliase (name) VALUES (%s);", (name,))
                countries.append(create_val)
        return countries

    def get_or_create_director(self, list_value) -> list:
        directors = []
        for director in list_value:
            get_val = self.get_element("director", f"SELECT id, name FROM director WHERE name = %s;", (director,))
            if get_val:
                directors.append(get_val)
            else:
                create_val = self.create_element("director", f"INSERT INTO director (name) VALUES (%s);", (director,))
                directors.append(create_val)
        return directors

    def get_or_create_actor(self, list_value) -> list:
        actors = []
        for actor in list_value:
            get_val = self.get_element("actor", f"SELECT id, name FROM actor WHERE name = %s;", (actor,))
            if get_val:
                actors.append(get_val)
            else:
                create_val = self.create_element("actor", f"INSERT INTO actor (name) VALUES (%s);", (actor,))
                actors.append(create_val)
        return actors
    
    def get_or_create_creator(self, list_value) -> list:
        creators = []
        for creator in list_value:
            get_val = self.get_element("creator", f"SELECT id, name FROM creator WHERE name = %s;", (creator,))
            if get_val:
                creators.append(get_val)
            else:
                create_val = self.create_element("creator", f"INSERT INTO creator (name) VALUES (%s);", (creator,))
                creators.append(create_val)
        return creators
    
    def get_or_create_screen_movie(self, name, list_value) -> list:
        creators = []
        conn = self.connect_db()
        cursor = conn.cursor()
        for screen in list_value:
            cursor.execute(f"INSERT INTO screenshot (name, url) VALUES (%s, %s);", (name, screen))
            conn.commit()
            cursor.execute("SELECT lastval();")
            create_val = cursor.fetchone()
            print(f"create screenshot: {create_val}")
            creators.append(create_val[0])
        cursor.close()
        conn.close()
        return creators

    def get_or_create_similar(self, list_value) -> list:
        similars = []
        for similar in list_value:
            filmId = similar[0]
            nameRu = similar[1]
            get_val = self.get_element("similar", f"SELECT id, kinopoisk_id FROM similars WHERE kinopoisk_id = %s;", (filmId,))
            if get_val:
                similars.append(get_val)
            else:
                create_val = self.create_element("similar", f"INSERT INTO similars (kinopoisk_id, name) VALUES (%s, %s);", (filmId, nameRu))
                similars.append(create_val)
        return similars

    def create_movie(self, data, title_images, screen_image, director, actor, creator, similar) -> list:
        print(data)
        # data_json = data # .json()
        data_json = data.json()
        
        rating_kinopoisk = self.get_or_create_rating_kinopoisk(data_json['ratingKinopoisk'])
        rating_imdb = self.get_or_create_rating_imdb(data_json['ratingImdb'])
        rating_film_critics = self.get_or_create_rating_critics(data_json['ratingFilmCritics'])
        year = self.get_or_create_year(data_json['year'])
        film_length = self.get_or_create_film_length(data_json['filmLength'])
        
        typevideo = self.get_or_create_type(data_json['type'])
        age = self.get_or_create_age_limits(data_json['ratingAgeLimits'])

        
        if data_json['nameOriginal']:
            slug = slugify(str(data_json['kinopoiskId']) + ' ' + data_json['nameOriginal'])
        else:
            slug = slugify(str(data_json['kinopoiskId']) + ' ' + data_json['nameRu'])

        genres = self.get_or_create_genre(data_json['genres'])
        countries = self.get_or_create_country(data_json['countries'])

        directors = self.get_or_create_director(director)
        actors = self.get_or_create_actor(actor)
        creators = self.get_or_create_creator(creator)

        date_format = self.converting_date_time(data_json['lastSync'])

        created = datetime.now()

        screenshots = self.get_or_create_screen_movie(data_json['nameRu'], screen_image)

        similars = self.get_or_create_similar(similar)

        name = """kinopoisk_id, imdb_id, name_ru, name_original, poster_url,
                slug, rating_kinopoisk_id, rating_imdb_id, rating_critics_id, 
                year_id, film_length_id, slogan, description, short_description, 
                type_video_id, age_limits_id, last_syncs, created"""


        values = (data_json['kinopoiskId'],
                data_json['imdbId'],
                data_json['nameRu'],
                data_json['nameOriginal'],
                title_images,
                slug,
                rating_kinopoisk,
                rating_imdb,
                rating_film_critics,
                year,
                film_length,
                data_json['slogan'],
                data_json['description'],
                data_json['shortDescription'],
                typevideo,
                age,
                date_format,
                created,
        )

        insert = f"INSERT INTO movie ({name}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"

        conn = self.connect_db()
        cursor = conn.cursor()
        
        # add movie
        cursor.execute(insert, values)
        conn.commit()
        
        # get new movie id
        cursor.execute("SELECT lastval();")
        new_movie_id = cursor.fetchone()[0]

        list_many_to_many = {}
        list_many_to_many['new_movie_id'] = new_movie_id
        list_many_to_many['genres'] = genres
        list_many_to_many['countries'] = countries
        list_many_to_many['directors'] = directors
        list_many_to_many['actors'] = actors
        list_many_to_many['creators'] = creators
        list_many_to_many['similars'] = similars
        list_many_to_many['screenshots'] = screenshots


        return list_many_to_many
        # создаем связи между таблицами
        # self.create_connection_many_to_many(new_movie_id, genres, countries, directors, actors, creators, screenshots, similars)

    def many_to_many(self, table_name, movie_id, list_many_to_many):
        conn = self.connect_db()
        cursor = conn.cursor()

        print(table_name, list_many_to_many)
        for gen_id in list_many_to_many:
            cursor.execute(f"INSERT INTO {table_name} VALUES (%s, %s);", (movie_id, gen_id))
        
        conn.commit()
        cursor.close()
        conn.close()

    def create_connection_many_to_many(self, list_many_to_many) -> int:
        self.many_to_many('genre_movie', list_many_to_many['new_movie_id'], list_many_to_many['genres'])
        self.many_to_many('country_movie', list_many_to_many['new_movie_id'], list_many_to_many['countries'])
        self.many_to_many('director_movie', list_many_to_many['new_movie_id'], list_many_to_many['directors'])
        self.many_to_many('actor_movie', list_many_to_many['new_movie_id'], list_many_to_many['actors'])
        self.many_to_many('creator_movie', list_many_to_many['new_movie_id'], list_many_to_many['creators'])
        self.many_to_many('screenshot_movie', list_many_to_many['new_movie_id'], list_many_to_many['screenshots'])
        self.many_to_many('similars_movie', list_many_to_many['new_movie_id'], list_many_to_many['similars'])

        print(f"----> movie add [ {list_many_to_many['new_movie_id']} ] <----\n\n")
        return list_many_to_many['new_movie_id']

