import json
from os import environ

from spotify.clients import SpotifyClient


def _pprint(results):
    for result in results:
        print(json.dumps(result.dict(), indent=4))


def search_artist(artist_name=environ.get("ARTIST_NAME")):
    client = SpotifyClient()
    results = client.search_artist(artist_name)
    _pprint(results)


def search_artist_album(
    artist_name=environ.get("ARTIST_NAME"), album_name=environ.get("ALBUM_NAME")
):
    client = SpotifyClient()
    results = client.search_artist_album(artist_name, album_name)
    _pprint(results)


def fetch_artist_albums(id=environ.get("ARTIST_ID")):
    client = SpotifyClient()
    results = client.artist_albums(id)
    _pprint(results)
