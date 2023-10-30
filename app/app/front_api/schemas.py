from marshmallow import Schema, fields
from flask_paginate import Pagination


class MoviesSchema(Schema):
    id = fields.Integer(dump_only=True)
    kinopoisk_id = fields.Integer()
    imdb_id = fields.String()
    name_ru = fields.String()
    name_original = fields.String()
    poster_url = fields.String()
    slug = fields.String()
    rating_kinopoisk = fields.String()
    rating_imdb = fields.String()
    rating_critics = fields.String()
    year = fields.String()
    film_length = fields.String()
    slogan = fields.String()
    description = fields.String()
    short_description = fields.String()
    type_video = fields.String()
    age_limits = fields.String()
    last_syncs = fields.String()
    countries = fields.List(fields.String(required=True))
    genres = fields.List(fields.String(required=True))
    director = fields.List(fields.String(required=True))
    creator = fields.List(fields.String(required=True))
    actor = fields.List(fields.String(required=True))
    screen_img = fields.List(fields.String(required=True))
    similar = fields.List(fields.String(required=True))
    trailer = fields.String()


class GenreSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class CountrySchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()


class DirectorSchema(Schema):
    id = fields.Integer(dump_only=True)
    name = fields.String()

class ReliaseSchema(Schema):
    id = fields.Integer(dump_only=True)
    year = fields.String()


class PaginationSchema(Pagination):
    page = fields.Integer(description='The current page number'),
    per_page = fields.Integer(description='Number of items per page'),
    total = fields.Integer(description='Total number of items'),
    pages = fields.Integer(description='Total number of pages')
