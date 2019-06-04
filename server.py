from flask import Flask

app = Flask(__name__)

@app.route('/play')
def play():
    spotify_uri = request.args.get('uri')
    # Play the music
    return redirect('google.com', code=302)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')