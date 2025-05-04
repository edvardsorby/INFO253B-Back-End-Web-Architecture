from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from db import db
from schemas import FlightSchema
from models import FlightModel
from flask import request

# blue print divides data into multiple segments
blp = Blueprint("flights", __name__, description="Flights APIs")

@blp.route("/flight/<string:flight_id>")
class Flight(MethodView):
  @blp.response(200, FlightSchema)
  def get(self, flight_id):
    flight = FlightModel.query.get_or_404(flight_id)
    return flight
  
  def delete(self, flight_id):
    flight = FlightModel.query.get_or_404(flight_id)
    db.session.delete(flight)
    db.session.commit()
    return {"message": f"deleted flight with id {flight_id}"}

@blp.route("/flight")
class FlightList(MethodView):
  
  @blp.arguments(FlightSchema)
  @blp.response(200, FlightSchema)
  def post(self, flight_data):
    # uniqueness of name and flight already checked in the models, so we dont have to check here.
    flight = FlightModel(**flight_data) # converts dictionary to keyword arguments

    # save it to db
    try:
      db.session.add(flight)
      db.session.commit()
    except SQLAlchemyError as e:
      print(e)
      abort(500, message="Error occured while inserting flight")
    
    return flight, 201
  
@blp.route("/flights")
class FlightSearch(MethodView):

  @blp.response(200, FlightSchema(many=True))
  def get(self):
    source = request.args.get('source')
    destination = request.args.get('destination')
    date = request.args.get('date')
    
    flights = FlightModel.query.filter_by(source=source, destination=destination).all()
    
    if date:
      for flight in flights:
        if flight.departure_time[:10] != date or flight.arrival_time[:10] != date:
          flights.remove(flight)

    return flights