from flask import Flask, request, redirect
import subprocess
import os

# spotify:track:2Iq6HhIquO7JKr0KfTNLzU

app = Flask(__name__)

def run(*popenargs, input=None, check=False, **kwargs):
    if input is not None:
        if 'stdin' in kwargs:
            raise ValueError('stdin and input arguments may not both be used.')
        kwargs['stdin'] = subprocess.PIPE

    process = subprocess.Popen(*popenargs, **kwargs)
    try:
        stdout, stderr = process.communicate(input)
    except:
        process.kill()
        process.wait()
        raise
    retcode = process.poll()
    if check and retcode:
        raise subprocess.CalledProcessError(
            retcode, process.args, output=stdout, stderr=stderr)
    return retcode, stdout, stderr

@app.route('/music')
def music():
    spotify_uri = request.args.get('uri')
    # Play the music
    print(run(["python3", "/home/pi/Documents/QRCodeMusic/spotify_example.py", "--user", "Rafael09ED", "--password", os.environ['SPOTIFY_PASS'], "--uri", spotify_uri]))
    media_type, id = spotify_uri.split(":")
    return redirect("https://open.spotify.com/{media_type}/{id}".format(media_type=media_type, id = id), code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
