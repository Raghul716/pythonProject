import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

sp_oauth = SpotifyOAuth(
    client_id=os.getenv("SPOTIFY_CLIENT_ID"),
    client_secret=os.getenv("SPOTIFY_CLIENT_SECRET"),
    redirect_uri=os.getenv("SPOTIFY_REDIRECT_URI"),
    scope="user-read-playback-state,user-modify-playback-state,user-read-currently-playing"
)

def get_spotify_client():
    token_info = sp_oauth.get_cached_token()
    if not token_info:
        auth_url = sp_oauth.get_authorize_url()
        print("Please go to the following URL and authorize:", auth_url)
        code = input("Enter the URL you were redirected to: ").split("code=")[-1]
        token_info = sp_oauth.get_access_token(code)
    access_token = token_info["access_token"]
    return spotipy.Spotify(auth=access_token)
