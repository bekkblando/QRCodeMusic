"""
Example on how to use the Spotify Controller.
NOTE: You need to install the spotipy and spotify-token dependencies.

This can be done by running the following:
pip install spotify-token
pip install git+https://github.com/plamere/spotipy.git
"""
import argparse
import http.client as http_client
import logging
import time
import sys

import pychromecast
from pychromecast.controllers.spotify import SpotifyController
import spotify_token as st
import spotipy

CAST_NAME = "Sadie's TV"

parser = argparse.ArgumentParser(
    description="Example on how to use the Spotify Controller.")
parser.add_argument('--show-debug', help='Enable debug log',
                    action='store_true')
parser.add_argument('--cast',
                    help='Name of cast device (default: "%(default)s")',
                    default=CAST_NAME)
parser.add_argument('--user', help='Spotify username', required=True)
parser.add_argument('--password', help='Spotify password', required=True)
parser.add_argument('--uri', help='Spotify uri(s) (default: "%(default)s")',
                    default=["spotify:track:3Zwu2K0Qa5sT6teCCHPShP"],
                    nargs='+')
args = parser.parse_args()

if args.show_debug:
    logging.basicConfig(level=logging.DEBUG)
    # Uncomment to enable http.client debug log
    #http_client.HTTPConnection.debuglevel = 1

chromecasts = pychromecast.get_chromecasts()
cast = None
for _cast in chromecasts:
    if _cast.name == args.cast:
        cast = _cast
        break

if not cast:
    print('No chromecast with name "{}" discovered'.format(args.cast))
    print('Discovered casts: {}'.format(chromecasts))
    sys.exit(1)

print('cast {}'.format(cast))

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

# Wait for connection to the chromecast
cast.wait()

spotify_device_id = None

# Create a spotify token
data = st.start_session(args.user, args.password)
access_token = data[0]
expires = data[1] - int(time.time())

# Create a spotify client
client = spotipy.Spotify(auth=access_token)
if args.show_debug:
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
if args.uri[0].find('track') > 0:
    client.start_playback(device_id=spotify_device_id, uris=args.uri)
else:
    client.start_playback(device_id=spotify_device_id, context_uri=args.uri[0])
