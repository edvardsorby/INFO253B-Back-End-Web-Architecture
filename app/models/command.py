from db import db

class CommandModel(db.Model):
  __tablename__ = "commands"
  command = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
  url = db.Column(db.String(80), unique=True, nullable=False)