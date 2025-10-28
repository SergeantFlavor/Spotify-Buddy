import os
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth, SpotifyPKCE
from spotipy.cache_handler import CacheFileHandler

load_dotenv()
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIFY_REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
SPOTIFY_TOKEN_CACHE_PATH = os.getenv("SPOTIFY_TOKEN_CACHE", "token_store.json")
TOP_TYPE = os.getenv("TOP_TYPE")
TIME_RANGE = os.getenv("TIME_RANGE")
ARTIST_LIMIT = os.getenv("ARTIST_LIMIT")

SCOPE = "user-top-read"

def _set_cache_handler():
    return CacheFileHandler(cache_path=SPOTIFY_TOKEN_CACHE_PATH)

# Get User's Top Items
def set_spotify_client():
    cache_handler = _set_cache_handler()
    if SPOTIFY_CLIENT_SECRET:
        return SpotifyOAuth(
            client_id = SPOTIFY_CLIENT_ID,
            client_secret = SPOTIFY_CLIENT_SECRET,
            redirect_uri = SPOTIFY_REDIRECT_URI,
            scope = SCOPE,
            open_browser=True,
            cache_handler=cache_handler,
            show_dialog=False
        )
    else: 
        return SpotifyPKCE(
            client_id = SPOTIFY_CLIENT_ID,
            redirect_uri = SPOTIFY_REDIRECT_URI,
            scope = SCOPE,
            open_browser=True,
            cache_handler=cache_handler
        )

def get_spotify_client() -> spotipy.Spotify:
    auth_mgr=set_spotify_client()
    return spotipy.Spotify(auth_manager=auth_mgr)
    
def get_token_info() -> dict:
    auth_mgr=set_spotify_client()
    return auth_mgr.get_cached_token()

def main():
    sp = get_spotify_client()

    me = sp.me()
    print(f"Authenticated as: {me['display_name']} ({me['id']})")
    
    top_artists = sp.current_user_top_artists(limit=ARTIST_LIMIT, time_range=TIME_RANGE)
    artist_names = [artist["name"] for artist in top_artists.get("items",[])]
    print(f"top_artists {len(artist_names)} artist ({TIME_RANGE}): {', '.join(artist_names)}")

if __name__ == "__main__":
    main()