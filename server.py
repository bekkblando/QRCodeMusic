from flask import Flask, request, redirect
import subprocess
import os
from play_spotify import play_spotify
from play_youtube import play_youtube

# spotify:track:2Iq6HhIquO7JKr0KfTNLzU

application = Flask(__name__)

@application.route('/spotify')
def spotify():
    spotify_uri = request.args.get('uri')
    # Play the music
    play_spotify("Rafael09ED", os.environ['SPOTIFY_PASS'], [spotify_uri] )
    spotify, media_type, id = spotify_uri.split(":")
    return redirect("https://open.spotify.com/{media_type}/{id}".format(media_type=media_type, id = id), code=302)

@application.route('/youtube')
def youtube():
    video_id = request.args.get('id')
    # Play the video
    play_youtube("Sadie's TV", video_id )
    return redirect("https://youtube.com/watch?v={video_id}&autoplay=0".format(video_id = video_id), code=302)


if __name__ == '__main__':
    application.run(debug=True, host='0.0.0.0', threaded=True)
