from flask.views import MethodView
from flask_smorest import Blueprint, abort
from db import db
from models import AirlineModel
from schemas import AirlineSchema, PlainAirlineSchema
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

# blue print divides data into multiple segments
blp = Blueprint("airlines", __name__, description="Airlines APIs")

@blp.route("/airline/<string:airline_id>")
class Airline(MethodView):
  @blp.response(200, PlainAirlineSchema)
  def get(self, airline_id):
    airline = AirlineModel.query.get_or_404(airline_id)
    return airline

@blp.route("/airline")
class AirlineList(MethodView):
  
  @blp.arguments(AirlineSchema)
  @blp.response(200, PlainAirlineSchema)
  def post(self, airline_data):
    new_airline = AirlineModel(**airline_data)
    try:
      db.session.add(new_airline)
      db.session.commit()
    except IntegrityError:
      abort(500, message="Airline with that name already exists")
    except SQLAlchemyError:
      abort(500, message="Error occured while inserting airline")
    
    return new_airline, 201
