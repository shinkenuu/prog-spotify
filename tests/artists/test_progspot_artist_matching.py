import pytest

from spotify.artists import _rate_candidate

from tests import fixtures


GENESIS_PROGARCHIVES_ID = "1"
GENESIS_SIMILAR_SPOTIFY_ARTIST_IDS = [
    "1i0FwIJ3oUPrLSVrDXZfrt",
    "1YWaABizGll91McSy7RLzg",
    "6vHBuUxrcpn1do5UaEJ7g6",
]

CAMEL_PROGARCHIVES_ID = "50"
CAMEL_SIMILAR_SPOTIFY_ARTIST_IDS = ["3Q1GqsBVdXT5UAJ1DANFsS"]


@pytest.mark.parametrize(
    "progarchives_artist_id, similar_spotify_artist_ids",
    [
        (GENESIS_PROGARCHIVES_ID, GENESIS_SIMILAR_SPOTIFY_ARTIST_IDS),
        (CAMEL_PROGARCHIVES_ID, CAMEL_SIMILAR_SPOTIFY_ARTIST_IDS),
    ],
)
def test_progspot_artist_is_rated_highest(
    progarchives_artist_id,
    similar_spotify_artist_ids,
):
    """The progspot fixture's expected Spotify artist beats all decoys."""
    expected_spotify_artist_id = fixtures.get_expected_spotify_artist_id(
        progarchives_artist_id
    )
    progarchives_artist = fixtures.progarchives_artist(progarchives_artist_id)
    progarchives_album_names = fixtures.get_progarchives_album_name_list(
        progarchives_artist_id
    )

    expected_artist = fixtures.spotify_artist(expected_spotify_artist_id)
    expected_albums = fixtures.spotify_albums(expected_spotify_artist_id)

    expected_rate = _rate_candidate(
        progarchives_artist_name=progarchives_artist["name"],
        progarchives_album_names=progarchives_album_names,
        spotify_artist_name=expected_artist.name,
        spotify_albums=expected_albums,
    )

    for decoy_id in similar_spotify_artist_ids:
        decoy_artist = fixtures.spotify_artist(decoy_id)
        decoy_albums = fixtures.spotify_albums(decoy_id)

        decoy_rate = _rate_candidate(
            progarchives_artist_name=progarchives_artist["name"],
            progarchives_album_names=progarchives_album_names,
            spotify_artist_name=decoy_artist.name,
            spotify_albums=decoy_albums,
        )

        assert expected_rate > decoy_rate, (
            f"Expected artist {expected_spotify_artist_id} ({expected_rate}) "
            f"should beat decoy {decoy_id} ({decoy_rate})"
        )


@pytest.mark.parametrize(
    "progarchives_artist_id",
    [GENESIS_PROGARCHIVES_ID, CAMEL_PROGARCHIVES_ID],
)
def test_progspot_artist_name_matches_exactly(progarchives_artist_id):
    """The progspot fixture's expected Spotify artist has the same name (case-insensitive)."""
    expected_spotify_artist_id = fixtures.get_expected_spotify_artist_id(
        progarchives_artist_id
    )
    progarchives_artist = fixtures.progarchives_artist(progarchives_artist_id)
    spotify_artist = fixtures.spotify_artist(expected_spotify_artist_id)

    assert progarchives_artist["name"].lower() == spotify_artist.name.lower()


@pytest.mark.parametrize(
    "progarchives_artist_id",
    [GENESIS_PROGARCHIVES_ID, CAMEL_PROGARCHIVES_ID],
)
def test_progspot_artist_pre_rate_passes_threshold(progarchives_artist_id):
    """The progspot fixture's expected Spotify artist passes the pre-rate (name-only) threshold."""
    expected_spotify_artist_id = fixtures.get_expected_spotify_artist_id(
        progarchives_artist_id
    )
    progarchives_artist = fixtures.progarchives_artist(progarchives_artist_id)
    spotify_artist = fixtures.spotify_artist(expected_spotify_artist_id)

    pre_rate = _rate_candidate(
        progarchives_artist_name=progarchives_artist["name"],
        progarchives_album_names=[],
        spotify_artist_name=spotify_artist.name,
        spotify_albums=[],
    )

    assert pre_rate >= 90, (
        f"Pre-rate {pre_rate} for artist {progarchives_artist_id} "
        f"should pass threshold 90"
    )
