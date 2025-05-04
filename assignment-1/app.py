from flask import Flask, request, jsonify
app = Flask(__name__)

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
    
    chat_response = {
      "chat": f"{command}: {message}"
    }
    
    return jsonify(chat_response), 201
  else:
    return jsonify({'message': 'No data received'}), 400