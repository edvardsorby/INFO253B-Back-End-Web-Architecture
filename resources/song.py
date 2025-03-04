import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import SongSchema, SongUpdateSchema

song_library = None

genres = ["Pop", "Rock", "Jazz", "Hip-Hop", "Pop-Punk", "EDM"]

with open('library.json', 'r') as file:
  song_library = json.load(file)

blp = Blueprint("songs", __name__, description="Songs APIs")

@blp.route("/songs")
class SongList(MethodView):

  @blp.response(200, SongSchema(many=True))
  def get(self):
    return song_library

  @blp.arguments(SongSchema)
  @blp.response(200, SongSchema)
  def post(self, song_data):
      
    for song in song_library:
      if song["title"] == song_data["title"] and song["artist"] == song_data["artist"]:
        abort(400, message="Song already exists")

    if song_data["year"] < 1900 or song_data["year"] > 2025:
      abort(400, message="Year must be between 1900 and 2025")

    if song_data["genre"].lower() not in (genre.lower() for genre in genres):
      abort(400, message=f"Genre must be either: {genres}")

    new_song = {
      "title": song_data["title"],
      "artist": song_data["artist"],
      "genre": song_data["genre"],
      "year": song_data["year"]
    }

    song_library.append(new_song)

    with open("library.json", "w") as outfile:
      json.dump(song_library, outfile, indent=2)

    return new_song, 201

# Corresponds with provided endpoints in the Lab description,
#  but is not able to uniquely identify a song without the use of
#  ID or artist. Finds first song with matching title instead.
@blp.route("/songs/<string:title>")
class Song(MethodView):

  def delete(self, title):
    for song in song_library:
      if song["title"] == title:
        song_library.remove(song)
        with open("library.json", "w") as outfile:
          json.dump(song_library, outfile, indent=2)
        return {"message": "Song deleted"}
    abort(400, message="Song does not exist")

  @blp.arguments(SongUpdateSchema)
  @blp.response(200, SongSchema)
  def put(self, song_data, title):

    if song_data["year"] < 1900 or song_data["year"] > 2025:
      abort(400, message="Year must be between 1900 and 2025")

    if song_data["genre"].lower() not in (genre.lower() for genre in genres):
      abort(400, message=f"Genre must be either: {genres}")

    updated_song = None

    for song in song_library:
      if song["title"] == title:
        song |= song_data
        updated_song = song

        with open("library.json", "w") as outfile:
          json.dump(song_library, outfile, indent=2)

        return updated_song
    abort(400, message="Song does not exist")