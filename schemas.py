from marshmallow import Schema, fields

class SongSchema(Schema):
  id = fields.Int(dump_only=True)
  title = fields.Str(required=True)
  artist = fields.Str(required=True)
  year = fields.Int(required=True)
  genre = fields.Str(required=True)

class SongUpdateSchema(Schema):
  artist = fields.Str()
  year = fields.Int()
  genre = fields.Str()