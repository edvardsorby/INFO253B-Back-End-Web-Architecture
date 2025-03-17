from flask import Flask, request, jsonify
from urllib.parse import urljoin
import requests
app = Flask(__name__)

command_db = {
  "shrug": "http://localhost:5001",
  "command_2": "server_url_2",
  "command_3": "server_url_3"
}

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

      print(command)
      print(message)
    
      if command == "admin":
        parts = message.split(" ")
        operation = parts[0]
        print(operation)
        if operation == "add":
          server_name = parts[1]
          server_url = parts[2]
          command_db[server_name] = server_url
          return "", 201
        elif operation == "update":
          server_name = parts[1]
          server_url = parts[2]
          command_db[server_name] = server_url
          return "", 200
        elif operation == "list":
          return {"command_db": command_db}, 200
        elif operation == "delete":
          server_name = parts[1]
          command_db.pop(server_name)
          return "", 204
      elif command in command_db:

        return send_chat(command_db[command], message)

      else:
        return f"The command {command} is not registered.", 404


    chat_response = {
      "chat": f"{command}: {message}"
    }
    
    return jsonify(chat_response), 201
  else:
    return jsonify({'message': 'No data received'}), 400
  

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