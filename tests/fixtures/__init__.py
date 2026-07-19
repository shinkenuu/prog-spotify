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


def get_expected_spotify_artist_id(progarchives_artist_id: str) -> str:
	"""Get the expected Spotify artist ID from progspot fixtures."""
	docs = progspot(progarchives_artist_id)
	artist_doc = next((d for d in docs if d.spot_artist_id is not None and d.prog_album_id is None), None)
	if artist_doc is None:
		raise ValueError(f"No artist-level mapping found in progspot fixture for {progarchives_artist_id}")
	return artist_doc.spot_artist_id


def get_expected_album_mappings(progarchives_artist_id: str) -> list[ProgSpot]:
	"""Get album-level progspot mappings for a ProgArchives artist.

	Returns list of ProgSpot docs that have both prog_album_id and spot_album_id set.
	"""
	docs = progspot(progarchives_artist_id)
	return [d for d in docs if d.prog_album_id is not None and d.spot_album_id is not None]


def get_progarchives_album_names(progarchives_artist_id: str) -> dict[int, str]:
	"""Get ProgArchives album names as {id: name} dict.

	Handles both dict format {id: name} and list format [{id, name, ...}].
	"""
	data = progarchives_artist(progarchives_artist_id)
	albums = data["albums"]

	if isinstance(albums, dict):
		return {int(k): v for k, v in albums.items()}
	else:
		return {album["id"]: album["name"] for album in albums}


def get_progarchives_album_name_list(progarchives_artist_id: str) -> list[str]:
	"""Get ProgArchives album names as a list of strings.

	Used for _rate_candidate which expects list[str].
	"""
	data = progarchives_artist(progarchives_artist_id)
	albums = data["albums"]

	if isinstance(albums, dict):
		return list(albums.values())
	else:
		return [album["name"] for album in albums]
