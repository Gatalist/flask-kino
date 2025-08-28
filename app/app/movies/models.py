from app import db
from datetime import datetime, timezone
from app.users.models import User


genre_movie = db.Table(
    'genre_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete="SET NULL"), primary_key=True, index=True)
)

country_movie = db.Table(
    'country_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('country_id', db.Integer, db.ForeignKey('countries.id', ondelete="SET NULL"), primary_key=True, index=True),
)

director_movie = db.Table(
    'director_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('persons_id', db.Integer, db.ForeignKey('persons.id', ondelete="SET NULL"), primary_key=True, index=True),
)

creator_movie = db.Table(
    'creator_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('persons_id', db.Integer, db.ForeignKey('persons.id', ondelete="SET NULL"), primary_key=True, index=True),
)

actor_movie = db.Table(
    'actor_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('persons_id', db.Integer, db.ForeignKey('persons.id', ondelete="SET NULL"), primary_key=True, index=True),
)

screenshot_movie = db.Table(
    'screenshot_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="CASCADE"), primary_key=True, index=True),
    db.Column('screenshot_id', db.Integer, db.ForeignKey('screenshots.id', ondelete="CASCADE"), primary_key=True, index=True),
)

similar_movie = db.Table(
    'similar_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('similar_id', db.Integer, db.ForeignKey('similars.id', ondelete="SET NULL"), primary_key=True, index=True),
)

user_movie = db.Table(
    'user_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('user_id', db.Integer, db.ForeignKey('users.id', ondelete="SET NULL"), primary_key=True, index=True),
)

segment_movie = db.Table(
    'segment_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('segment_id', db.Integer, db.ForeignKey('segments.id', ondelete="SET NULL"), primary_key=True, index=True),
)

tag_person = db.Table(
    'tag_person',
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('person_id', db.Integer, db.ForeignKey('persons.id', ondelete="SET NULL"), primary_key=True, index=True),
)

video_movie = db.Table(
    'video_movie',
    db.Column('movie_id', db.Integer, db.ForeignKey('movies.id', ondelete="SET NULL"), primary_key=True, index=True),
    db.Column('video_id', db.Integer, db.ForeignKey('videos.id', ondelete="SET NULL"), primary_key=True, index=True),
)


class BaseModel(db.Model):
    __abstract__ = True
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    publish = db.Column(db.Boolean, default=True)
    sorting = db.Column(db.Integer, default=100)
    created_on = db.Column(db.DateTime(), default=lambda: datetime.now(timezone.utc))
    updated_on = db.Column(
        db.DateTime(),
        default=datetime.now(timezone.utc),
        onupdate=datetime.now(timezone.utc)
    )


class Movie(BaseModel):
    __tablename__ = 'movies'

    kinopoisk_id = db.Column(db.Integer, nullable=True, info={'label': 'Кинопоиск ID'})
    kinopoisk_hd_id = db.Column(db.String(50), nullable=True, info={'label': 'kinopoisk HD Id'})
    imdb_id = db.Column(db.String(12), nullable=True)

    editor_annotation = db.Column(db.String(512), nullable=True)
    is_tickets_available = db.Column(db.Boolean, default=False)

    production_status_id = db.Column(db.Integer, db.ForeignKey('production_status.id', ondelete='SET NULL'))
    production_status = db.relationship('ProductionStatus', backref=db.backref('movie'), passive_deletes=True)

    name_ru = db.Column(db.String(256), nullable=True, info={'label': 'Название ru'})
    name_en = db.Column(db.String(256), nullable=True, info={'label': 'Название en'})
    name_uk = db.Column(db.String(256), nullable=True, info={'label': 'Название uk'})
    name_original = db.Column(db.String(256), nullable=True, info={'label': 'Название оригинал'})

    poster_url = db.Column(db.String(256), nullable=True)
    slug = db.Column(db.String(256), nullable=True)

    reviews_count = db.Column(db.Integer, nullable=True)

    rating_mpaa_id = db.Column(db.Integer, db.ForeignKey('rating_mpaa.id', ondelete='SET NULL'))
    rating_mpaa = db.relationship('RatingMPAA', lazy='selectin', passive_deletes=True)

    rating_good_review = db.Column(db.Float, nullable=True)
    rating_good_review_vote_count = db.Column(db.Integer, nullable=True)

    trailer = db.relationship('Video', secondary=video_movie, lazy='selectin', passive_deletes=True)

    rating_kinopoisk_id = db.Column(db.Integer, db.ForeignKey('rating.id', ondelete='SET NULL'))
    rating_kinopoisk = db.relationship(
        'Rating', foreign_keys=[rating_kinopoisk_id], passive_deletes=True,
        overlaps="rating_imdb_id,rating_critics_id"
    )

    rating_kinopoisk_vote_count = db.Column(db.Integer, nullable=True)

    rating_imdb_id = db.Column(db.Integer, db.ForeignKey('rating.id', ondelete='SET NULL'))
    rating_imdb = db.relationship(
        'Rating', foreign_keys=[rating_imdb_id], passive_deletes=True,
        overlaps="rating_kinopoisk_id,rating_critics_id"
    )

    rating_imdb_vote_count = db.Column(db.Integer, nullable=True)

    rating_critics_id = db.Column(db.Integer, db.ForeignKey('rating.id', ondelete='SET NULL'))
    rating_critics = db.relationship(
        'Rating', foreign_keys=[rating_critics_id], passive_deletes=True,
        overlaps="rating_kinopoisk_id,rating_imdb_id"
    )

    rating_critics_vote_count = db.Column(db.Integer, nullable=True, default=None)

    rating_await_id = db.Column(db.Integer, db.ForeignKey('rating_await.id', ondelete='SET NULL'))
    rating_await = db.relationship('RatingAwait', lazy='selectin', passive_deletes=True)

    rating_await_count = db.Column(db.Integer, nullable=True)

    year_id = db.Column(db.Integer, db.ForeignKey('releases.id', ondelete='SET NULL'))
    year = db.relationship(
        'Release', foreign_keys=[year_id], passive_deletes=True, overlaps="start_year,end_year"
    )

    start_year_id = db.Column(db.Integer, db.ForeignKey('releases.id', ondelete='SET NULL'))
    start_year = db.relationship(
        'Release', foreign_keys=[start_year_id], passive_deletes=True, overlaps="year,end_year"
    )

    end_year_id = db.Column(db.Integer, db.ForeignKey('releases.id', ondelete='SET NULL'))
    end_year = db.relationship(
        'Release', foreign_keys=[end_year_id], passive_deletes=True, overlaps="year,start_year"
    )

    film_length_id = db.Column(db.Integer, db.ForeignKey('film_length.id', ondelete='SET NULL'))
    film_length = db.relationship('FilmLength', lazy='selectin', passive_deletes=True)

    slogan = db.Column(db.Text, nullable=True)
    description = db.Column(db.Text, nullable=True)
    short_description = db.Column(db.Text, nullable=True)

    type_video_id = db.Column(db.Integer, db.ForeignKey('type_videos.id', ondelete='SET NULL'))
    type_video = db.relationship('TypeVideo', lazy='selectin', passive_deletes=True)

    age_limits_id = db.Column(db.Integer, db.ForeignKey('age_limits.id', ondelete='SET NULL'))
    age_limits = db.relationship('AgeLimit', lazy='selectin', passive_deletes=True)

    last_syncs = db.Column(db.DateTime, nullable=True)

    segment_id = db.Column(db.Integer, db.ForeignKey('segments.id', ondelete='SET NULL'))
    segment = db.relationship('Segment', secondary=segment_movie, lazy='selectin', passive_deletes=True)

    countries_id = db.Column(db.Integer, db.ForeignKey('countries.id', ondelete='SET NULL'))
    countries = db.relationship('Country', secondary=country_movie, lazy='selectin', passive_deletes=True)

    genres = db.relationship('Genre', secondary=genre_movie, lazy='selectin', passive_deletes=True)
    director = db.relationship('Person', secondary=director_movie, lazy='selectin', passive_deletes=True)
    creator = db.relationship('Person', secondary=creator_movie, lazy='selectin', passive_deletes=True)
    actor = db.relationship('Person', secondary=actor_movie, lazy='selectin', passive_deletes=True)
    screen_img = db.relationship('Screenshot', secondary=screenshot_movie, lazy='selectin', passive_deletes=True)
    similar = db.relationship('Similar', secondary=similar_movie, lazy='selectin', passive_deletes=True)

    has_3d = db.Column(db.Boolean, default=False)
    has_imax = db.Column(db.Boolean, default=False)
    short_film = db.Column(db.Boolean, default=False)

    serial = db.Column(db.Boolean, default=False)
    completed = db.Column(db.Boolean, default=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))
    user = db.relationship('User', lazy='selectin', passive_deletes=True)

    def __repr__(self):
        return f'{self.id} {self.name_ru}'

    @property
    def last_syncs_format(self):
        return str(self.last_syncs).split()[0]

    @property
    def star_rating_kinopoisk(self):
        max_rating = 10
        current_rating = self.rating_kinopoisk

        list_star = []

        if not current_rating:
            list_minus = ['star_m' for _ in range(10)]
            list_star.extend(list_minus)
            return list_star

        plus = int(current_rating.star)
        list_plus = ['star_p' for _ in range(plus)]
        list_star.extend(list_plus)

        center = 0
        list_center = []
        if current_rating.star - plus > 0.45:
            list_center.append('star_c')
            center = 1
        list_star.extend(list_center)

        minus = max_rating - (plus + center)
        list_minus = ['star_m' for _ in range(minus)]
        list_star.extend(list_minus)
        return list_star

    @staticmethod
    def mod_list_to_str(list_obj):
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

    @staticmethod
    def split_count_reviews(count_reviews: float | int):
        stringify = str(count_reviews)
        result = ''
        counter = 0
        if len(stringify) > 3:
            for char in stringify[::-1]:
                if counter % 3 == 0:
                    result += ' '
                result += char
                counter += 1
            return result[::-1]
        return stringify

    @property
    def rating_imdb_vote_count_format(self):
        return self.split_count_reviews(self.rating_imdb_vote_count)

    @property
    def rating_kinopoisk_vote_count_format(self):
        return self.split_count_reviews(self.rating_kinopoisk_vote_count)


class ProductionStatus(BaseModel):
    __tablename__ = 'production_status'
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Rating(BaseModel):
    __tablename__ = 'rating'
    star = db.Column(db.Float)

    def __repr__(self):
        return f'{self.star}'


class RatingAwait(BaseModel):
    __tablename__ = 'rating_await'
    star = db.Column(db.Float)

    def __repr__(self):
        return f'{self.star}'


class RatingMPAA(BaseModel):
    __tablename__ = 'rating_mpaa'
    star = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'{self.star}'


class Release(BaseModel):
    __tablename__ = 'releases'
    year = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.year}'


class FilmLength(BaseModel):
    __tablename__ = 'film_length'
    length = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.length}'


class AgeLimit(BaseModel):
    __tablename__ = 'age_limits'
    name = db.Column(db.Integer)

    def __repr__(self):
        return f'{self.name}'


class TypeVideo(BaseModel):
    __tablename__ = 'type_videos'
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Genre(BaseModel):
    __tablename__ = 'genres'
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Country(BaseModel):
    __tablename__ = 'countries'
    name = db.Column(db.String(64), index=True, unique=True)

    def __repr__(self):
        return f'{self.name}'


class Person(BaseModel):
    __tablename__ = 'persons'

    person_id = db.Column(db.Integer, nullable=True)
    name_ru = db.Column(db.String(64), index=True, nullable=True)
    name_en = db.Column(db.String(64), index=True, nullable=True)
    name_uk = db.Column(db.String(64), index=True, nullable=True)

    actor = db.Column(db.Boolean, default=False)
    director = db.Column(db.Boolean, default=False)
    creator = db.Column(db.Boolean, default=False)

    birthday = db.Column(db.DateTime(), nullable=True)
    death = db.Column(db.DateTime(), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    image_url = db.Column(db.String(256), index=True, nullable=True)
    description = db.Column(db.Text, nullable=True)

    tag = db.relationship(
        'Tag',
        secondary=tag_person,
        lazy='selectin',
        passive_deletes=True
    )

    def __repr__(self):
        if self.name_ru:
            return f'{self.name_ru}'
        else:
            return f'{self.name_en}'

class Screenshot(BaseModel):
    __tablename__ = 'screenshots'
    kinopoisk_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(256), index=True)
    url = db.Column(db.String(256), index=True)

    def __repr__(self):
        return f'{self.name}'


class Similar(BaseModel):
    __tablename__ = 'similars'
    kinopoisk_id = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(256), nullable=True, index=True)

    def __repr__(self):
        return f'{self.name}'


class Tag(BaseModel):
    __tablename__ = 'tags'
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f'{self.name}'


class Segment(BaseModel):
    __tablename__ = 'segments'
    name = db.Column(db.String(64), index=True)
    activate = db.Column(db.DateTime(), nullable=True)
    deactivate = db.Column(db.DateTime(), nullable=True)

    def __repr__(self):
        return f'{self.name}'


class Video(BaseModel):
    __tablename__ = 'videos'
    name = db.Column(db.String(64), index=True)
    url = db.Column(db.String(128), index=True)
    source_id = db.Column(db.Integer, db.ForeignKey('video_sources.id', ondelete='SET NULL'))
    source = db.relationship('VideoSource', lazy='selectin', passive_deletes=True)

    def __repr__(self):
        return f'{self.name}'


class VideoSource(BaseModel):
    __tablename__ = 'video_sources'
    name = db.Column(db.String(64), index=True)

    def __repr__(self):
        return f'{self.name}'
