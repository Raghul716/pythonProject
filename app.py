from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from spotipy.oauth2 import SpotifyOAuth
import spotipy

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Keep this secret and secure in production!

# Spotify OAuth setup with your credentials
sp_oauth = SpotifyOAuth(
    client_id='7827d46662eb4bcf8e00a64c457e3def',
    client_secret='3f0010a76d0f492d83e45241aacf5108',
    redirect_uri='http://127.0.0.1:5000/callback',
    scope='user-modify-playback-state user-read-currently-playing user-read-playback-state'
)

def get_spotify_client():
    token_info = session.get('token_info', None)
    if not token_info:
        return None
    if sp_oauth.is_token_expired(token_info):
        token_info = sp_oauth.refresh_access_token(token_info['refresh_token'])
        session['token_info'] = token_info
    access_token = token_info['access_token']
    return spotipy.Spotify(auth=access_token)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route("/callback")
def callback():
    code = request.args.get('code')
    token_info = sp_oauth.get_access_token(code)
    session['token_info'] = token_info
    return redirect(url_for('index'))

@app.route("/voice-command", methods=["GET"])
def voice_command():
    command = request.args.get("command")
    if not command:
        return jsonify({"status": "error", "message": "No command provided"})

    sp = get_spotify_client()
    if not sp:
        return jsonify({"status": "error", "message": "User not authorized"}), 401

    if "play" in command.lower():
        artist_name = command.lower().replace("play", "").strip()
        result = sp.search(q=artist_name, type="track", limit=1)
        if result['tracks']['items']:
            track = result['tracks']['items'][0]

            # Check available devices
            devices = sp.devices()
            if not devices['devices']:
                return jsonify({
                    "status": "error",
                    "message": "No active Spotify devices found. Open Spotify on a device and start playback."
                })

            # Use active device or fallback to first device
            active_device_id = None
            for device in devices['devices']:
                if device['is_active']:
                    active_device_id = device['id']
                    break
            if not active_device_id:
                active_device_id = devices['devices'][0]['id']

            # Start playback on chosen device
            sp.start_playback(device_id=active_device_id, uris=[track["uri"]])
            return jsonify({"status": "playing", "track": track["name"]})

    return jsonify({"status": "not recognized", "track": "N/A"})

if __name__ == "__main__":
    app.run(debug=True)

