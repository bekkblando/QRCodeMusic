import pychromecast
from pychromecast.controllers.youtube import YouTubeController


# Give the name of your Chromecast
def play_youtube(cast_name, video_id):
    # Change to the video id of the YouTube video
    # video id is the last part of the url http://youtube.com/watch?v=video_id
    chromecasts = pychromecast.get_chromecasts()
    cast = next(cc for cc in chromecasts if cc.device.friendly_name == cast_name)
    cast.wait()
    yt = YouTubeController()
    cast.register_handler(yt)
    yt.play_video(video_id)