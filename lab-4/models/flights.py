from db import db

class FlightModel(db.Model):
  __tablename__ = "flights"

  id = db.Column(db.Integer, primary_key=True)
  source = db.Column(db.String(80), unique=False, nullable=False)
  destination = db.Column(db.String(80), unique=False, nullable=False)
  departure_time = db.Column(db.String(19), unique=False, nullable=False)
  arrival_time = db.Column(db.String(19), unique=False, nullable=False)
  
  airline_id = db.Column(db.Integer, db.ForeignKey("airlines.id"), unique=False, nullable=False)
  airline = db.relationship("AirlineModel", back_populates="flights")