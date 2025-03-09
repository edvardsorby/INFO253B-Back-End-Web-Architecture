from marshmallow import Schema, fields

# Flight Schema without the Airline information
class PlainFlightSchema(Schema):
  id = fields.Int(dump_only=True)
  source = fields.Str(required=True)
  destination = fields.Str(required=True)
  departure_time = fields.Str(required=True)
  arrival_time = fields.Str(required=True)

class PlainAirlineSchema(Schema):
  id = fields.Int(dump_only=True)
  airline_name = fields.Str(required=True)

# define the schema
class FlightSchema(PlainFlightSchema):
  airline_id = fields.Int(required=True, load_only = True)
  airline = fields.Nested(PlainAirlineSchema(), dump_only = True)

class AirlineSchema(PlainAirlineSchema):
  flights = fields.List(fields.Nested(PlainFlightSchema()), dump_only = True)