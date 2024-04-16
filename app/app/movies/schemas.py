from marshmallow import Schema, fields


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class CountrySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class ReleaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    year = fields.Integer()


class TrailerSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()
    url = fields.String()


class MoviesSchema(Schema):
    id = fields.Integer(dump_only=True)
    kinopoisk_id = fields.Integer()
    imdb_id = fields.String()
    name_ru = fields.String()
    name_original = fields.String()
    poster_url = fields.String()
    slug = fields.String()
    rating_kinopoisk = fields.Float(attribute='rating_kinopoisk.star')
    rating_imdb = fields.Float(attribute='rating_imdb.star')
    rating_critics = fields.Float(attribute='rating_critics.star')
    year = fields.Integer(attribute='year.year')
    film_length = fields.Integer(attribute='film_length.length')
    slogan = fields.String()
    description = fields.String()
    short_description = fields.String()
    type_video = fields.String()
    age_limits = fields.Integer(attribute='age_limits.name')
    last_syncs = fields.DateTime(format='%Y-%m-%d %H:%M:%S')
    countries = fields.List(fields.String())
    genres = fields.List(fields.String())
    director = fields.List(fields.String())
    creator = fields.List(fields.String())
    actor = fields.List(fields.String())
    screen_img = fields.List(fields.String())
