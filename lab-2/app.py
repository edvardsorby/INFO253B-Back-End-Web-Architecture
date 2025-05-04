import json
from flask import Flask, request, jsonify
app = Flask(__name__)

song_library = None

with open('library.json', 'r') as file:
  song_library = json.load(file)

@app.route('/songs')
def songs():
 return jsonify({"result": song_library}), 200

@app.post("/songs")
def add_song():
 
  request_data = request.get_json()

  if request_data:

    for song in song_library:
      if song["title"] == request_data["title"] and song["artist"] == request_data["artist"]:
        return jsonify({'message': 'Song already exists'}), 403

    new_song = {
      "id": len(song_library)+1,
      "title": request_data["title"],
      "artist": request_data["artist"],
      "genre": request_data["genre"],
      "year": request_data["year"]
    }

    song_library.append(new_song)

    with open("library.json", "w") as outfile:
      json.dump(song_library, outfile, indent=2)

    return jsonify({'message': 'Song added', 'song': new_song}), 201
  else:
    return jsonify({'message': 'No data received'}), 400
 
@app.put("/songs")
def edit_song():
 
 request_data = request.get_json()

 if request_data:

  for song in song_library:
    if song["id"] == request_data["id"]:
      song["title"] = request_data["title"]
      song["artist"] = request_data["artist"]
      song["genre"] = request_data["genre"]
      song["year"] = request_data["year"]

      with open("library.json", "w") as outfile:
        json.dump(song_library, outfile, indent=2)

      return jsonify({'message': 'Song updated', 'song': request_data}), 200
  return jsonify({'message': 'Song does not exist'}), 403
 else:
  return jsonify({'message': 'No data received'}), 400
 
@app.delete("/songs/<id>")
def remove_song(id):
 
  for song in song_library:
    if song["id"] == int(id):
      song_library.remove(song)
      with open("library.json", "w") as outfile:
        json.dump(song_library, outfile, indent=2)
      return jsonify({'message': 'Song deleted'}, 200)

  return jsonify({'message': 'No data received'}), 400