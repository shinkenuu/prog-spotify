import pytest

from spotify.artists import _rate_candidate

from tests import fixtures


GENESIS_PROGARCHIVES_ID = "1"
GENESIS_SPOTIFY_ARTIST_ID = "3CkvROUTQ6nRi9yQOcsB50"

GENESIS_SIMILAR_SPOTIFY_ARTIST_IDS = [
    "1i0FwIJ3oUPrLSVrDXZfrt",
    "1YWaABizGll91McSy7RLzg",
    "6vHBuUxrcpn1do5UaEJ7g6",
]


CAMEL_PROGARCHIVES_ID = "50"
CAMEL_SPOTIFY_ARTIST_ID = "3Uz6jx81OY2J5K8Z4wmy2P"
CAMEL_SIMILAR_SPOTIFY_ARTIST_IDS = ["3Q1GqsBVdXT5UAJ1DANFsS"]


@pytest.mark.parametrize(
    "desired_progarchives_artist_id, desired_spotify_artist_id, undesired_spotify_artist_ids",
    [
        (
            GENESIS_PROGARCHIVES_ID,
            GENESIS_SPOTIFY_ARTIST_ID,
            GENESIS_SIMILAR_SPOTIFY_ARTIST_IDS,
        ),
        (
            CAMEL_PROGARCHIVES_ID,
            CAMEL_SPOTIFY_ARTIST_ID,
            CAMEL_SIMILAR_SPOTIFY_ARTIST_IDS,
        ),
    ],
)
def test_rates_the_desired_higher_than_undesired_artist(
    desired_progarchives_artist_id,
    desired_spotify_artist_id,
    undesired_spotify_artist_ids,
):
    # ARRANGE
    desired_progarchives_artist = fixtures.progarchives_artist(
        desired_progarchives_artist_id
    )
    desired_spotify_artist = fixtures.spotify_artist(desired_spotify_artist_id)
    desired_spotify_artist_albums = fixtures.spotify_albums(desired_spotify_artist_id)

    # ACT
    desired_candidate_rate = _rate_candidate(
        progarchives_artist_name=desired_progarchives_artist["name"],
        progarchives_album_names=desired_progarchives_artist["albums"],
        spotify_artist_name=desired_spotify_artist.name,
        spotify_albums=desired_spotify_artist_albums,
    )

    undesired_candidates_rates = []
    for undesired_spotify_artist_id in undesired_spotify_artist_ids:
        undesired_spotify_artist = fixtures.spotify_artist(undesired_spotify_artist_id)
        undesired_spotify_artist_albums = fixtures.spotify_albums(
            undesired_spotify_artist_id
        )

        undesired_candidates_rate = _rate_candidate(
            progarchives_artist_name=desired_progarchives_artist["name"],
            progarchives_album_names=desired_progarchives_artist["albums"],
            spotify_artist_name=undesired_spotify_artist.name,
            spotify_albums=undesired_spotify_artist_albums,
        )

        undesired_candidates_rates.append(undesired_candidates_rate)

    # ASSERT
    max_undesired_candidate_rate = max(undesired_candidates_rates)

    import logging
    logging.warning('desired_candidate_rate %d', desired_candidate_rate)
    logging.warning('max_undesired_candidate_rate %d', max_undesired_candidate_rate)

    assert desired_candidate_rate > max_undesired_candidate_rate
