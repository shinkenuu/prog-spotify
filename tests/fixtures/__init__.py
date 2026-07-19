from functools import lru_cache
import json

from spotify.models import ProgSpot
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


@lru_cache
def progspot(progarchives_artist_id: str):
	"""Load ProgSpot fixture docs for a ProgArchives artist.

	Returns a list of ProgSpot model instances. The first doc is the
	artist-level mapping (prog_artist_id + spot_artist_id); subsequent
	docs are per-album mappings (prog_artist_id + prog_album_id + spot_album_id).
	"""
	with open(
		f"{_FIXTURES_BASE_PATH}/progspot/{progarchives_artist_id}.json"
	) as file:
		content = json.load(file)

	return [ProgSpot(**doc) for doc in content]
