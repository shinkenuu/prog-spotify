from datetime import datetime
from functools import wraps
import logging
from time import sleep
from typing import Iterable

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from config import MIN_SECONDS_BETWEEN_REQUESTS, PAGINATION_INTERVAL_SECONDS
from spotify.models.spotify import Artist, Album, Track, AudioFeature


def rate_limited(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        elapsed_seconds = datetime.now().timestamp() - self._last_called_timestamp

        if elapsed_seconds < MIN_SECONDS_BETWEEN_REQUESTS:
            sleep(1)

        self._last_called_timestamp = datetime.now().timestamp()
        return method(self, *args, **kwargs)

    return wrapper


class SpotifyClient:
    _last_called_timestamp = 0

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

    @rate_limited
    def search_artist(self, artist: str, limit: int = 50):
        query = self._build_query(artist=artist)
        result = self._client.search(q=query, limit=limit, type="artist")
        artists = [Artist(**item) for item in result["artists"]["items"]]
        return artists

    @rate_limited
    def search_artist_album(self, artist: str, album: str, limit: int = 50):
        query = self._build_query(artist=artist, album=album)
        result = self._client.search(q=query, limit=limit, type="album")
        albums = [Album(**item) for item in result["albums"]["items"]]
        return albums

    # ======================

    @rate_limited
    def artist_albums(self, artist_id: str, limit: int = 50, **kwargs):
        results = self._client.artist_albums(artist_id=artist_id, limit=limit, **kwargs)
        for album in self._paginate(results=results, model=Album):
            yield album

    @rate_limited
    def album_tracks(self, album_id: str, limit: int = 50, **kwargs):
        results = self._client.album_tracks(album_id=album_id, limit=limit, **kwargs)
        for track in self._paginate(results=results, model=Track):
            yield track

    @rate_limited
    def audio_features(self, track_ids: Iterable[str], **kwargs):
        results = self._client.audio_features(tracks=track_ids, **kwargs)
        for audio_feature in self._paginate(results=results, model=AudioFeature):
            yield audio_feature

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

    def _paginate(self, results, model):
        for item in self._generate_items(results):
            if item:  # Sometimes it comes as None
                yield model(**item)

    def _generate_items(
        self,
        results,
        sleep_seconds: float = PAGINATION_INTERVAL_SECONDS,
        max_pages: int = 5,
    ):
        page = 0
        while results["next"]:
            if page >= max_pages:
                break

            for item in results["items"]:
                yield item

            logging.debug(
                f"Sleeping for {PAGINATION_INTERVAL_SECONDS} seconds before next result page"
            )
            sleep(sleep_seconds)
            results = self._client.next(results)
            page += 1

        for item in results["items"]:
            yield item
