import logging

from thefuzz import process
from tqdm import tqdm

from spotify.clients import SpotifyClient
from spotify.models import ProgSpot
from spotify.models.spotify import Artist, Album
from spotify.repositories.local import ProgarchiveAlbumLocalRepository
from spotify.repositories.mongo import (
    ArtistMongoRepository,
    AlbumMongoRepository,
    ProgSpotMongoRepository,
)


def _match_prog_spot_album(
    progarchives_album_name: str,
    spotify_albums: list[Album],
    album_fuzz_threshold: int = 90,
):
    if not spotify_albums:
        return None

    spotify_album_names = [album.name.lower() for album in spotify_albums]
    best_match_name, best_match_score = process.extractOne(
        progarchives_album_name.lower(), spotify_album_names
    )

    if best_match_score < album_fuzz_threshold:
        return None

    best_match_spotify_album = next(
        (album for album in spotify_albums if album.name.lower() == best_match_name),
        None,
    )

    return best_match_spotify_album


def sync(
    progarchives_artist_id: str,
    progarchives_album_id: str,
    progarchives_album_name: str,
    spotify_albums: list[Album],
):
    logging.info(
        f"Syncing progarchives album {progarchives_album_id} {progarchives_album_name}"
    )
    spotify_album = _match_prog_spot_album(
        progarchives_album_name=progarchives_album_name, spotify_albums=spotify_albums
    )

    prog_spot = ProgSpot(
        prog_artist_id=int(progarchives_artist_id),
        prog_album_id=int(progarchives_album_id),
        spotify_album_id=spotify_album.id if spotify_album else None,
    )
    ProgSpotMongoRepository.upsert(prog_spot)

    if spotify_album:
        logging.info(
            f"Matched progarchives album {progarchives_album_id} {progarchives_album_name} to spotify album {spotify_album.id} {spotify_album.name}"
        )
        spotify_album.progarchives_album_id = int(progarchives_album_id)
        AlbumMongoRepository.upsert(spotify_album)

    return spotify_album


def sync_by_spotify_artist(
    spotify_artist: Artist,
    progarchives_album_id: int,
    progarchives_album_name: str,
    spotify_client: SpotifyClient = None,
):
    spotify_client = spotify_client or SpotifyClient()

    spotify_artist_albums = spotify_client.artist_albums(
        spotify_artist.id, album_type="album", limit=50
    )

    spotify_album = sync(
        progarchives_artist_id=spotify_artist._progarchives_artist_id,
        progarchives_album_id=progarchives_album_id,
        progarchives_album_name=progarchives_album_name,
        spotify_artist_albums=spotify_artist_albums,
    )

    return spotify_album


def main():
    spotify_client = SpotifyClient()

    progarchives_artists_albums = ProgarchiveAlbumLocalRepository.read()

    for progarchives_artist_id in tqdm(progarchives_artists_albums):
        try:
            spotify_artist = ArtistMongoRepository.find_one(
                {"_progarchives_artist_id": progarchives_artist_id}
            )

            if not spotify_artist:
                continue

            progarchives_artist_albums = progarchives_artists_albums[
                progarchives_artist_id
            ]

            for progarchives_album_id in progarchives_artist_albums:
                progarchives_album_name = progarchives_artist_albums[
                    progarchives_album_id
                ]

                sync_by_spotify_artist(
                    spotify_artist=spotify_artist,
                    progarchives_album_id=progarchives_album_id,
                    progarchives_album_name=progarchives_album_name,
                    spotify_client=spotify_client,
                )

        except (Exception, KeyboardInterrupt) as error:
            print(error)


if __name__ == "__main__":
    main()
