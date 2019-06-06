import pychromecast
from pychromecast.controllers.youtube import YouTubeController
from helper_functions import discover_casts, get_cast


# Give the name of your Chromecast
def play_youtube(cast, video_id):
    # Change to the video id of the YouTube video
    # video id is the last part of the url http://youtube.com/watch?v=video_id

    cast_ip = None
    with open('cast.txt', 'r+') as f:
        print("This is the file pointer", f)
        if len(f.read(1)) == 0:
            cast = discover_casts(cast)
        else:
            f.seek(0)
            cast_ip = [line for line in f][0]
            cast = get_cast(cast_ip, cast)
        
        if(cast.host != cast_ip):
            f.write(cast.host)

    cast.wait()
    yt = YouTubeController()
    cast.register_handler(yt)
    yt.play_video(video_id)