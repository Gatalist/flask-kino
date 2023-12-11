from app import db
from app.users.models import User
from datetime import datetime



genre_movie = db.Table(
    'genre_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('genre_id', db.Integer, db.ForeignKey('genre.id'))
)

country_movie = db.Table(
    'country_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('country_id', db.Integer, db.ForeignKey('country.id'))
)

director_movie = db.Table(
    'director_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('director_id', db.Integer, db.ForeignKey('director.id'))
)

creator_movie = db.Table(
    'creator_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('creator_id', db.Integer, db.ForeignKey('creator.id'))
)

actor_movie = db.Table(
    'actor_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id'))
)

screenshot_movie = db.Table(
    'screenshot_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('screenshot_id', db.Integer, db.ForeignKey('screenshot.id'))
)

similars_movie = db.Table(
    'similars_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('similars_id', db.Integer, db.ForeignKey('similars.id'))
)

user_movie = db.Table(
    'user_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('users_id', db.Integer, db.ForeignKey('users.id'))
)

trailer_movie = db.Table(
    'trailer_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('trailer_id', db.Integer, db.ForeignKey('trailer.id'))
)

tag_actor = db.Table(
    'tag_actor',
    db.Column('actor_id', db.Integer, db.ForeignKey('actor.id')),
    db.Column('tagactor_id', db.Integer, db.ForeignKey('tagactor.id'))
)

segment_movie = db.Table(
    'segment_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movie.id')),
    db.Column('segment_id', db.Integer, db.ForeignKey('segment.id'))
)



class Movie(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kinopoisk_id = db.Column(db.Integer, nullable=True, info={'label': 'Кинопоиск ID'})
    imdb_id = db.Column(db.String(12), nullable=True)

    name_ru = db.Column(db.String(256), nullable=True)
    name_original = db.Column(db.String(256), nullable=True)

    poster_url = db.Column(db.String(256),  nullable=True)
    slug = db.Column(db.String(256), nullable=True)

    rating_kinopoisk_id = db.Column(db.Integer, db.ForeignKey('ratingkinopoisk.id', ondelete='SET NULL'))
    rating_kinopoisk = db.relationship('RatingKinopoisk', backref=db.backref('movie'), passive_deletes=True)

    rating_imdb_id = db.Column(db.Integer, db.ForeignKey('ratingimdb.id', ondelete='SET NULL'))
    rating_imdb = db.relationship('RatingImdb', backref=db.backref('movie'), passive_deletes=True)

    rating_critics_id = db.Column(db.Integer, db.ForeignKey('ratingfilmcritics.id', ondelete='SET NULL'))
    rating_critics = db.relationship('RatingFilmCritics', backref=db.backref('movie'), passive_deletes=True)
    
    year_id = db.Column(db.Integer, db.ForeignKey('reliase.id', ondelete='SET NULL'))
    year = db.relationship('Reliase', backref=db.backref('movie'), passive_deletes=True)

    film_length_id = db.Column(db.Integer, db.ForeignKey('filmlength.id', ondelete='SET NULL'))
    film_length = db.relationship('FilmLength', backref=db.backref('movie'), passive_deletes=True)

    slogan = db.Column(db.String(512), nullable=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.Text, nullable=True)

    type_video_id = db.Column(db.Integer, db.ForeignKey('typevideo.id', ondelete='SET NULL'))
    type_video = db.relationship('TypeVideo', backref=db.backref('movie'), passive_deletes=False)
    
    age_limits_id = db.Column(db.Integer, db.ForeignKey('agelimit.id', ondelete='SET NULL'))
    age_limits = db.relationship('AgeLimit', backref=db.backref('movie'), passive_deletes=False)

    last_syncs = db.Column(db.DateTime, nullable=True)

    segment_id = db.Column(db.Integer, db.ForeignKey('segment.id', ondelete='SET NULL'))
    segment = db.relationship('Segment', secondary=segment_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)
    
    countries_id = db.Column(db.Integer, db.ForeignKey('country.id', ondelete='SET NULL'))
    countries = db.relationship('Country', secondary=country_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    genres_id = db.Column(db.Integer, db.ForeignKey('genre.id', ondelete='SET NULL'))
    genres = db.relationship('Genre', secondary=genre_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    director_id = db.Column(db.Integer, db.ForeignKey('director.id', ondelete='SET NULL'))
    director = db.relationship('Director', secondary=director_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)
    
    creator_id = db.Column(db.Integer, db.ForeignKey('creator.id', ondelete='SET NULL',))
    creator = db.relationship('Creator', secondary=creator_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    actor_id = db.Column(db.Integer, db.ForeignKey('actor.id', ondelete='SET NULL'))
    actor = db.relationship('Actor', secondary=actor_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    screen_img_id = db.Column(db.Integer, db.ForeignKey('screenshot.id', ondelete='CASCADE'))
    screen_img = db.relationship('Screenshot', secondary=screenshot_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    similar_id = db.Column(db.Integer, db.ForeignKey('similars.id', ondelete='SET NULL'))
    similar = db.relationship('Similars', secondary=similars_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    trailer_id = db.Column(db.Integer, db.ForeignKey('trailer.id', ondelete='SET NULL'))
    trailer = db.relationship('Trailer', secondary=trailer_movie, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    user = db.relationship('User', backref=db.backref('movie'), passive_deletes=False)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name_ru}'
    
    @property
    def last_syncs_format(self):
        return str(self.last_syncs).split()[0]

    
    @property
    def first_trailer(self):
        first = [tr for tr in self.trailer]
        if first:
            print(first)
            return first[0]
        return ''
    
    @property
    def star_rating_kinopoisk(self):
        max_rating = 10
        curent_rating = self.rating_kinopoisk

        list_star = []
        
        if not curent_rating:
            list_minus = ['star_m' for star in range(10)]
            list_star.extend(list_minus)
            return list_star

        plus = int(curent_rating.star)
        list_plus = ['star_p' for star in range(plus)]
        list_star.extend(list_plus)

        center = 0
        list_center = []
        if curent_rating.star - plus > 0.45:
            list_center.append('star_c')
            center = 1
        list_star.extend(list_center)

        minus = max_rating - (plus + center)
        list_minus = ['star_m' for star in range(minus)]
        list_star.extend(list_minus)
        return list_star

    def mod_list_to_str(self, list_obj):
        # убираем с имени знак ',' с последнего елемента списка
        if list_obj:
            list_name = [f'{name},' for name in list_obj]
            last = list_name[-1].replace(',', '')
            list_name.pop()
            list_name.append(last)
            return list_name
        return list_obj

    @property
    def mod_genres(self):
        return self.mod_list_to_str(self.genres)
    
    @property
    def mod_creators(self):
        return self.mod_list_to_str(self.creator)
    
    @property
    def mod_directors(self):
        return self.mod_list_to_str(self.director)
    
    @property
    def mod_actors(self):
        return self.mod_list_to_str(self.actor)
    
    @property
    def mod_countries(self):
        return self.mod_list_to_str(self.countries)
    
    @property
    def get_similar_movie(self):
        similar_values = [sim.kinopoisk_id for sim in self.similar]
        print('list_sim:', similar_values)
        filtered_movies = Movie.query.filter(Movie.kinopoisk_id.in_(similar_values)).all()

        print('movie', filtered_movies)
        return filtered_movies


class RatingKinopoisk(db.Model):
    __tablename__ = 'ratingkinopoisk'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    star = db.Column(db.Float)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.star}'


class RatingImdb(db.Model):
    __tablename__ = 'ratingimdb'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    star = db.Column(db.Float)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
   
    def __repr__(self):
        return f'{self.star}'


class RatingFilmCritics(db.Model):
    __tablename__ = 'ratingfilmcritics'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    star = db.Column(db.Float)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
  
    def __repr__(self):
        return f'{self.star}'
        

class Reliase(db.Model):
    __tablename__ = 'reliase'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    year = db.Column(db.Integer)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
 
    def __repr__(self):
        return f'{self.year}'


class FilmLength(db.Model):
    __tablename__ = 'filmlength'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    length = db.Column(db.Integer)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
 
    def __repr__(self):
        return f'{self.length}'


class AgeLimit(db.Model):
    __tablename__ = 'agelimit'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'


class TypeVideo(db.Model):
    __tablename__ = 'typevideo'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)
 
    def __repr__(self):
        return f'{self.name}'


class Genre(db.Model):
    __tablename__ = 'genre'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'


class Country(db.Model):
    __tablename__ = 'country'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'


class Director(db.Model):
    __tablename__ = 'director'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'


class Creator(db.Model):
    __tablename__ = 'creator'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'
    

class Actor(db.Model):
    __tablename__ = 'actor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True, unique=True)

    tag_id = db.Column(db.Integer, db.ForeignKey('tagactor.id', ondelete='SET NULL'))
    tag = db.relationship('TagActor', secondary=tag_actor, backref=db.backref('movie', lazy='dynamic'), passive_deletes=False)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'


class Screenshot(db.Model):
    __tablename__ = 'screenshot'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kinopoisk_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(256), index=True)
    url = db.Column(db.String(256), index=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.url}'


class Similars(db.Model):
    __tablename__ = 'similars'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    kinopoisk_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(256), nullable=True, index=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.kinopoisk_id}| {self.name}'


class Trailer(db.Model):
    __tablename__ = 'trailer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(256), index=True)
    type = db.Column(db.String(8), index=True)
    url = db.Column(db.String(1024), index=True)
    background = db.Column(db.String(256), index=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'


class TagActor(db.Model):
    __tablename__ = 'tagactor'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'


class Segment(db.Model):
    __tablename__ = 'segment'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(64), index=True)

    created_on = db.Column(db.DateTime(), default=datetime.utcnow)
    updated_on = db.Column(db.DateTime(), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'{self.name}'
