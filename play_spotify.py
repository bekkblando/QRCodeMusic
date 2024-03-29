"""
Example on how to use the Spotify Controller.
NOTE: You need to install the spotipy and spotify-token dependencies.

This can be done by running the following:
pip install spotify-token
pip install git+https://github.com/plamere/spotipy.git
"""
import http.client as http_client
import logging
import time
import sys

import pychromecast
from pychromecast.controllers.spotify import SpotifyController
import spotify_token as st
import spotipy
from helper_functions import discover_casts, get_cast

CAST_NAME = "Sadie's TV"


class ConnListener:
    def __init__(self, mz):
        self._mz=mz

    def new_connection_status(self, connection_status):
        """Handle reception of a new ConnectionStatus."""
        if connection_status.status == 'CONNECTED':
            self._mz.update_members()

class MzListener:
    def __init__(self):
        self.got_members=False
    
    def multizone_member_added(self, uuid):
        pass

    def multizone_member_removed(self, uuid):
        pass

    def multizone_status_received(self):
        self.got_members=True


# Main Function
def play_spotify(user, password, uri = ["spotify:track:3Zwu2K0Qa5sT6teCCHPShP"], show_debug = False, cast = "Sadie's TV"):
    if show_debug:
        logging.basicConfig(level=logging.DEBUG)
        # Uncomment to enable http.client debug log
        #http_client.HTTPConnection.debuglevel = 1

    # Store the ip in a txt file
    # Open File
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

    # Wait for connection to the chromecast
    cast.wait()

    spotify_device_id = None

    # Create a spotify token
    data = st.start_session(user, password)
    access_token = data[0]
    expires = data[1] - int(time.time())

    # Create a spotify client
    client = spotipy.Spotify(auth=access_token)
    if show_debug:
        spotipy.trace = True
        spotipy.trace_out = True

    # Launch the spotify app on the cast we want to cast to
    sp = SpotifyController(access_token, expires)
    cast.register_handler(sp)
    sp.launch_app()

    if not sp.is_launched and not sp.credential_error:
        print('Failed to launch spotify controller due to timeout')
        sys.exit(1)
    if not sp.is_launched and sp.credential_error:
        print('Failed to launch spotify controller due to credential error')
        sys.exit(1)

    # Query spotify for active devices
    devices_available = client.devices()

    # Match active spotify devices with the spotify controller's device id
    for device in devices_available['devices']:
        if device['id'] == sp.device:
            spotify_device_id = device['id']
            break

    if not spotify_device_id:
        print('No device with id "{}" known by Spotify'.format(sp.device))
        print('Known devices: {}'.format(devices_available['devices']))
        sys.exit(1)

    # Start playback
    if uri[0].find('track') > 0:
        client.start_playback(device_id=spotify_device_id, uris=uri)
    else:
        client.start_playback(device_id=spotify_device_id, context_uri=uri[0])
