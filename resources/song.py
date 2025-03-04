import json
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import SongSchema, SongUpdateSchema

song_library = None

genres = ["pop", "rock", "jazz", "hip-hop"]

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
      
    try:
      if song["year"] < 1900 or song["year"] > 2025:
        abort(403, message="Invalid year")

      if song["genre"] not in genres:
        abort(403, message="Invalid genre")

      for song in song_library:
        if song["title"] == song_data["title"] and song["artist"] == song_data["artist"]:
          abort(403, message="Song already exists")


      new_song = {
        "id": len(song_library)+1,
        "title": song_data["title"],
        "artist": song_data["artist"],
        "genre": song_data["genre"],
        "year": song_data["year"]
      }

      song_library.append(new_song)

      with open("library.json", "w") as outfile:
        json.dump(song_library, outfile, indent=2)

    except Exception:
        abort(500, message="Error adding song")
    return new_song, 201

# Corresponds with provided endpoints in the Lab description,
#  but is not able to uniquely identify a song without the use of
#  ID or artist. Finds first song with matching title instead.
@blp.route("/songs/<string:song_title>")
class Song(MethodView):

  def delete(self, song_title):
    for song in song_library:
      if song["title"] == song_title:
        song_library.remove(song)
        with open("library.json", "w") as outfile:
          json.dump(song_library, outfile, indent=2)
    return {"message": "Song deleted"}

  @blp.arguments(SongUpdateSchema)
  @blp.response(200, SongSchema)
  def put(self, song_data, song_title):

    updated_song = None

    for song in song_library:
      if song["title"] == song_title:
        song["artist"] = song_data["artist"]
        song["genre"] = song_data["genre"]
        song["year"] = song_data["year"]

        updated_song = song

        with open("library.json", "w") as outfile:
          json.dump(song_library, outfile, indent=2)

        return updated_song
    abort(403, message="Song does not exist")