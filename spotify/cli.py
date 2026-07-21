"""CLI entry point for ProgSpot — match ProgArchives with Spotify."""

import json
import logging

import click
from tqdm import tqdm

from spotify import artists, albums
from spotify.clients import SpotifyClient
from spotify.repositories.local import read_visited, write_visited
from spotify.repositories.mongo import (
    find_prog_spot_albums,
    find_tracks,
    insert_audio_features,
    upsert_track,
)
from spotify.repositories.progarchives import ProgArchivesArtistRepository
from spotify.repositories.mongo import ProgSpotMongoRepository


MAX_TRACK_IDS_PER_REQUEST = 100


def _pprint(results):
    for result in results:
        print(json.dumps(result.dict(), indent=4))


@click.group()
def cli():
    """Match ProgArchives artists and albums with Spotify."""
    pass


# ---------------------------------------------------------------------------
# catch-up: iterate all ProgArchives artists, match + sync
# ---------------------------------------------------------------------------
@cli.command()
@click.option(
    "--start-from",
    default=None,
    help="ProgArchives artist ID to start from (skips all artists before this ID).",
)
def catch_up(start_from):
    """Sync all ProgArchives artists with Spotify.

    Iterates every ProgArchives artist, finds Spotify matches, and stores
    the mappings in MongoDB.  Use --start-from to resume from a specific
    artist ID after an interruption.
    """
    logging.basicConfig(
        filename="catch_up_with_progarchives.log", filemode="a", level=logging.INFO
    )

    spotify_client = SpotifyClient()

    total = ProgArchivesArtistRepository.count_all()
    logging.info(f"Total progarchives artists: {total}")

    # If --start-from is given, collect IDs to skip
    start_from_int = None
    if start_from is not None:
        start_from_int = int(start_from)
        click.echo(f"Starting from artist ID {start_from_int} (skipping earlier IDs)")

    all_artists = list(ProgArchivesArtistRepository.iter_all())

    for progarchives_artist_id, progarchives_artist in tqdm(
        all_artists, total=len(all_artists),
    ):
        # Skip artists before --start-from
        if start_from_int is not None and progarchives_artist_id < start_from_int:
            continue

        logging.debug(f"Progarchives artist {progarchives_artist_id}")

        if ProgSpotMongoRepository.has_progarchives_artist(progarchives_artist_id):
            logging.info(
                f"Progarchives artist {progarchives_artist_id} already exists in mongo"
            )
            continue

        progarchives_album_names = progarchives_artist["albums"].values()

        logging.info(f"Progarchives artist: {progarchives_artist}")

        _, *spotify_artist_albums = artists.sync(
            progarchives_artist_id=progarchives_artist_id,
            progarchives_artist_name=progarchives_artist["name"],
            progarchives_album_names=progarchives_album_names,
            spotify_client=spotify_client,
        )

        for progarchives_album_id in progarchives_artist["albums"]:
            progarchives_album_name = progarchives_artist["albums"][
                progarchives_album_id
            ]

            albums.sync(
                progarchives_artist_id=progarchives_artist_id,
                progarchives_album_id=progarchives_album_id,
                progarchives_album_name=progarchives_album_name,
                spotify_albums=spotify_artist_albums,
            )


# ---------------------------------------------------------------------------
# refresh: re-sync a single ProgArchives artist by ID
# ---------------------------------------------------------------------------
@cli.command()
@click.argument("artist_id")
def refresh(artist_id):
    """Re-sync a single ProgArchives artist by ID."""
    spotify_client = SpotifyClient()

    progarchives_artist = ProgArchivesArtistRepository.find_one(artist_id)

    progarchives_album_names = progarchives_artist["albums"].values()

    _, *spotify_artist_albums = artists.sync(
        progarchives_artist_id=artist_id,
        progarchives_artist_name=progarchives_artist["name"],
        progarchives_album_names=progarchives_album_names,
        spotify_client=spotify_client,
    )

    for progarchives_album_id in progarchives_artist["albums"]:
        progarchives_album_name = progarchives_artist["albums"][progarchives_album_id]

        albums.sync(
            progarchives_artist_id=artist_id,
            progarchives_album_id=progarchives_album_id,
            progarchives_album_name=progarchives_album_name,
            spotify_albums=spotify_artist_albums,
        )


# ---------------------------------------------------------------------------
# search-artist: search Spotify for an artist by name
# ---------------------------------------------------------------------------
@cli.command(name="search-artist")
@click.argument("artist_name")
def search_artist(artist_name):
    """Search Spotify for an artist by name."""
    client = SpotifyClient()
    results = client.search_artist(artist_name)
    _pprint(results)


# ---------------------------------------------------------------------------
# search-album: search Spotify for an artist+album
# ---------------------------------------------------------------------------
@cli.command(name="search-album")
@click.argument("artist_name")
@click.argument("album_name")
def search_album(artist_name, album_name):
    """Search Spotify for an artist+album combination."""
    client = SpotifyClient()
    results = client.search_artist_album(artist_name, album_name)
    _pprint(results)


# ---------------------------------------------------------------------------
# fetch-albums: fetch all albums for a Spotify artist
# ---------------------------------------------------------------------------
@cli.command(name="fetch-albums")
@click.argument("artist_id")
def fetch_albums(artist_id):
    """Fetch all albums for a Spotify artist by Spotify ID."""
    client = SpotifyClient()
    results = client.artist_albums(artist_id)
    _pprint(results)


# ---------------------------------------------------------------------------
# fetch-tracks: fetch tracks for all matched albums
# ---------------------------------------------------------------------------
@cli.command(name="fetch-tracks")
def fetch_tracks():
    """Fetch tracks for all ProgArchives↔Spotify matched albums."""
    from time import sleep

    spotify = SpotifyClient()

    visited = read_visited()
    progspot_albums = list(find_prog_spot_albums())
    progspot_albums.sort(key=lambda x: x["spotify_id"])

    try:
        for progspot_album in tqdm(progspot_albums):
            spotify_album_id = progspot_album["spotify_id"]

            if spotify_album_id in visited:
                continue

            sleep(1)
            album_tracks = spotify.album_tracks(spotify_album_id)
            visited.add(spotify_album_id)

            for album_track in album_tracks:
                album_track["_album_id"] = spotify_album_id
                upsert_track(album_track)

    except (Exception, KeyboardInterrupt) as error:
        click.echo(str(error), err=True)

    write_visited(visited)


# ---------------------------------------------------------------------------
# fetch-audio-features: fetch audio features for all tracks
# ---------------------------------------------------------------------------
@cli.command(name="fetch-audio-features")
def fetch_audio_features():
    """Fetch audio features for all tracks (batched 100 per request)."""
    from time import sleep

    spotify = SpotifyClient()

    visited = read_visited()
    track_ids = [track["id"] for track in find_tracks()]
    track_ids.sort()

    chunks = len(track_ids) // MAX_TRACK_IDS_PER_REQUEST

    try:
        for chunk_index in tqdm(range(chunks)):
            if str(chunk_index) in visited:
                continue

            chunk_start = chunk_index * MAX_TRACK_IDS_PER_REQUEST
            chunk_end = chunk_start + MAX_TRACK_IDS_PER_REQUEST

            chunk_track_ids = track_ids[chunk_start:chunk_end]

            sleep(1)
            audio_features = spotify.audio_features(chunk_track_ids)
            visited.add(str(chunk_index))

            insert_audio_features(audio_features)

        chunk_track_ids = track_ids[chunk_end:]
        audio_features = spotify.audio_features(chunk_track_ids)
        insert_audio_features(audio_features)

    except (Exception, KeyboardInterrupt) as error:
        click.echo(str(error), err=True)

    write_visited(visited)


if __name__ == "__main__":
    cli()
