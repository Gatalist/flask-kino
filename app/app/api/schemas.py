from marshmallow import Schema, fields


class MoviesSchema(Schema):
    id = fields.Integer(dump_only=True)
    title = fields.String()
    description = fields.String()
    poster = fields.String()
    reliase = fields.Integer()
    director = fields.String()
    rating = fields.Float()
    genres = fields.List(fields.String(required=True))
