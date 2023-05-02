from functools import lru_cache
import json

from spotify.models.spotify import Artist, Album

_FIXTURES_BASE_PATH = "./tests/fixtures"


@lru_cache
def progarchives_artist(progarchives_artist_id: str):
    with open(
        f"{_FIXTURES_BASE_PATH}/progarchives_artists/{progarchives_artist_id}.json"
    ) as file:
        return json.load(file)


@lru_cache
def spotify_artist(spotify_artist_id: str):
    with open(
        f"{_FIXTURES_BASE_PATH}/spotify_artists/{spotify_artist_id}.json"
    ) as file:
        content = json.load(file)

    return Artist(**content)


@lru_cache
def spotify_albums(spotify_artist_id: str):
    with open(f"{_FIXTURES_BASE_PATH}/spotify_albums/{spotify_artist_id}.json") as file:
        content = json.load(file)

    return [Album(**content_element) for content_element in content]
