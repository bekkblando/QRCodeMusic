from flask import Flask
from flask import request
import subprocess
import os

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

@app.route('/play')
def play():
    spotify_uri = request.args.get('uri')
    # Play the music
    run(["python3", "/home/pi/Documents/QRCodeMusic/spotify_example.py", "--user", "rafeal09ED", "--password", os.environ['SPOTIFY_PASS']])
    return redirect('google.com', code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
