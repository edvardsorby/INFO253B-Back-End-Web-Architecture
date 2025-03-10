from flask import Flask, request, jsonify
app = Flask(__name__)

@app.post('/chat')
def chat():
  chat_request = request.get_json()

  if chat_request:

    message = chat_request["chat"]
    
    chat_response = {
      "chat": f"{message}¯\_(ツ)_/¯"
    }
    
    return jsonify(chat_response), 201
  else:
    return jsonify({'message': 'No data received'})