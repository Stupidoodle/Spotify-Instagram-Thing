import spotipy
from spotipy.oauth2 import SpotifyOAuth

class Spotify():
    def create_spotify(SCOPE, USERNAME, CLIENT_ID, CLIENT_SECRET):
        AUTH_MANAGER = SpotifyOAuth(
        scope=SCOPE,
        username=USERNAME,
        redirect_uri='http://example.com',
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        show_dialog=False)
    
        spotify = spotipy.Spotify(auth_manager=AUTH_MANAGER)

        return AUTH_MANAGER, spotify

    def pretty_print_current_song(spotify):
        playing = spotify.currently_playing()
        if playing:
            song_info = spotify.current_user_playing_track()
            return ("Playing: " + song_info["item"]["name"] + " by " + song_info["item"]["artists"][0]["name"]), (song_info["item"]["external_urls"]["spotify"])