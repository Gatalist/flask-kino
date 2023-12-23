from .models import Movie, Reliase, Genre, Director, genre_movie, director_movie, RatingKinopoisk
from sqlalchemy.orm import joinedload
from flask import session



class MixinMovie:    
    data_sorted = [
        {'value': "standart", 'text': 'стандартная',},
        {'value': "rating_asc", 'text': 'От мин до мах рейтинга',},
        {'value': "rating_desc", 'text': """От мах до мин рейтинга""",},
        {'value': "release_date_asc", 'text': 'От старых до новых',},
        {'value': "release_date_desc", 'text': 'От новых до старых',},]
    
    context = {}

    def create_context(self):
        self.context["movies_sorted"] = self.data_sorted
        self.context["all_reliase"] = self.get_years()
        self.context["all_genres"] = self.get_genres()
        self.context["all_directors"] = self.top_directors()

    def top_directors(self):
        return Director.query.join(director_movie).group_by(Director.id).order_by(Director.id.desc())[:15]
    
    def get_genres(self):
        return Genre.query #.all()
    
    def get_years(self):
        return Reliase.query.order_by(Reliase.year.desc()) #.all()

    def session_data(self, name, data):
        session.permanent = True
        if name not in session:
            session[name] = data
        else:
            session[name] = data
        session.modified = True
        return session

    def update_context_session(self, reliase, genre, director):
        # Добавляем активные фильтра в context
        self.context["is_active_years"] = reliase
        self.context["is_active_genres"] = genre
        self.context["is_active_directors"] = director
        # добавляем фильтра в сессию
        self.session_data('is_active_years', reliase)
        self.session_data('is_active_genres', genre)
        self.session_data('is_active_directors', director)
    
    def filter_movie(self, form=None):
        if form and form.get('form_name') == 'filter_movie':
            reliase = self.is_activate_filter(form, 'year_')
            genre = self.is_activate_filter(form, 'genre_')
            director = self.is_activate_filter(form, 'director_')
            self.update_context_session(reliase, genre, director)
        
        else:
            reliase = session.get('is_active_years')
            genre = session.get('is_active_genres')
            director = session.get('is_active_directors')
            self.update_context_session(reliase, genre, director)

        # фильтруем фильмы
        return self.activate_filter(reliase, genre, director)

    def is_activate_filter(self, form, filter_name):
        list_activate_filter = []
        for filter in form:
            if filter.startswith(filter_name):
                filter_id = filter[len(filter_name):]
                list_activate_filter.append(int(filter_id))
        print(list_activate_filter)
        return list_activate_filter

    def activate_filter(self, active_reliase, active_genre, active_directors):
        movies = Movie.query
        if active_reliase:
            movies = movies.join(Reliase).filter(Reliase.id.in_(active_reliase))
        if active_genre:
            movies = movies.join(genre_movie).join(Genre).options(joinedload(Movie.genres)).filter(Genre.id.in_(active_genre))
        if active_directors:
            movies = movies.join(director_movie).join(Director).options(joinedload(Movie.genres)).filter(Director.id.in_(active_directors))
        return movies
    
    def get_name_sorted(self, name):
        for n in self.data_sorted:
            if n.get('value') == name:
                return n.get('text')

    def sort_movie(self, movie, form=None):
        sorted = None
        if form and form.get('form_name') == 'sorted_movie':
            sorted = form.get('sorted')
            self.session_data('sorted', sorted)
            self.context["sorted_name"] = self.get_name_sorted(sorted)
        else:
            sorted = session.get('sorted')
            self.context["sorted_name"] = self.get_name_sorted(sorted)
        
        if sorted == "rating_asc":
            return movie.join(RatingKinopoisk).order_by(RatingKinopoisk.star.asc()) 
        
        if sorted == "rating_desc":
            return movie.join(RatingKinopoisk).order_by(RatingKinopoisk.star.desc()) 
        
        if sorted == "release_date_asc":
            if session.get('is_active_years'):
                return movie.order_by(Reliase.year.asc())
            return movie.join(Reliase).order_by(Reliase.year.asc())
        
        if sorted == "release_date_desc":
            if session.get('is_active_years'):
                return movie.order_by(Reliase.year.desc())
            return movie.join(Reliase).order_by(Reliase.year.desc())
        
        if sorted == "standart":
            return movie.order_by(Movie.id.desc())
        
        return movie
