from db import db

class AirlineModel(db.Model):
  __tablename__ = "airlines"

  id = db.Column(db.Integer, primary_key=True)
  airline_name = db.Column(db.String(80), unique=True, nullable=False)

  flights = db.relationship("FlightModel", back_populates="airline", lazy="dynamic")

