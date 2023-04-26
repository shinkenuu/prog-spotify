from thefuzz import fuzz, process
from tqdm import tqdm

from spotify.clients import SpotifyClient
from spotify.models import ProgSpot
from spotify.models.spotify import Album
from spotify.repositories.local import ProgarchiveArtistLocalRepository
from spotify.repositories.mongo import ArtistMongoRepository, ProgSpotMongoRepository


def _rate_candidate(
    progarchives_artist_name: str,
    progarchives_album_names: list[str],
    spotify_artist_name: str,
    spotify_albums: list[Album],
    album_fuzz_threshold: int = 90,
) -> float:
    artist_score = fuzz.ratio(
        progarchives_artist_name.lower(), spotify_artist_name.lower()
    )

    if not spotify_albums:
        return artist_score

    spotify_album_names_left_to_match = [album.name.lower() for album in spotify_albums]

    albums_scores = []
    for progarchives_album_name in progarchives_album_names:
        if not spotify_album_names_left_to_match:
            break

        best_match_name, best_match_score = process.extractOne(
            progarchives_album_name.lower(), spotify_album_names_left_to_match
        )

        if best_match_score < album_fuzz_threshold:
            albums_scores.append(0)
            continue

        spotify_album_names_left_to_match.remove(best_match_name)
        albums_scores.append(best_match_score)

        # print(f"Spotify's {spotify_album_name} \t| ProgArchive's {best_match_name} - {best_match_score}")

    weighted_artist_score = 1 * artist_score
    weighted_albums_score = (
        3 * (sum(albums_scores) / len(albums_scores)) if albums_scores else 0
    )

    return weighted_artist_score + weighted_albums_score


def _search_prog_spot_match(
    progarchives_artist_name: str,
    progarchives_album_names: list[str],
    spotify_client: SpotifyClient = None,
    min_candidate_rate: int = 100,
):
    spotify_client = spotify_client or SpotifyClient()

    spotify_artist_candidates = spotify_client.search_artist(progarchives_artist_name)

    if not spotify_artist_candidates:
        return (None, *[])

    best_candidate_rate = min_candidate_rate * 1
    best_candidate = {}

    for spotify_artist_candidate in spotify_artist_candidates:
        candidate_spotify_albums = spotify_client.artist_albums(
            artist_id=spotify_artist_candidate.id,
            album_type="album",
        )

        candidate_rate = _rate_candidate(
            progarchives_artist_name=progarchives_artist_name,
            progarchives_album_names=progarchives_album_names,
            spotify_artist_name=spotify_artist_candidate.name,
            spotify_albums=candidate_spotify_albums,
        )

        if candidate_rate > best_candidate_rate:
            best_candidate_rate = candidate_rate
            best_candidate = {
                "artist": spotify_artist_candidate,
                "albums": candidate_spotify_albums,
            }

    return best_candidate.get("artist"), *best_candidate.get("albums", [])


def sync(
    progarchives_artist_id: str,
    progarchives_artist_name: str,
    progarchives_album_names: list[str],
    spotify_client: SpotifyClient = None,
):
    spotify_client = spotify_client or SpotifyClient()

    spotify_artist, *spotify_artist_albums = _search_prog_spot_match(
        progarchives_artist_name, progarchives_album_names, spotify_client
    )

    # prog_spot = ProgSpot(
    #     prog_artist_id=int(progarchives_artist_id),
    #     spot_artist_id=spotify_artist.id if spotify_artist else None,
    # )
    # ProgSpotMongoRepository.upsert_one(prog_spot)

    if not spotify_artist:
        return None, *[]

    spotify_artist.progarchives_artist_id = int(progarchives_artist_id)
    ArtistMongoRepository.upsert_one(spotify_artist)

    return spotify_artist, *spotify_artist_albums


def main():
    spotify_client = SpotifyClient()

    progarchives_artists = ProgarchiveArtistLocalRepository.read()

    for progarchives_artist_id in tqdm(progarchives_artists):
        progarchives_artist = progarchives_artists[progarchives_artist_id]
        progarchives_album_names = progarchives_artist["albums"].values()

        try:
            sync(
                progarchives_artist_id=progarchives_artist_id,
                progarchives_artist_name=progarchives_artist["name"],
                progarchives_album_names=progarchives_album_names,
                spotify_client=spotify_client,
            )
        except (Exception, KeyboardInterrupt) as error:
            print(error)


if __name__ == "__main__":
    main()