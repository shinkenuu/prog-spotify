import pytest

from spotify.albums import _match_prog_spot_album
from spotify.models.spotify import Album

from tests.albums import fixtures


@pytest.mark.parametrize(
    "progarchives_album_name, spotify_albums, expected_spotify_album",
    [
        (
            fixtures.lunar_chateau_progarchives_albums[progarchives_album_id],
            fixtures.lunar_chateau_spotify_albums,
            fixtures.find_match(
                progarchives_album_id, fixtures.lunar_chateau_spotify_albums
            ),
        )
        for progarchives_album_id in fixtures.lunar_chateau_progarchives_albums
    ],
)
def test_matches_progarchives_album_to_spotify_albums(
    progarchives_album_name, spotify_albums, expected_spotify_album
):
    # ARRANGE
    # ACT
    actual_spotify_album = _match_prog_spot_album(
        progarchives_album_name=progarchives_album_name,
        spotify_albums=spotify_albums,
    )

    # ASSERT
    assert actual_spotify_album == expected_spotify_album
