from flask import Flask
import subprocess
import os

app = Flask(__name__)

@app.route('/play')
def play():
    spotify_uri = request.args.get('uri')
    # Play the music
    subprocess.run(["python3", "/home/pi/Documents/QRCodeMusic/spotify_example.py", "--user", "rafeal09ED", "--password", os.environ['SPOTIFY_PASS']])
    return redirect('google.com', code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')