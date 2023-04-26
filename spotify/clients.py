from time import sleep
from typing import Iterable

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from spotify.models.spotify import Artist, Album, Track, AudioFeature


class SpotifyClient:
    def __init__(self, client_id: str = None, client_secret: str = None):
        client_credentials = SpotifyClientCredentials(
            client_id=client_id,
            client_secret=client_secret,
        )

        self._client = Spotify(
            auth_manager=client_credentials,
            requests_timeout=5,
            retries=5,
            status_retries=5,
            backoff_factor=0.3,
        )

    # ======= Search =======

    def search_artist(self, artist: str, limit: int = 50):
        query = self._build_query(artist=artist)
        result = self._client.search(q=query, limit=limit, type="artist")
        artists = [Artist(**item) for item in result["artists"]["items"]]
        return artists

    def search_artist_album(self, artist: str, album: str, limit: int = 50):
        query = self._build_query(artist=artist, album=album)
        result = self._client.search(q=query, limit=limit, type="album")
        albums = [Album(**item) for item in result["albums"]["items"]]
        return albums

    # ======================

    def artist_albums(self, artist_id: str, **kwargs):
        results = self._client.artist_albums(artist_id=artist_id, **kwargs)
        items = list(self._generate_items(results=results))
        albums = [Album(**item) for item in items]
        return albums

    def album_tracks(self, album_id: str, **kwargs):
        results = self._client.album_tracks(album_id=album_id, **kwargs)
        items = list(self._generate_items(results=results))
        tracks = [Track(**item) for item in items]
        return tracks

    def audio_features(self, track_ids: Iterable[str], **kwargs):
        results = self._client.audio_features(tracks=track_ids, **kwargs)
        items = [item for item in results if item]  # Sometimes it comes as None
        audio_features = [AudioFeature(**item) for item in items]
        return audio_features

    @staticmethod
    def _build_query(
        artist: str = None,
        album: str = None,
        year: str = None,  # this could be a range. I.e 1994-2099
    ):
        filters = []

        if artist:
            filters += ["artist:" + artist]

        if album:
            filters += ["album:" + album]

        if year:
            filters += ["year:" + year]

        query = " ".join(filters)
        return query

    def _generate_items(self, results, sleep_seconds: float = 3.0):
        while results["next"]:
            for item in results["items"]:
                yield item

            sleep(sleep_seconds)
            results = self._client.next(results)

        for item in results["items"]:
            yield item
