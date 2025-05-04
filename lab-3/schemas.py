from marshmallow import Schema, fields

class SongSchema(Schema):
  title = fields.Str(required=True)
  artist = fields.Str(required=True)
  year = fields.Int(required=True)
  genre = fields.Str(required=True)

class SongUpdateSchema(Schema):
  title = fields.Str()
  artist = fields.Str()
  year = fields.Int()
  genre = fields.Str()