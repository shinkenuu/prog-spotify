from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials


def create_spotify() -> Spotify:
    """Create and setup spotipy's Spotify client

    Returns:
        Spotify: an setup Spotify client
    """
    client_credentials = SpotifyClientCredentials()
    spotify = Spotify(auth_manager=client_credentials)

    return spotify
