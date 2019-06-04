from flask import Flask, request, redirect
import subprocess
import os
from play_spotify import play_spotify

# spotify:track:2Iq6HhIquO7JKr0KfTNLzU

app = Flask(__name__)

@app.route('/music')
def music():
    spotify_uri = request.args.get('uri')
    # Play the music
    play_spotify("Rafael09ED", os.environ['SPOTIFY_PASS'], spotify_uri, False, "Sadie's TV", )
    spotify, media_type, id = spotify_uri.split(":")
    return redirect("https://open.spotify.com/{media_type}/{id}".format(media_type=media_type, id = id), code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
