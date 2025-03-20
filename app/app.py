import os
from flask import Flask, request, jsonify
from urllib.parse import urljoin
import requests
from models.command import CommandModel
from db import db
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

def create_app(db_url = None):
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
     
    return app

app = create_app()

@app.post('/chat')
def chat():
    request_data = request.get_json()

    if request_data:

        chat = request_data["chat"]
        command = None
        message = chat
        
        if chat[0] == "/":
            parts = chat[1:].split(" ", 1)
            command = parts[0]
            message = parts[1]
            
            if command == "admin":
                parts = message.split(" ")
                operation = parts[0]
                if operation == "add":
                    server_name = parts[1]
                    server_url = parts[2]
                    
                    return insert(CommandModel(command=server_name, server_url=server_url))

                elif operation == "update":
                    server_name = parts[1]
                    server_url = parts[2]

                    return update(server_name, server_url)
                elif operation == "list":
                    return get()
                elif operation == "delete":
                    server_name = parts[1]
                    return delete(server_name) 
                else:
                    return {"chat": f"Invalid admin command '{operation}'"}, 200                   
            else:
                registered_command = CommandModel.query.get(command)
                if registered_command:
                    return send_chat(registered_command.server_url, message)
                else:
                    return {"chat": f"The command {command} is not registered."}, 200
        else:
            return {"chat": f"Missing '/'"}, 200
    else:
        return {'chat': 'No data received'}, 400
  
def insert(command):
    try:
        db.session.add(command)
        db.session.commit()
        return {"chat": ""}, 201
    except IntegrityError:
        return {"chat": "Command or url already exists"}, 400
    except SQLAlchemyError:
        return {"chat": "An error occurred while inserting the command"}, 500
    
def get():
    commands = CommandModel.query.all()
    command_list = ""
    for command in commands:
        command_list += f"\n/{command.command} -> {command.server_url}"
    return {"chat": command_list}, 200

def delete(command_name):
    command = CommandModel.query.get_or_404(command_name)
    db.session.delete(command)
    db.session.commit()
    return {"chat": ""}, 200

def update(server_name, new_url):
    command = CommandModel.query.get(server_name)
    if command:
        command.server_url = new_url
    try:
        db.session.add(command)
        db.session.commit()
        return {"chat": ""}, 200
    except SQLAlchemyError:
        return {"chat": "Error occured while updating command"}, 500


def send_chat(server_url, chat):
    full_url = urljoin(server_url, "/chat")

    chat_request = {"chat": chat } 
    
    try: 
        r = requests.post(full_url, json=chat_request)
        r.raise_for_status()
    except requests.exceptions.ConnectionError as err:
        # eg, no internet
        raise SystemExit(err)
    except requests.exceptions.HTTPError as err:
        # eg, url, server and other errors
        raise SystemExit(err)

    response_json = r.json()

    return response_json