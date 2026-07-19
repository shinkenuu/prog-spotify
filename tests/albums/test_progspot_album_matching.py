import pytest

from spotify.albums import _match_prog_spot_album

from tests import fixtures


GENESIS_PROGARCHIVES_ID = "1"
CAMEL_PROGARCHIVES_ID = "50"


@pytest.mark.parametrize(
    "progarchives_artist_id",
    [GENESIS_PROGARCHIVES_ID, CAMEL_PROGARCHIVES_ID],
)
def test_all_albums_match_their_expected_spotify_albums(
    progarchives_artist_id,
):
    """Verify every progspot fixture album mapping is what the matcher actually returns."""
    expected_mappings = fixtures.get_expected_album_mappings(progarchives_artist_id)
    expected_spotify_artist_id = fixtures.get_expected_spotify_artist_id(progarchives_artist_id)
    progarchives_album_names = fixtures.get_progarchives_album_names(progarchives_artist_id)
    spotify_albums = fixtures.spotify_albums(expected_spotify_artist_id)

    for mapping in expected_mappings:
        prog_album_name = progarchives_album_names[mapping.prog_album_id]

        actual = _match_prog_spot_album(
            progarchives_album_name=prog_album_name,
            spotify_albums=spotify_albums,
        )

        assert actual is not None, (
            f"ProgArchives album {mapping.prog_album_id} ({prog_album_name}) "
            f"should match but got None"
        )
        assert actual.id == mapping.spot_album_id, (
            f"ProgArchives album {mapping.prog_album_id} ({prog_album_name}) "
            f"matched {actual.id} ({actual.name}), expected {mapping.spot_album_id}"
        )


@pytest.mark.parametrize(
    "progarchives_artist_id",
    [GENESIS_PROGARCHIVES_ID, CAMEL_PROGARCHIVES_ID],
)
def test_progspot_fixture_has_artist_mapping(progarchives_artist_id):
    """Verify progspot fixture contains an artist-level mapping with spot_artist_id."""
    docs = fixtures.progspot(progarchives_artist_id)
    artist_doc = next((d for d in docs if d.spot_artist_id is not None and d.prog_album_id is None), None)
    assert artist_doc is not None, (
        f"progspot fixture for artist {progarchives_artist_id} has no artist-level mapping"
    )
    assert artist_doc.prog_artist_id == int(progarchives_artist_id)


@pytest.mark.parametrize(
    "progarchives_artist_id",
    [GENESIS_PROGARCHIVES_ID, CAMEL_PROGARCHIVES_ID],
)
def test_progspot_album_mappings_reference_valid_albums(progarchives_artist_id):
    """Verify all progspot album mappings reference ProgArchives albums that exist."""
    expected_mappings = fixtures.get_expected_album_mappings(progarchives_artist_id)
    progarchives_album_names = fixtures.get_progarchives_album_names(progarchives_artist_id)

    for mapping in expected_mappings:
        assert mapping.prog_album_id in progarchives_album_names, (
            f"progspot fixture references ProgArchives album {mapping.prog_album_id} "
            f"which doesn't exist for artist {progarchives_artist_id}"
        )


@pytest.mark.parametrize(
    "progarchives_artist_id",
    [GENESIS_PROGARCHIVES_ID, CAMEL_PROGARCHIVES_ID],
)
def test_progspot_album_mappings_reference_valid_spotify_albums(progarchives_artist_id):
    """Verify all progspot album mappings reference Spotify albums that exist in fixtures."""
    expected_mappings = fixtures.get_expected_album_mappings(progarchives_artist_id)
    expected_spotify_artist_id = fixtures.get_expected_spotify_artist_id(progarchives_artist_id)
    spotify_albums = fixtures.spotify_albums(expected_spotify_artist_id)
    spotify_album_ids = {a.id for a in spotify_albums}

    for mapping in expected_mappings:
        assert mapping.spot_album_id in spotify_album_ids, (
            f"progspot fixture references Spotify album {mapping.spot_album_id} "
            f"which isn't in the Spotify albums fixture for artist {expected_spotify_artist_id}"
        )
