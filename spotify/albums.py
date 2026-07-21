import logging
import re

from thefuzz import process
from tqdm import tqdm

from spotify.clients import SpotifyClient
from spotify.models import ProgSpot
from spotify.models.spotify import Artist, Album
from spotify.repositories.progarchives import ProgArchivesAlbumRepository
from spotify.repositories.mongo import (
    ArtistMongoRepository,
    AlbumMongoRepository,
    ProgSpotMongoRepository,
)


def _score_album_version(album_name: str) -> int:
    """Score album version preference. Higher is better.

    Prefers remastered/stereo/expanded editions over plain versions.
    Penalizes deluxe/anniversary editions.
    """
    name_lower = album_name.lower()
    score = 0

    # Bonus for remastered/stereo/mono/expanded versions
    if "remaster" in name_lower:
        score += 10
    if "stereo" in name_lower:
        score += 10
    if "mono" in name_lower:
        score += 10
    if "expanded" in name_lower:
        score += 5

    # Penalty for deluxe/anniversary editions
    if "deluxe" in name_lower:
        score -= 10
    if "anniversary" in name_lower:
        score -= 10

    return score


def _get_base_album_name(album_name: str) -> str:
    """Extract base album name without parenthetical version info.

    e.g. 'The Snow Goose (2023 Remastered & Expanded Edition)' -> 'the snow goose'
    """
    return re.sub(r'\s*\(.*\)\s*$', '', album_name).strip().lower()


def _match_prog_spot_album(
    progarchives_album_name: str,
    spotify_albums: list[Album],
    album_fuzz_threshold: int = 90,
):
    logging.info(
        f"Matching progarchives album {progarchives_album_name} against {len(spotify_albums)} spotify albums"
    )

    if not spotify_albums:
        logging.info(f"No spotify albums to match {progarchives_album_name}")
        return None

    query_base = progarchives_album_name.lower()

    # Match using base album names (without parenthetical version info),
    # then apply version preference as tiebreaker among candidates meeting threshold.
    # This ensures all editions of the same album get equal fuzzy scores,
    # so version preference (remastered/stereo > plain > deluxe/anniversary) decides.
    candidates = []
    for album in spotify_albums:
        base_name = _get_base_album_name(album.name)
        fuzzy_score = process.extractOne(query_base, [base_name])[1]
        
        if fuzzy_score >= album_fuzz_threshold:
            version_pref = _score_album_version(album.name)
            logging.info(
                f"Spotify album {album.id} {album.name} scored {fuzzy_score} (version pref {version_pref})"
            )
            candidates.append((album, fuzzy_score, version_pref))

    if not candidates:
        logging.info(f"No spotify album match for {progarchives_album_name}")
        return None

    # Sort by fuzzy score first, then version preference as tiebreaker
    best_album, _, _ = max(candidates, key=lambda x: (x[1], x[2]))

    logging.info(
        f"Best match for {progarchives_album_name}: {best_album.id} {best_album.name}"
    )

    return best_album


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
        spot_album_id=spotify_album.id if spotify_album else None,
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
    spotify_client: SpotifyClient | None = None,
):
    logging.info(
        f"Syncing album {progarchives_album_id} {progarchives_album_name} for spotify artist {spotify_artist.id} {spotify_artist.name}"
    )

    spotify_client = spotify_client or SpotifyClient()

    spotify_artist_albums = list(
        spotify_client.artist_albums(
            spotify_artist.id, album_type="album", limit=50
        )
    )

    logging.info(
        f"Fetched {len(spotify_artist_albums)} spotify albums for {spotify_artist.name}"
    )

    spotify_album = sync(
        progarchives_artist_id=spotify_artist.progarchives_artist_id,
        progarchives_album_id=progarchives_album_id,
        progarchives_album_name=progarchives_album_name,
        spotify_albums=spotify_artist_albums,
    )

    return spotify_album


def main():
    spotify_client = SpotifyClient()

    for progarchives_artist_id, progarchives_artist_albums in tqdm(
        ProgArchivesAlbumRepository.iter_all(),
    ):
        try:
            spotify_artist = ArtistMongoRepository.find_one(
                {"_progarchives_artist_id": progarchives_artist_id}
            )

            if not spotify_artist:
                continue

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
